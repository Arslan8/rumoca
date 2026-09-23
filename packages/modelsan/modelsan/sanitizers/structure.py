"""StructureSan — defects in the shape of the equation system.

Modelica equations are acausal, so "is this variable determined?" is a
*matching* question over the equation-variable bipartite graph, not something
readable from the syntax of an assignment. That is the whole basis of this
pass.

What it reports, and the confidence each carries (§26):

    high    STATE_WITHOUT_DERIVATIVE_CONSTRAINT  a state nothing integrates
            UNMATCHED_VARIABLE                   no equation left to determine it
            UNMATCHED_EQUATION                   a constraint with nothing to constrain
            CONTRADICTORY_CONSTRAINT             x = 1 and x = 2
            DUPLICATE_EQUATION                   the same constraint twice
    medium  ISOLATED_COMPONENT                   reaches nothing observable
            DEGENERATE_PARAMETER_STRUCTURE       a parameter collapses a constraint

**Structural, never algebraic.** `x + y = 0` with `2x + 2y = 0` matches
perfectly and is singular. This pass cannot see that and does not claim to;
§15 requires `STRUCTURAL_MATCH_FAILURE` and `ALGEBRAIC_SINGULARITY` stay
distinct, and only the first is in scope.

Duplicate and contradictory detection reuses the coefficient normaliser built
for ConservationSan rather than a second one — two equations are the same
constraint when their normalised forms agree up to scale, and contradictory
when the coefficients agree and the constants do not.
"""

from __future__ import annotations

import collections
import itertools

from ..analysis import structure as structural
from ..analysis.context import AnalysisContext
from ..conservation.residual import Normalised, normalise_equation
from ..findings.finding import Finding, Severity
from ..findings.location import locate
from ..instrumentation.capability import Capability
from ..runtime.anchors import CanonicalAnchor, EntityKind

#: Coefficients are small rationals; this only absorbs float division.
TOLERANCE = 1e-9


def _signature(normalised: Normalised) -> tuple | None:
    """A scale-invariant key for a linear constraint.

    `x - y = 0` and `y - x = 0` are the same constraint written twice, and
    `2x = 2` is the same as `x = 1`. Normalising by the first coefficient makes
    all three comparable; without it the duplicate check finds almost nothing.
    """
    if not normalised.ok or not normalised.coefficients:
        return None
    pivot_key = sorted(normalised.coefficients)[0]
    pivot = normalised.coefficients[pivot_key]
    if pivot == 0:
        return None
    terms = tuple(sorted(
        (key, round(value / pivot, 9))
        for key, value in normalised.coefficients.items()))
    return terms


