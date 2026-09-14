"""Capabilities a sanitizer may implement. It implements only what it uses.

There is deliberately no `Sanitizer` base class with a dozen methods. Most
sanitizers need one or two of these; a shared base would force every one of them
to carry stubs for the rest, and would make it tempting to reach across
capability boundaries.

    StaticAnalyzer           reads the DAE, no execution needed
    RuntimeObserver          judges an observation stream
    InstrumentationRequester needs something observed that is not by default
    FuzzHintProvider         knows values worth trying
    DifferentialOracle       compares results from several backends

A sanitizer declares `name`; everything else is opt-in and discovered by
`isinstance` against these protocols.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ..analysis.context import AnalysisContext
from ..backends.base import ExecutionResult
from ..findings.finding import Finding
from ..fuzz.hints import FuzzHint
from ..fuzz.testcase import TestCase
from ..instrumentation.request import InstrumentationRequest
from ..runtime.observations import ObservationStream


@runtime_checkable
class StaticAnalyzer(Protocol):
    """Finds violations, or candidates, without running anything."""

    name: str

    def analyze(self, model, context: AnalysisContext) -> list[Finding]: ...


@runtime_checkable
class RuntimeObserver(Protocol):
    """Judges what one execution reported."""

    name: str

    def observe(self, stream: ObservationStream, model,
                context: AnalysisContext, testcase: TestCase) -> list[Finding]: ...


@runtime_checkable
class InstrumentationRequester(Protocol):
    """Declares the observations it needs to do its job."""

    name: str

    def requests(self, model, context: AnalysisContext) -> list[InstrumentationRequest]: ...


@runtime_checkable
class FuzzHintProvider(Protocol):
    """Suggests values worth trying, with reasons."""

    name: str

    def hints(self, model, context: AnalysisContext) -> list[FuzzHint]: ...


@runtime_checkable
class DifferentialOracle(Protocol):
    """Judges agreement between backends rather than one execution."""

    name: str

    def compare(self, results: dict[str, ExecutionResult], model,
                testcase: TestCase) -> list[Finding]: ...


#: Parameters that configure presentation or diagnostics rather than physics.
#: Perturbing `world.defaultFrameDiameterFraction` breaks a picture, not a
#: model, and reporting it wastes a reviewer's attention on nothing.
COSMETIC_MARKERS = (
    "animation", "defaultframe", "defaultwidth", "defaultlength",
    "defaultdiameter", "defaultarrow", "defaultheadl", "shapetype",
    "color", "specularcoefficient", "diameterfraction", "widthfraction",
    "lengthfraction", "enableanimation", "logging", "loglevel",
)


def is_cosmetic(name: str) -> bool:
    """Whether a parameter only affects how a model is drawn or logged."""
    lowered = name.lower()
    return any(marker in lowered for marker in COSMETIC_MARKERS)
