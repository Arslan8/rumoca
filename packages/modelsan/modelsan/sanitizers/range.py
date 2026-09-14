"""RangeSan — a variable leaving the range its own declaration promised.

1. Bug class    the model states `min`/`max` and computes outside them. Unlike a
                crash this is a *silent* wrong answer: the run completes and the
                trajectory is simply invalid.
2. Overlap      distinct. NumericSan needs the value to be non-finite; DomainSan
                needs a restricted operation. A mass fraction reaching -1.3e-1 is
                neither, and is still wrong.
3. Signal       runtime: an observed value outside a declared bound.
4. Needs        OBSERVE_VARIABLE. Bounds come from DAE metadata, already in the
                artifact. Canonical identity is *not* required — see below.
5. Transform    no.
6. Fuzzing      hints: the bounds themselves are the values worth trying.
7. Signature    the anchored variable plus which bound broke. Canonical where
                available, backend-namespaced otherwise.

**Backend-only anchoring is deliberate.** OpenModelica reports variable names,
not DAE ids. Discarding a real violation because the identity is weaker would
throw away bug-finding capability; inventing a DAE id would corrupt identity
semantics for everything downstream. So the finding is kept and labelled
backend-only, and the bound is matched by name.
"""

from __future__ import annotations

from ..analysis.context import AnalysisContext
from ..findings.finding import Finding, Severity, SourceLocation
from ..fuzz.hints import FuzzHint
from ..fuzz.testcase import TestCase
from ..instrumentation.capability import Capability
from ..runtime.anchors import EntityKind
from ..runtime.observations import ObservationStream, VariableObservation


def _literal(expression) -> float | None:
    return getattr(expression, "value", None) if expression is not None else None


class RangeSan:
    name = "range"

    #: Notably does *not* require CANONICAL_IDENTITY: a named observation and a
    #: declared bound are enough to establish the violation.
    requires = {
        "runtime": frozenset({Capability.OBSERVE_VARIABLE,
                              Capability.CANONICAL_MODEL}),
        "hints": frozenset({Capability.CANONICAL_MODEL}),
    }

    def __init__(self, relative_tolerance: float = 1e-9) -> None:
        # Bounds are enforced by an integrator only approximately, so a
        # violation below its own tolerance is not a model defect.
        self.relative_tolerance = relative_tolerance

    def _bounds(self, model):
        """{name: (min, max, variable)} — keyed by name so a backend-anchored
        observation can be matched without a canonical id."""
        found = {}
        for variable in model.variables:
            low, high = _literal(variable.minimum), _literal(variable.maximum)
            if low is not None or high is not None:
                found[variable.name] = (low, high, variable)
        return found

    def hints(self, model, context: AnalysisContext) -> list[FuzzHint]:
        found = []
        for _, (low, high, variable) in self._bounds(model).items():
            if not variable.is_parameter:
                continue
            values = tuple(v for v in (low, high) if v is not None)
            if values:
                found.append(FuzzHint(
                    target=variable.name, values=values,
                    reason="the parameter\'s own declared bound",
                    source=self.name, variable_ids=(variable.id,)))
        return found

    def observe(self, stream: ObservationStream, model, context: AnalysisContext,
                testcase: TestCase) -> list[Finding]:
        bounds = self._bounds(model)
        worst: dict[tuple[str, str], Finding] = {}

        for observation in stream.of(VariableObservation):
            name = observation.label
            entry = bounds.get(name)
            if entry is None:
                continue
            low, high, variable = entry
            for bound, limit, broken in (("min", low, lambda v, l: v < l),
                                         ("max", high, lambda v, l: v > l)):
                if limit is None or not broken(observation.value, limit):
                    continue
                excess = abs(observation.value - limit)
                if excess <= self.relative_tolerance * max(abs(limit), 1.0):
                    continue
                key = (name, bound)
                previous = worst.get(key)
                if previous and previous.evidence["excess"] >= excess:
                    continue
                worst[key] = Finding(
                    sanitizer=self.name,
                    kind="below-min" if bound == "min" else "above-max",
                    severity=Severity.MEDIUM,
                    # Whichever identity the observation actually carried. The
                    # canonical one is only asserted when the producer knew it.
                    canonical_anchors=([observation.canonical]
                                       if observation.canonical else []),
                    backend_anchors=([observation.backend]
                                     if observation.backend else []),
                    source_locations=self._location(variable),
                    phase=observation.phase,
                    time=observation.time,
                    test_case=testcase,
                    evidence={"variable": name, "bound": bound, "limit": limit,
                              "value": observation.value, "excess": excess,
                              "anchor_quality": observation.anchor_quality.value},
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