class StructureSan:
    name = "structure"

    requires = {"static": frozenset({Capability.CANONICAL_MODEL})}

    def analyze(self, model, context: AnalysisContext) -> list[Finding]:
        graph = structural.build(model, context.dependencies)
        matching = structural.maximum_matching(graph)
        names = {v.id: v.name for v in model.variables}

        findings: list[Finding] = []
        findings += self._states_without_derivative(model, context)
        findings += self._unmatched(model, graph, matching, names)
        findings += self._duplicates(model, names)
        findings += self._singular_at_zero(model, context, graph, matching)
        return findings

    # ── topology-specific degeneracy (§ shared contracts) ────────────────────

    def _singular_at_zero(self, model, context, graph, matching) -> list[Finding]:
        """Parameters whose zero makes *this* topology structurally singular.

        The distinction this exists to preserve: a massless body is a normal
        modelling idiom, and a massless body *in a particular circuit* may
        leave that circuit under-determined. The first is not a defect and the
        second is a fact about the model, not about
        `Mechanics.Translational.Components.Mass`.

        Converting the second into the first is what produced 1448 reports
        across ten component families. This reports the topology instead, and
        names the model rather than the declaration as the place to look.
        """
        from ..contracts import ZeroBehavior, resolve
        from ..divisor import build

        try:
            contracts = resolve(model, build(model),
                                assumptions=getattr(context, "assumptions", None))
        except Exception:
            return []

        found = []
        for variable in model.variables:
            contract = contracts.get(variable.id)
            if contract is None:
                continue
            if contract.behavior not in (ZeroBehavior.ALGEBRAIC_LIMIT,
                                         ZeroBehavior.FEATURE_DISABLED):
                continue
            # At zero the terms this parameter scales drop out, and with them
            # the incidences they carried. Whether the remaining system still
            # determines everything is a matching question, and asking it is
            # the only way to tell `Inductor.L` in a circuit that tolerates a
            # short from `IdealGear.ratio`, which at zero stops constraining
            # `flange_a.tau` altogether.
            shortfall = self._shortfall_at_zero(model, graph, matching, variable)
            if shortfall is None:
                # No proof, but the shape that produced every confirmed
                # instance of this kind: the parameter scales a rate, so at
                # zero a state and its equation go together. That is balanced
                # in general and singular in particular models, and only
                # execution decides which.
                if not self._participates_in_a_state_equation(model, variable):
                    continue
                lost, missing = 0, 0
            else:
                lost, missing = shortfall
            found.append(Finding(
                sanitizer=self.name,
                kind="STRUCTURE_DEGENERATES_AT_ZERO",
                severity=Severity.LOW,
                canonical_anchors=[CanonicalAnchor(EntityKind.PARAMETER,
                                                   variable.id, variable.name)],
                source_locations=locate(variable),
                evidence={
                    "parameter": variable.name,
                    "contract": contract.explain(),
                    "contract_behavior": contract.behavior.value,
                    "contract_confidence": contract.confidence.value,
                    "confidence": "low",
                    "result": "TOPOLOGY_SPECIFIC",
                    "incidences_lost": lost,
                    "unknowns_left_undetermined": missing,
                    "evidence_kind": ("matching-shortfall" if missing
                                      else "scales-a-rate"),
                    "note": (
                        "at zero the terms this parameter scales drop out, and "
                        f"the maximum matching over this model then falls "
                        f"short by {missing}: that many unknowns have no "
                        "equation left to determine them. This is proof that "
                        "the system is under-determined at that value, and it "
                        "is a fact about this topology, not about the "
                        "component's declaration."
                        if missing else
                        "at zero this parameter removes a state and the "
                        "equation that determines it. The matching survives, "
                        "so the system is not structurally short; whether it "
                        "is *algebraically* singular depends on this model's "
                        "topology and initialization and needs execution to "
                        "decide. This is not a claim that the declaration "
                        "should forbid zero.")}))
        return found

    @staticmethod
    def _shortfall_at_zero(model, graph, matching, variable):
        """How much of the matching this parameter's zero destroys.

        Setting `p = 0` deletes every term `p * X`, and with it every incidence
        that only existed through such a term. Re-matching the graph without
        those edges is a *proof* that the model is short of equations at that
        value --- the earlier version asked instead whether `p` scaled a rate,
        which is true of every storage element and false of `IdealGear.ratio`,
        so it both over-reported and missed the case that mattered.
        """
        lost = _incidence_lost_at_zero(model, variable)
        if not lost:
            return None
        reduced = _without(graph, lost)
        after = structural.maximum_matching(reduced)
        missing = matching.size - after.size
        if missing <= 0:
            return None
        return sum(len(v) for v in lost.values()), missing


    @staticmethod
    def _participates_in_a_state_equation(model, variable) -> bool:
        """Whether this parameter scales a rate in some equation.

        The rate may be a `der()` or a variable one equation defines as one:
        `Mass` writes `m*a = f` with `der(v) = a` alongside, so looking only
        for `reads_derivative` finds nothing.
        """
        from ..contracts.infer import _rate_variables

        rates = _rate_variables(model)
        for equation in model.equations:
            if not any(v.id == variable.id for v in equation.reads):
                continue
            if getattr(equation, "reads_derivative", None):
                return True
            if any(v.id in rates for v in equation.reads):
                return True
        return False

    # ── a state nothing integrates (§20) ─────────────────────────────────────

    def _states_without_derivative(self, model, context) -> list[Finding]:
        """A continuous state whose `der(x)` appears in no equation.

        The strongest structural finding available: the model declares
        something that evolves and then never says how.
        """
        # Every partition that can carry `der(x)`, not just the scalar
        # continuous equations. An array state is constrained by an equation
        # *family* and a sampled one by a B.1b equation; walking only
        # `model.equations` reported 246 well-posed states across 41 models,
        # `imc.airGap.psi_ms` among them, whose `der()` sits in a `for` loop.
        #
        # `reads_derivative` yields Variable objects, not ids. Comparing the
        # objects against ids silently matched nothing and made every state in
        # a well-posed model look unconstrained.
        constrained: set[int] = set()
        owners = itertools.chain(
            model.equations,
            model.initial_equations,
            getattr(model, "equation_families", ()) or (),
            getattr(model, "initial_equation_families", ()) or (),
            getattr(model, "discrete_real_equations", ()) or (),
        )
        for equation in owners:
            for variable in getattr(equation, "reads_derivative", ()) or ():
                constrained.add(getattr(variable, "id", variable))

        found = []
        for variable in model.variables:
            if not getattr(variable, "is_state", False):
                continue
            if variable.id in constrained:
                continue
            found.append(Finding(
                sanitizer=self.name, kind="STATE_WITHOUT_DERIVATIVE_CONSTRAINT",
                severity=Severity.HIGH,
                canonical_anchors=[CanonicalAnchor(EntityKind.VARIABLE,
                                                   variable.id, variable.name)],
                source_locations=locate(variable),
                evidence={
                    "state": variable.name,
                    "component": str(getattr(variable, "component", "") or ""),
                    "confidence": "high",
                    "note": "declared as a continuous state, but der() of it "
                            "appears in no equation, so nothing determines how "
                            "it evolves",
                }))
        return found

    # ── matching residuals (§13, §14) ────────────────────────────────────────

    def _unmatched(self, model, graph, matching, names) -> list[Finding]:
        variables = matching.unmatched_variables(graph)
        equations = matching.unmatched_equations(graph)
        if not variables and not equations:
            return []

        spans = {e.id: e for e in model.equations}
        families = {structural.family_key(f.id): f
                    for f in getattr(model, "equation_families", ()) or ()}
        found = []

        # Report the connected region, not "the model is singular" (§14).
        region_variables, region_equations = graph.region_of(
            variables or set(), graph.equations)

        for variable_id in sorted(variables):
            relevant = sorted(graph.touching.get(variable_id, ()))[:6]
            scalars = graph.unknown_capacity.get(variable_id, 1)
            determined = matching.covered_variables.get(variable_id, 0)
            found.append(Finding(
                sanitizer=self.name, kind="UNMATCHED_VARIABLE",
                severity=Severity.HIGH,
                canonical_anchors=[CanonicalAnchor(EntityKind.VARIABLE, variable_id,
                                                   names.get(variable_id, "?"))],
                evidence={
                    "variable": names.get(variable_id, "?"),
                    "scalars": scalars,
                    "scalars_determined": determined,
                    "region_variables": len(region_variables),
                    "region_equations": len(region_equations),
                    "touching_equations": ", ".join(self._name_of(e, families)
                                                    for e in relevant) or "none",
                    "confidence": "high",
                    "result": "STRUCTURAL_MATCH_FAILURE",
                    "note": (f"{scalars - determined} of {scalars} scalars have "
                             "no equation row left to determine them"
                             if scalars > 1 else
                             "no equation in the connected structural region can "
                             "be matched to this unknown")
                            + ". This is a structural result and says nothing "
                              "about algebraic rank.",
                }))

        for key in sorted(equations):
            family = families.get(key)
            equation = spans.get(key)
            rows = graph.equation_capacity.get(key, 1)
            used = matching.covered_equations.get(key, 0)
            owner = family or equation
            # A family is over-constrained by however many of its rows found
            # nothing to determine, which is the number a maintainer needs —
            # "this `for` equation has one spare row" is actionable, "this
            # array equation is unmatched" is not.
            spare = "" if rows == 1 else f" ({rows - used} of {rows} rows spare)"
            found.append(Finding(
                sanitizer=self.name, kind="UNMATCHED_EQUATION",
                severity=Severity.HIGH,
                canonical_anchors=[CanonicalAnchor(EntityKind.EQUATION, key)],
                source_locations=locate(owner) if owner else [],
                evidence={
                    "equation": self._render(family, equation),
                    "scalar_rows": rows,
                    "rows_matched": used,
                    "confidence": "high",
                    "result": "STRUCTURAL_MATCH_FAILURE",
                    "note": "this constraint has no unknown left to determine; "
                            f"the region is over-constrained{spare}",
                }))
        return found

    @staticmethod
    def _render(family, equation) -> str:
        """The source shape of a constraint, family or scalar."""
        if family is not None:
            binders = ", ".join(str(b) for b in family.domain.binders)
            body = "; ".join(repr(b)[:60] for b in family.bodies)
            return f"for {binders} loop 0 = {body}"
        return repr(equation.residual)[:120] if equation is not None else "?"

    @staticmethod
    def _name_of(key: int, families: dict) -> str:
        """Equation keys and family keys share one namespace; say which."""
        return (f"family {structural.family_id_of(key)}"
                if structural.is_family(key) else str(key))

    # ── duplicate and contradictory constraints (§10, §11) ───────────────────

    def _duplicates(self, model, names) -> list[Finding]:
        by_shape: dict[tuple, list[tuple]] = collections.defaultdict(list)
        for equation in model.equations:
            normalised = normalise_equation(equation)
            signature = _signature(normalised)
            if signature is None:
                continue
            pivot = normalised.coefficients[sorted(normalised.coefficients)[0]]
            by_shape[signature].append((equation, normalised.constant / pivot))

        found = []
        for signature, entries in by_shape.items():
            if len(entries) < 2:
                continue
            constants = {round(c, 9) for _, c in entries}
            equations = [e for e, _ in entries]
            rendered = ", ".join(repr(e.residual)[:60] for e in equations[:3])
            if len(constants) > 1:
                found.append(Finding(
                    sanitizer=self.name, kind="CONTRADICTORY_CONSTRAINT",
                    severity=Severity.HIGH,
                    canonical_anchors=[CanonicalAnchor(EntityKind.EQUATION, e.id)
                                       for e in equations[:4]],
                    source_locations=locate(equations[0]),
                    evidence={
                        "equations": rendered,
                        "same_terms_different_constants": sorted(constants),
                        "confidence": "high",
                        "note": "these constrain the same combination of "
                                "variables to different values; no assignment "
                                "satisfies both",
                    }))
            else:
                found.append(Finding(
                    sanitizer=self.name, kind="DUPLICATE_EQUATION",
                    severity=Severity.MEDIUM,
                    canonical_anchors=[CanonicalAnchor(EntityKind.EQUATION, e.id)
                                       for e in equations[:4]],
                    source_locations=locate(equations[0]),
                    evidence={
                        "equations": rendered,
                        "count": len(equations),
                        "confidence": "medium",
                        "note": "the same constraint up to scale, stated more "
                                "than once; one of them constrains nothing new",
                    }))
        return found


