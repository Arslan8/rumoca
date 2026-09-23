"""What it means for a component to conserve a quantity.

The general balance, and the only one this represents:

    incoming - outgoing + generated - consumed - rate_of_storage = 0

expressed as a residual over signed terms. A component satisfies its contract
when the residual its equations implement matches the one its semantics
require.

Two things the representation deliberately allows, because assuming otherwise
is how a conservation checker becomes a false-positive generator:

**Storage is not optional.** A vessel accumulates; a pipe does not. A contract
with no storage term is a *claim* about the component, not a default.

**Terms may be explicitly excluded.** A model that states it neglects kinetic
energy is not violating energy conservation, it is documenting an
approximation. An excluded term suppresses its own absence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Role(str, Enum):
    """What part a term plays in the balance."""

    FLUX = "flux"
    """Crosses the boundary. Sign follows the connector convention."""
    STORAGE = "storage"
    """`der(x)` of an accumulated quantity. Enters negatively."""
    SOURCE = "source"
    SINK = "sink"
    LOSS = "loss"
    CONVERSION = "conversion"
    """Leaves this balance for another domain's — a motor's shaft power."""


#: How each role enters the residual. Flux uses the connector convention
#: (positive into the component), which is why it is +1 and not inferred.
SIGN: dict[Role, int] = {
    Role.FLUX: +1,
    Role.SOURCE: +1,
    Role.SINK: -1,
    Role.LOSS: -1,
    Role.CONVERSION: -1,
    Role.STORAGE: -1,
}


class Applicability(str, Enum):
    ESTABLISHED = "established"
    UNKNOWN = "unknown"
    EXCLUDED = "excluded"


class Verdict(str, Enum):
    PROVEN_CONSERVED = "PROVEN_CONSERVED"
    PROVEN_VIOLATION = "PROVEN_VIOLATION"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class Term:
    """One signed contribution, with the evidence that placed it there."""

    variable_id: int
    name: str
    role: Role
    derivative: bool = False
    """True for `der(x)`: the term is a rate, not a level."""

    evidence: str = ""
    source: str = ""

    @property
    def sign(self) -> int:
        return SIGN[self.role]

    @property
    def key(self) -> tuple[int, bool]:
        """Identity in a coefficient map: `x` and `der(x)` are different terms."""
        return (self.variable_id, self.derivative)

    def __str__(self) -> str:
        rendered = f"der({self.name})" if self.derivative else self.name
        return f"{'+' if self.sign > 0 else '-'} {rendered}"


@dataclass
class Contract:
    """The balance one component is expected to satisfy for one quantity."""

    quantity: str
    """mass | energy | charge | species | linear_momentum | ... — an open
    vocabulary, so a new conserved quantity needs no change here."""

    scope: str
    """The component path this applies to."""

    terms: list[Term] = field(default_factory=list)
    excluded: tuple[str, ...] = ()
    """Terms the model states it neglects. Their absence is not a violation."""

    applicability: Applicability = Applicability.UNKNOWN
    origin: str = ""
    """Why this contract applies, in prose, for the diagnostic."""

    provenance: str = ""

    def of_role(self, role: Role) -> list[Term]:
        return [t for t in self.terms if t.role is role]

    @property
    def expected(self) -> dict[tuple[int, bool], int]:
        """The residual as a coefficient map, which is what gets compared."""
        coefficients: dict[tuple[int, bool], int] = {}
        for term in self.terms:
            coefficients[term.key] = coefficients.get(term.key, 0) + term.sign
        return {k: v for k, v in coefficients.items() if v != 0}

    def render(self) -> str:
        if not self.terms:
            return "0 = 0"
        body = " ".join(str(t) for t in self.terms).lstrip("+ ")
        return f"{body} = 0"

    def __str__(self) -> str:
        return f"{self.quantity} over {self.scope}: {self.render()}"
