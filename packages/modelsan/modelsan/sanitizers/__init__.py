"""Sanitizers. Each implements only the capabilities it needs."""

from .assertion import AssertSan
from .base import (
    DifferentialOracle,
    FuzzHintProvider,
    InstrumentationRequester,
    RuntimeObserver,
    StaticAnalyzer,
)
from .discontinuity import DiscontinuitySan
from .event import EventSan
from .domain import DomainSan
from .initialization import InitSan
from .numeric import NumericSan
from .range import RangeSan
from .registry import SanitizerRegistry
from .singularity import SingularitySan
from .solver import SolverSan
from .zeno import ZenoSan

#: Everything that needs no capability a current backend lacks.
DEFAULT = (DomainSan, NumericSan, RangeSan, SolverSan, AssertSan,
           DiscontinuitySan, SingularitySan, InitSan, EventSan, ZenoSan)

__all__ = ["AssertSan", "DEFAULT", "DifferentialOracle", "DiscontinuitySan",
           "DomainSan", "EventSan", "FuzzHintProvider", "InitSan",
           "InstrumentationRequester",
           "NumericSan", "RangeSan", "RuntimeObserver", "SanitizerRegistry",
           "SingularitySan", "SolverSan", "StaticAnalyzer", "ZenoSan"]
