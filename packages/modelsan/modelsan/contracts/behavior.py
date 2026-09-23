"""What zero *means* for a parameter, as one shared classification.

Three detectors were each deciding this separately and disagreeing.
`Inductor.L` reaches a denominator in the solved DAE, so DivisorSan called it a
divide-by-zero; its declared quantity is an inductance, so PhysicalSan called
it a missing positivity bound; and the library documentation says plainly that
`L` may be zero, at which point the component becomes an ideal short. Two of
those three were wrong about the same parameter for different reasons, and
1448 reports across ten groups came from that disagreement.

The fix is not a third opinion. It is one classification, computed once, with
provenance, that every detector consults.

**Zero is not one thing.** The constitutive equation decides what it means:

    L*der(i) = v        at L=0 this is `v = 0`, an ideal short
    m*a = f_a + f_b     at m=0 this is a force balance
    Q_flow = G*dT       at G=0 no heat flows
    flow = level/R      at R=0 this is undefined

The first three are supported limits of the physics the component models. The
fourth is a defect. A detector that cannot tell them apart will either report
all four or none.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ZeroBehavior(str, Enum):
    """What happens to the model when a parameter is zero."""

    DIRECT_DIVISOR = "direct_divisor"
    """Zero reaches an active denominator written in the source."""

    ALGEBRAIC_LIMIT = "algebraic_limit"
    """Zero turns a differential relation into an algebraic constraint.

    `L*der(i) = v` becomes `v = 0`. The component still means something — an
    ideal short, a massless body, a rigid connection — and the library usually
    documents it as supported.
    """

    FEATURE_DISABLED = "feature_disabled"
    """Zero removes an optional term or subsystem, leaving the rest intact."""

    ALLOWED = "allowed"
    """Zero is explicitly supported, without more specific semantics."""

    FORBIDDEN = "forbidden"
    """A bound or an assertion excludes zero."""

    UNKNOWN = "unknown"
    """Not enough evidence. Never treated as either safe or unsafe."""


class Confidence(str, Enum):
    """How the behaviour was established. Every suppression must say which."""

    PROVEN = "proven"
    """Derived from the model's own source equations or bounds."""

    DECLARED = "declared"
    """Stated by the component's catalog entry — its documented contract."""

    ASSUMED = "assumed"
    """Supplied by the user. An input to the analysis, not a result of it."""


class Source(str, Enum):
    EQUATION = "equation"
    BOUND = "bound"
    CLASS_CATALOG = "class_catalog"
    USER_CONFIG = "user_config"


#: Authority, lowest first. Mirrors `semantics.binding.BindingSource`, because
#: the two answer neighbouring questions and a second ordering would drift.
#:
#: The one rule that is not negotiable: a user assumption may override a
#: heuristic or a catalog entry, and may **never** override a proven active
#: source division. An assumption that a parameter is safe does not make the
#: arithmetic go away.
AUTHORITY = {
    Source.CLASS_CATALOG: 2,
    Source.USER_CONFIG: 3,
    Source.BOUND: 4,
    Source.EQUATION: 5,
}


@dataclass(frozen=True)
class ZeroContract:
    """One decision about one symbol, and everything behind it."""

    behavior: ZeroBehavior
    confidence: Confidence
    source: Source
    reason: str
    canonical_declaration: str = ""
    """The class-qualified declaration this applies to, e.g.
    `Modelica.Electrical.Analog.Basic.Inductor.L`."""

    target: str = ""
    """The flattened instance it was applied to."""

    origin: str = ""
    """Where a user contract came from: the file and the rule that matched."""

    match_kind: str = ""
    """exact-declaration | exact-instance | prefix — prefix is lower confidence."""

    @property
    def authority(self) -> int:
        return AUTHORITY.get(self.source, 0)

    @property
    def zero_is_safe(self) -> bool:
        """Whether a detector should stop reporting zero for this symbol.

        `UNKNOWN` is deliberately not safe. Insufficient evidence is a reason
        to keep looking, not a reason to stop.
        """
        return self.behavior in (ZeroBehavior.ALGEBRAIC_LIMIT,
                                 ZeroBehavior.FEATURE_DISABLED,
                                 ZeroBehavior.ALLOWED,
                                 ZeroBehavior.FORBIDDEN)

    def explain(self) -> str:
        """One line a suppression can quote verbatim."""
        where = self.canonical_declaration or self.target or "this symbol"
        detail = f"{self.behavior.value} ({self.confidence.value}, "\
                 f"from {self.source.value})"
        line = f"{where}: {detail} — {self.reason}"
        if self.origin:
            line += f" [{self.origin}]"
        if self.match_kind == "prefix":
            line += " [matched by prefix, lower confidence]"
        return line
