"""DivisorSan — a settable parameter that can drive a denominator to zero.

1. Bug class    a parameter the user configures, which reaches a division, and
                which nothing prevents from being zero. Not "this expression
                divides" — DomainSan says that — but "*this knob* zeroes that
                divisor, and the declaration allows it."
2. Overlap      DomainSan finds the division site and can hint at its operand
                when the operand *is* a parameter. This traces backwards
                through derived parameters and arithmetic, which is where the
                interesting cases live: in BUG-014 `area` reaches a division
                two steps later, in a base class, and nothing in the component
                that declares it divides by anything at all.
3. Signal       static: a reachability path from a settable parameter to a
                denominator, with no declaration on that path excluding zero.
4. Needs        the DAE and the parameter dependency graph. Nothing at runtime,
                so it works on models no backend can execute.
5. Transform    no.
6. Fuzzing      the strongest hints available: it names the exact parameter and
                the exact value, and both are derived rather than guessed.
7. Signature    the divisor expression plus the parameter that reaches it.

Four shapes are recognised, which between them cover every division defect
filed in this project:

    x / p               direct         BUG-003  SwitchedRLC.R
    x / (a * b)         product        a factor of zero zeroes the product
    p -> d, x / d       propagated     BUG-014  area -> A -> G_m -> 1/G_m
    x / (a - b)         relational     BUG-016  Vps - Vns, zero when equal

BUG-006 is deliberately *not* in that list. `k -> C -> C*der(v)` is a vanishing
*coefficient*, not a divisor, and belongs to SingularitySan. The two families
look alike and are not the same defect.

The relational case is the one no `min` can express, and is reported with that
said explicitly.

**A limitation worth knowing before trusting the propagated case.** Rumoca
constant-folds derived parameters whose inputs are all literal: `d = k * 10`
with `k = 2` arrives in the DAE as `d = 20`, and the chain is simply gone. The
propagated shape is therefore only visible when something on the path resists
folding — a parameter declared with no default, or bound to a non-constant.
`Der.mo` is the common case: `f` and `R` have no defaults, so the divisor
`2*pi*f*R` survives and both are found.

Where the chain does fold, this sanitizer reports the *derived* parameter as a
direct risk. That is not wrong — the derived parameter is still a divisor with
no bound — but it names a value the user cannot set, so the fix it implies is
in the wrong place. Reading the source, as BUG-006 and BUG-014 were found, is
still required for those.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..analysis.context import AnalysisContext
from ..dae import BinaryOp, ops
from ..dae.traversal import walk_expressions
from ..findings.finding import Finding, Severity, SourceLocation
from ..fuzz.hints import FuzzHint
from ..instrumentation.capability import Capability
from ..runtime.anchors import CanonicalAnchor, EntityKind

#: A denominator built only from these is still zeroable by its operands.
TRANSPARENT = frozenset({ops.MULTIPLY, ops.ADD, ops.SUBTRACT})


@dataclass(frozen=True)
class DivisorRisk:
    """One settable parameter that can zero one denominator."""

    parameter: object
    divisor_id: int
    shape: str
    """direct | product | propagated | relational"""

    path: tuple[str, ...]
    """Parameter names from the settable knob to the divisor, inclusive."""

    partner: object = None
    """For a relational risk, the other side of the difference."""

    declared_min: float | None = None

    @property
    def zero_permitted(self) -> bool:
        """Whether anything on the path actually prevents zero."""
        return self.declared_min is None or self.declared_min <= 0.0


def _literal(expression):
    return getattr(expression, "value", None) if expression is not None else None


class DivisorSan:
    name = "divisor"

    requires = {
        "static": frozenset({Capability.CANONICAL_MODEL}),
        "hints": frozenset({Capability.CANONICAL_MODEL}),
    }

    # ── reachability ─────────────────────────────────────────────────────────

    @staticmethod
    def _settable_sources(variable, context: AnalysisContext,
                          seen: set[int] | None = None) -> list[tuple[object, tuple[str, ...]]]:
        """Parameters a user can set that determine this variable's value.

        A derived parameter is not a knob — `C = k/(2*pi*f*R)` is set by moving
        `k`, `f` or `R`. Walking the binding graph backwards is what makes the
        propagated cases visible; without it a per-component check sees nothing
        wrong in either component.
        """
        seen = seen or set()
        if variable.id in seen or not variable.is_parameter:
            return []
        seen = seen | {variable.id}

        sources = context.parameters.depends_on.get(variable.id, set())
        if not sources:
            return [(variable, (variable.name,))]  # a leaf: the user sets this

        found = []
        for source_id in sources:
            upstream = context.variable(source_id)
            if upstream is None:
                continue
            for parameter, path in DivisorSan._settable_sources(upstream, context, seen):
                found.append((parameter, path + (variable.name,)))
        return found or [(variable, (variable.name,))]

    def _denominators(self, model):
        """Every divisor expression, with the owner that evaluates it."""
        for owner, node in walk_expressions(model):
            if isinstance(node, BinaryOp) and node.op == ops.DIVIDE:
                yield owner, node.rhs

    def risks(self, model, context: AnalysisContext) -> list[DivisorRisk]:
        found: list[DivisorRisk] = []
        seen: set[tuple[int, int, str]] = set()

        for _owner, divisor in self._denominators(model):
            # A relational divisor is a different claim and is handled first,
            # because `a - b` also reads two parameters and would otherwise be
            # reported twice as two direct risks.
            if isinstance(divisor, BinaryOp) and divisor.op == ops.SUBTRACT:
                left, right = divisor.lhs.variables(), divisor.rhs.variables()
                if (len(left) == 1 and len(right) == 1
                        and left[0].is_parameter and right[0].is_parameter):
                    key = (divisor.id, left[0].id, "relational")
                    if key not in seen:
                        seen.add(key)
                        found.append(DivisorRisk(
                            parameter=left[0], divisor_id=divisor.id,
                            shape="relational", path=(left[0].name,),
                            partner=right[0],
                            declared_min=_literal(left[0].minimum)))
                    continue

            shape = "direct"
            if isinstance(divisor, BinaryOp) and divisor.op in TRANSPARENT:
                shape = "product" if divisor.op == ops.MULTIPLY else "sum"

            for variable in divisor.variables():
                if not variable.is_parameter:
                    continue
                for parameter, path in self._settable_sources(variable, context):
                    kind = "propagated" if len(path) > 1 else shape
                    key = (divisor.id, parameter.id, kind)
                    if key in seen:
                        continue
                    seen.add(key)
                    found.append(DivisorRisk(
                        parameter=parameter, divisor_id=divisor.id, shape=kind,
                        path=path, declared_min=_literal(parameter.minimum)))
        return found

    # ── reporting ────────────────────────────────────────────────────────────

    def analyze(self, model, context: AnalysisContext) -> list[Finding]:
        # Grouped by parameter, not by divisor site. One parameter reaching
        # three denominators is one thing to fix; reporting it three times
        # would make a widely-used knob look like three defects.
        grouped: dict[tuple[int, str], list[DivisorRisk]] = {}
        for risk in self.risks(model, context):
            if not risk.zero_permitted:
                continue
            grouped.setdefault((risk.parameter.id, risk.shape), []).append(risk)

        findings = []
        for group in grouped.values():
            risk = group[0]  # the declaration already excludes zero
            relational = risk.shape == "relational"
            sites = sorted({r.divisor_id for r in group})
            findings.append(Finding(
                sanitizer=self.name,
                kind=("divisor-zero-when-parameters-equal" if relational
                      else "divisor-reachable-zero"),
                severity=Severity.HIGH if risk.shape in ("direct", "relational")
                         else Severity.MEDIUM,
                canonical_anchors=[
                    CanonicalAnchor(EntityKind.PARAMETER, risk.parameter.id,
                                    risk.parameter.name),
                    # The first site only: the parameter is the fix site, and
                    # putting every divisor in the anchor list would make the
                    # signature depend on how many places use it.
                    CanonicalAnchor(EntityKind.EXPRESSION, sites[0]),
                ],
                source_locations=_location(risk.parameter),
                evidence={
                    "parameter": risk.parameter.name,
                    "shape": risk.shape,
                    "path": " -> ".join(risk.path),
                    "declared_min": risk.declared_min,
                    "divisor_sites": len(sites),
                    **({"partner": risk.partner.name,
                        "note": "zero when the two are equal; min/max cannot "
                                "express a constraint between two parameters, "
                                "so an assertion is the only mechanism"}
                       if relational else
                       {"note": "reaches a denominator and nothing excludes zero"}),
                },
            ))
        return findings

    def hints(self, model, context: AnalysisContext) -> list[FuzzHint]:
        found, emitted = [], set()
        for risk in self.risks(model, context):
            if not risk.zero_permitted or risk.parameter.id in emitted:
                continue
            emitted.add(risk.parameter.id)
            if risk.shape == "relational" and risk.partner is not None:
                # Not zero — the value that makes the *difference* zero.
                partner = _literal(risk.partner.binding)
                if partner is None:
                    continue
                found.append(FuzzHint(
                    target=risk.parameter.name, values=(partner,),
                    reason=f"equals {risk.partner.name}, zeroing the divisor "
                           f"{risk.parameter.name} - {risk.partner.name}",
                    source=self.name, variable_ids=(risk.parameter.id,)))
            else:
                found.append(FuzzHint(
                    target=risk.parameter.name, values=(0.0,),
                    reason=f"reaches a denominator via {' -> '.join(risk.path)}",
                    source=self.name, variable_ids=(risk.parameter.id,)))
        return found


def _location(variable) -> list[SourceLocation]:
    source = getattr(variable, "source", None)
    span = getattr(source, "span", None) if source else None
    if span is None:
        return []
    return [SourceLocation(file=getattr(span, "source_name", "") or "?",
                           line=getattr(span, "line", 0) or 0)]
