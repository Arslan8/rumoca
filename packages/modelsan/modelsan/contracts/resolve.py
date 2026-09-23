"""Choosing one contract per symbol, by authority.

    hard source arithmetic
        > explicit source bounds and assertions
        > user contract
        > component catalog
        > quantity/unit heuristic

The same ordering as `semantics.binding.BindingSource`, for the same reason:
it is an ordering of *authority*, not of quality. A user contract outranks the
catalog because the user knows their application; it does not outrank the
source because the source is what runs.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import catalog as component_catalog
from .assumptions import AssumptionSet
from .behavior import Confidence, Source, ZeroBehavior, ZeroContract
from .infer import (_declaration, bounds_contract, declared_value_contract,
                    infer)


@dataclass
class ContractSet:
    """Every symbol's zero contract for one model, and how it was chosen."""

    by_id: dict[int, ZeroContract] = field(default_factory=dict)
    assumptions: AssumptionSet | None = None
    considered: dict[int, list[ZeroContract]] = field(default_factory=dict)
    """Every candidate, for `--explain-contract`."""

    def get(self, variable_id: int) -> ZeroContract | None:
        return self.by_id.get(variable_id)

    def zero_is_safe(self, variable_id: int) -> ZeroContract | None:
        """The contract, when it says a detector should stop reporting zero."""
        contract = self.by_id.get(variable_id)
        return contract if contract and contract.zero_is_safe else None

    def explain(self, variable_id: int) -> str:
        """Every candidate and the one that won."""
        candidates = self.considered.get(variable_id, [])
        if not candidates:
            return "no contract applies to this symbol"
        chosen = self.by_id.get(variable_id)
        lines = []
        for candidate in sorted(candidates, key=lambda c: -c.authority):
            mark = "->" if candidate is chosen else "  "
            lines.append(f" {mark} [{candidate.authority}] {candidate.explain()}")
        return "\n".join(lines)


def resolve(model, environment, assumptions: AssumptionSet | None = None,
            use_assumptions: bool = True) -> ContractSet:
    """Build the contract set for one model."""
    resolved = ContractSet(assumptions=assumptions)
    inferred = infer(model, environment)

    for variable in model.variables:
        if not variable.is_parameter:
            continue
        declaration = _declaration(variable)
        candidates: list[ZeroContract] = []

        from_source = inferred.get(variable.id)
        if from_source is not None and from_source.behavior != ZeroBehavior.UNKNOWN:
            candidates.append(from_source)

        from_bound = bounds_contract(variable, environment)
        if from_bound is not None:
            candidates.append(from_bound)

        from_default = declared_value_contract(variable, environment)
        if from_default is not None:
            candidates.append(from_default)

        if use_assumptions and assumptions is not None:
            from_user = assumptions.lookup(declaration, variable.name)
            if from_user is not None:
                candidates.append(from_user)

        from_catalog = component_catalog.lookup(declaration)
        if from_catalog is not None:
            candidates.append(ZeroContract(
                behavior=from_catalog.behavior,
                confidence=from_catalog.confidence,
                source=from_catalog.source, reason=from_catalog.reason,
                canonical_declaration=from_catalog.canonical_declaration,
                target=variable.name, match_kind=from_catalog.match_kind))

        if not candidates:
            if from_source is not None:
                candidates.append(from_source)      # the UNKNOWN case
            else:
                continue

        resolved.considered[variable.id] = candidates
        # A proven source division is never overridden. Everything else goes
        # by authority, with a proven result beating a declared or assumed one
        # at equal authority.
        proven_divisor = next(
            (c for c in candidates
             if c.behavior == ZeroBehavior.DIRECT_DIVISOR
             and c.confidence == Confidence.PROVEN), None)
        if proven_divisor is not None:
            resolved.by_id[variable.id] = proven_divisor
            continue
        resolved.by_id[variable.id] = max(
            candidates,
            key=lambda c: (c.authority,
                           {Confidence.PROVEN: 2, Confidence.DECLARED: 1,
                            Confidence.ASSUMED: 0}[c.confidence]))

    _propagate(model, resolved)
    return resolved


#: Behaviours a parameter may inherit from what it configures. `FORBIDDEN` is
#: not among them: a bound on the consumer says nothing about the supplier.
_INHERITABLE = (ZeroBehavior.ALGEBRAIC_LIMIT, ZeroBehavior.FEATURE_DISABLED,
                ZeroBehavior.ALLOWED)


def _propagate(model, resolved: ContractSet) -> None:
    """Carry a contract back to the knob that configures it.

    `Rotational.Examples.First` declares `Jmotor` and `Jload` at the top level
    and binds `inertia1.J = Jmotor`. `Jmotor` appears in no equation, so no
    contract is inferred for it, and the positivity rule fires on the knob the
    user actually sets while being correctly suppressed on the component it
    feeds. The two must agree.

    Inheritance is conservative in three ways: only from a *proven* or
    *declared* contract, only when every consumer agrees, and never for
    `DIRECT_DIVISOR` --- a knob feeding a divisor is reported on its own
    merits by the division analysis, which names the parameter a user can set.
    """
    consumers: dict[int, list[int]] = {}
    for variable in model.variables:
        contract = getattr(variable, "contract", None)
        if contract is None:
            continue
        for supplier in contract.binding_depends_on:
            consumers.setdefault(supplier, []).append(variable.id)

    for supplier, fed in consumers.items():
        if supplier in resolved.by_id:
            continue
        behaviours = set()
        inherited = None
        for consumer in fed:
            downstream = resolved.by_id.get(consumer)
            if downstream is None or downstream.behavior not in _INHERITABLE:
                behaviours.add(None)
                break
            behaviours.add(downstream.behavior)
            inherited = inherited or downstream
        if None in behaviours or len(behaviours) != 1 or inherited is None:
            continue
        name = next((v.name for v in model.variables if v.id == supplier), "")
        carried = ZeroContract(
            behavior=inherited.behavior, confidence=inherited.confidence,
            source=inherited.source,
            reason=(f"inherited from {inherited.target or 'the component it '
                    'configures'}, which it binds: {inherited.reason}"),
            canonical_declaration=inherited.canonical_declaration,
            target=name, origin=inherited.origin,
            match_kind="inherited-through-binding")
        resolved.by_id[supplier] = carried
        resolved.considered.setdefault(supplier, []).append(carried)
