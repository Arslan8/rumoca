"""Sanitizers. Each implements only the capabilities it needs."""

from .assertion import AssertSan
from .behavior import BehaviorSan
from .base import (
    DifferentialOracle,
    FuzzHintProvider,
    InstrumentationRequester,
    RuntimeObserver,
    StaticAnalyzer,
)
from .determinism import DeterminismSan
from .differential import DifferentialSan
from .discontinuity import DiscontinuitySan
from .dimension import DimensionSan
from .divisor import DivisorSan
from .event import EventSan
from .domain import DomainSan
from .init_static import InitStaticSan
from .initialization import InitSan
from .numeric import NumericSan
from .physical import PhysicalSan
from .quantity import QuantitySan
from .range import RangeSan
from .registry import SanitizerRegistry
from .singularity import SingularitySan
from .network import NetworkSan
from .structure import StructureSan
from .solver import SolverSan
from .zeno import ZenoSan

#: Everything that needs no capability a current backend lacks.
DEFAULT = (DomainSan, NumericSan, RangeSan, SolverSan, AssertSan,
           DiscontinuitySan, SingularitySan, InitSan, EventSan, ZenoSan,
           PhysicalSan, DivisorSan)

#: Oracles that judge several executions against each other rather than one
#: execution against a property. The pipeline has to schedule extra runs for
#: these, so they are opt-in rather than part of DEFAULT.
COMPARATIVE = (DeterminismSan, DifferentialSan)

__all__ = ["AssertSan", "BehaviorSan", "COMPARATIVE", "DEFAULT", "DeterminismSan",
           "DifferentialSan", "DifferentialOracle", "DiscontinuitySan",
           "DimensionSan",
    "InitStaticSan",
    "NetworkSan",
    "StructureSan",
    "DivisorSan", "DomainSan", "EventSan", "FuzzHintProvider", "InitSan",
           "InstrumentationRequester",
           "NumericSan", "PhysicalSan", "QuantitySan", "RangeSan", "RuntimeObserver",
           "SanitizerRegistry",
           "SingularitySan", "SolverSan", "StaticAnalyzer", "ZenoSan"]
