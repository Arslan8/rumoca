"""InitSan — initialization treated as its own problem.

1. Bug class    the model cannot reach a consistent initial state. Different
                causes and different fixes from a transient failure: an
                over- or under-determined initialization system, a `start`
                value outside the variable's own declared bounds, a fixed
                initial value that contradicts an equation.
2. Overlap      SolverSan already separates initialization failures by phase,
                so the *runtime* halves overlap. What this adds is static: the
                contradictions visible before anything runs.
3. Signal       static: a `start` outside `min`/`max`; the initialization
                system's equation and unknown counts disagreeing.
                runtime: a failure whose phase is initialization.
4. Needs        DAE variable attributes and initial equations. No instrumentation.
5. Transform    no.
6. Fuzzing      hints on initial values rather than parameters, which is a
                dimension parameter fuzzing does not reach at all.
7. Signature    the variable, or the initialization system as a whole.
"""

from __future__ import annotations

from ..analysis.context import AnalysisContext
from ..instrumentation.capability import Capability
from .base import is_cosmetic
from ..findings.finding import Finding, Severity, SourceLocation
from ..fuzz.hints import FuzzHint
from ..runtime.anchors import CanonicalAnchor, EntityKind


def _literal(expression):
    return getattr(expression, "value", None) if expression is not None else None


class InitSan:
    name = "init"

    requires = {
        "static": frozenset({Capability.CANONICAL_MODEL}),
        "hints": frozenset({Capability.CANONICAL_MODEL}),
    }

    def analyze(self, model, context: AnalysisContext) -> list[Finding]:
        findings = []

        for variable in model.variables:
            start = _literal(variable.start)
            if start is None:
                continue
            low, high = _literal(variable.minimum), _literal(variable.maximum)
            for bound, limit, broken in (("min", low, lambda s, l: s < l),
                                         ("max", high, lambda s, l: s > l)):
                if limit is None or not broken(start, limit):
                    continue
                findings.append(Finding(
                    sanitizer=self.name,
                    kind=f"start-violates-{bound}",
                    # A declaration contradicting itself needs no execution to
                    # be wrong, which is why this is HIGH despite being static.
                    severity=Severity.HIGH,
                    canonical_anchors=[CanonicalAnchor(EntityKind.VARIABLE,
                                                       variable.id, variable.name)],
                    source_locations=_location(variable),
                    evidence={"variable": variable.name, "start": start,
                              "bound": bound, "limit": limit},
                ))

        states = [v for v in model.variables if v.is_state]
        if states and model.initial_equations:
            supplied = len(model.initial_equations) + sum(
                1 for v in states if _literal(v.start) is not None and v.fixed)
            if supplied != len(states):
                findings.append(Finding(
                    sanitizer=self.name,
                    kind="initialization-count-mismatch",
                    # Structural counting over bitcode is an approximation:
                    # it cannot see everything the compiler's own balance check
                    # does, so this is a candidate rather than a verdict.
                    severity=Severity.INFO,
                    evidence={"states": len(states),
                              "initial_equations": len(model.initial_equations),
                              "fixed_starts": supplied - len(model.initial_equations),
                              "note": "approximate; the compiler's balance check "
                                      "is authoritative"},
                ))
        return findings

    def hints(self, model, context: AnalysisContext) -> list[FuzzHint]:
        """Initial values at the edge of each state's declared range.

        A dimension parameter fuzzing never reaches: a model can be perfectly
        well behaved for every parameter value and still fail from a legal
        starting point.
        """
        found = []
        for variable in model.variables:
            if not variable.is_state or is_cosmetic(variable.name):
                continue
            low, high = _literal(variable.minimum), _literal(variable.maximum)
            values = tuple(v for v in (low, high, 0.0) if v is not None)
            if values:
                found.append(FuzzHint(
                    target=variable.name,
                    values=values,
                    reason="initial value at the edge of the state's declared range",
                    source=self.name,
                    variable_ids=(variable.id,),
                ))
        return found


def _location(variable) -> list[SourceLocation]:
    source = getattr(variable, "source", None)
    span = getattr(source, "span", None) if source else None
    if span is None:
        return []
    return [SourceLocation(file=getattr(span, "source_name", "") or "?",
                           line=getattr(span, "line", 0) or 0)]
