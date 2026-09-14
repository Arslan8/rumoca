"""RangeSan — a variable leaving the range its own declaration promised.

1. Bug class    the model states `min`/`max` and then computes outside them.
                Unlike a crash this is a *silent* wrong answer: the run
                completes and the trajectory is simply invalid.
2. Overlap      distinct. NumericSan needs the value to be non-finite;
                DomainSan needs a restricted operation. A mass fraction going
                to -0.0001 is neither, and it is still wrong.
3. Signal       runtime: an observed value outside a declared bound.
4. Needs        declared bounds from DAE variable metadata, plus observations.
                No instrumentation — the bounds are already in the artifact and
                the variables are already reported.
5. Transform    no.
6. Fuzzing      hints, yes: `min` and `max` themselves and their neighbourhoods
                are exactly the values worth trying.
7. Signature    DAE variable id plus which bound was broken.

Recording the magnitude of the violation matters as much as the fact of it:
-1e-15 on a quantity of order one is solver noise, -0.3 is a bug.
"""

from __future__ import annotations

from ..analysis.context import AnalysisContext
from ..findings.finding import Finding, Severity, SourceLocation
from ..fuzz.hints import FuzzHint
from ..fuzz.testcase import TestCase
from ..runtime.observations import ObservationStream, VariableObservation


def _literal(expression) -> float | None:
    return getattr(expression, "value", None) if expression is not None else None


class RangeSan:
    name = "range"

    def __init__(self, relative_tolerance: float = 1e-9) -> None:
        # Bounds are enforced by the integrator only approximately, so a
        # violation smaller than its own tolerance is not a model defect.
        self.relative_tolerance = relative_tolerance

    def _bounds(self, model) -> dict[int, tuple[float | None, float | None, object]]:
        found = {}
        for variable in model.variables:
            low = _literal(variable.minimum)
            high = _literal(variable.maximum)
            if low is not None or high is not None:
                found[variable.id] = (low, high, variable)
        return found

    def hints(self, model, context: AnalysisContext) -> list[FuzzHint]:
        """A declared bound is a value the component claims to support."""
        found = []
        for _, (low, high, variable) in self._bounds(model).items():
            if not variable.is_parameter:
                continue
            values = tuple(v for v in (low, high) if v is not None)
            if values:
                found.append(FuzzHint(
                    target=variable.name,
                    values=values,
                    reason="the parameter's own declared bound",
                    source=self.name,
                    variable_ids=(variable.id,),
                ))
        return found

    def observe(self, stream: ObservationStream, model, context: AnalysisContext,
                testcase: TestCase) -> list[Finding]:
        bounds = self._bounds(model)
        worst: dict[tuple[int, str], Finding] = {}

        for observation in stream.of(VariableObservation):
            entry = bounds.get(observation.variable_id)
            if entry is None:
                continue
            low, high, variable = entry
            for bound, limit, broken in (("min", low, lambda v, l: v < l),
                                         ("max", high, lambda v, l: v > l)):
                if limit is None or not broken(observation.value, limit):
                    continue
                excess = abs(observation.value - limit)
                if excess <= self.relative_tolerance * max(abs(limit), 1.0):
                    continue  # within the integrator's own tolerance
                key = (observation.variable_id, bound)
                previous = worst.get(key)
                if previous and previous.evidence["excess"] >= excess:
                    continue
                worst[key] = Finding(
                    sanitizer=self.name,
                    kind=f"below-{bound}" if bound == "min" else f"above-{bound}",
                    severity=Severity.MEDIUM,
                    variable_ids=[observation.variable_id],
                    source_locations=self._location(variable),
                    time=observation.time,
                    test_case=testcase,
                    evidence={
                        "variable": variable.name,
                        "bound": bound,
                        "limit": limit,
                        "value": observation.value,
                        "excess": excess,
                    },
                )
        return list(worst.values())

    @staticmethod
    def _location(variable) -> list[SourceLocation]:
        source = getattr(variable, "source", None)
        span = getattr(source, "span", None) if source else None
        if span is None:
            return []
        return [SourceLocation(file=getattr(span, "source_name", "") or "?",
                               line=getattr(span, "line", 0) or 0)]