def _incidence_lost_at_zero(model, parameter) -> dict[int, set[int]]:
    """equation id -> unknowns that vanish from it when `parameter` is zero.

    An unknown is lost only when *every* occurrence of it in the equation sits
    inside a product with the parameter. `p*x + x` still constrains `x`, and a
    `p` in a denominator removes nothing --- at zero that term is undefined,
    which is DivisorSan's question, not this one.
    """
    from ..dae import BinaryOp, VariableRef, ops

    def contains(node) -> bool:
        if isinstance(node, VariableRef):
            return node.variable.id == parameter.id and not node.is_derivative
        return any(contains(child) for child in node.children())

    def walk(node, scaled: bool, scaled_out: set, free_out: set) -> None:
        if isinstance(node, VariableRef):
            if node.variable.id == parameter.id and not node.is_derivative:
                return
            (scaled_out if scaled else free_out).add(node.variable.id)
            return
        if isinstance(node, BinaryOp) and node.op == ops.MULTIPLY:
            walk(node.lhs, scaled or contains(node.rhs), scaled_out, free_out)
            walk(node.rhs, scaled or contains(node.lhs), scaled_out, free_out)
            return
        for child in node.children():
            walk(child, scaled, scaled_out, free_out)

    lost: dict[int, set[int]] = {}
    for equation in model.equations:
        residual = getattr(equation, "residual", None)
        if residual is None:
            continue
        scaled: set[int] = set()
        free: set[int] = set()
        walk(residual, False, scaled, free)
        gone = scaled - free
        if gone:
            lost[equation.id] = gone
    return lost


def _without(graph, lost: dict[int, set[int]]):
    """A copy of the graph with the lost incidences deleted.

    Capacities are kept: an equation whose only unknown disappears still stands
    as a row, and counting it as gone would hide the shortfall it causes.
    """
    reduced = structural.StructuralGraph(
        unknowns=set(graph.unknowns), equations=set(graph.equations),
        unknown_capacity=dict(graph.unknown_capacity),
        equation_capacity=dict(graph.equation_capacity))
    for key, reads in graph.incident.items():
        kept = reads - lost.get(key, set())
        reduced.incident[key] = set(kept)
        for variable in kept:
            reduced.touching.setdefault(variable, set()).add(key)
    return reduced
