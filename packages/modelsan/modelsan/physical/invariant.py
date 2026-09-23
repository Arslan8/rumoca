"""A physical invariant, represented without reference to any domain.

The engine below never asks what domain a predicate came from. `mass > 0` and
`0 <= SOC <= 1` are the same kind of object to it: a comparison over model
quantities, attached to entities in the canonical DAE, with provenance for both
the Modelica source and the rule that produced it.

Keeping the representation domain-blind is what makes a new domain a matter of
adding rules rather than editing the checker.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable


class Domain(str):
    """A physical domain, named by the rule pack that defines it.

    A plain string subclass rather than an enum, deliberately. The design test
    is that adding aerodynamics or electrochemistry requires no edit to this
    module — an enum would require one, and would make the core the place every
    new domain has to touch.
    """

    __slots__ = ()

    def __repr__(self) -> str:
        return f"Domain({str.__str__(self)!r})"

    @property
    def value(self) -> str:
        """So call sites can read `.value` uniformly with other enums here."""
        return str.__str__(self)


class Enforcement(str, Enum):
    STATIC = "static"
    """Decidable from the declaration alone — a parameter with a known value."""

    RUNTIME = "runtime"
    """Depends on simulated state and must be observed."""

    EITHER = "either"
    """Static where the value is known, runtime otherwise."""


class Comparison(str, Enum):
    GT = ">"
    GE = ">="
    LT = "<"
    LE = "<="


@dataclass(frozen=True)
class Term:
    """One side of a comparison: a model variable, or a constant.

    Deliberately a small expression type rather than a bare variable id. A
    conservation law (`sum(flows) = 0`) or a relation (`density = mass/volume`)
    has to be expressible in the same representation, or the engine would need
    replacing the first time one is added.
    """

    kind: str  # "variable" | "constant" | "sum"
    variable_id: int | None = None
    name: str = ""
    value: float | None = None
    operands: tuple["Term", ...] = ()

    @staticmethod
    def variable(variable_id: int, name: str = "") -> "Term":
        return Term(kind="variable", variable_id=variable_id, name=name)

    @staticmethod
    def constant(value: float) -> "Term":
        return Term(kind="constant", value=value)

    @staticmethod
    def total(operands: tuple["Term", ...]) -> "Term":
        return Term(kind="sum", operands=operands)

    def variables(self) -> tuple[int, ...]:
        if self.kind == "variable" and self.variable_id is not None:
            return (self.variable_id,)
        return tuple(v for o in self.operands for v in o.variables())

    def evaluate(self, values: dict[int, float]) -> float | None:
        """Value under a binding of variable ids, or None if not determined."""
        if self.kind == "constant":
            return self.value
        if self.kind == "variable":
            return values.get(self.variable_id) if self.variable_id is not None else None
        parts = [o.evaluate(values) for o in self.operands]
        return None if any(p is None for p in parts) else sum(parts)

    def __str__(self) -> str:
        if self.kind == "constant":
            return f"{self.value:g}"
        if self.kind == "variable":
            return self.name or f"var:{self.variable_id}"
        return "sum(" + ", ".join(str(o) for o in self.operands) + ")"


@dataclass(frozen=True)
class Predicate:
    """`left <op> right`, over terms rather than bare variables."""

    left: Term
    op: Comparison
    right: Term

    def variables(self) -> tuple[int, ...]:
        return self.left.variables() + self.right.variables()

    def holds(self, values: dict[int, float]) -> bool | None:
        """True, False, or None when the terms are not determined."""
        a, b = self.left.evaluate(values), self.right.evaluate(values)
        if a is None or b is None:
            return None
        return {Comparison.GT: a > b, Comparison.GE: a >= b,
                Comparison.LT: a < b, Comparison.LE: a <= b}[self.op]

    def __str__(self) -> str:
        return f"{self.left} {self.op.value} {self.right}"


@dataclass(frozen=True)
class RuleProvenance:
    """Where the *rule* came from, kept beside where the model came from.

    A physical invariant is an external claim about what the model ought to
    satisfy, so a violation report has to cite the claim as well as the code.
    Without this a reader cannot tell a law of physics from someone's guess.
    """

    rule_id: str
    domain: Domain
    origin: str
    """Prose justification: "a passive resistor dissipates, so R > 0"."""

    reference: str = ""
    """A citation where one exists — an MLS clause, a textbook, a datasheet."""


@dataclass
class PhysicalInvariant:
    """One invariant instantiated against one model."""

    id: str
    predicate: Predicate
    domain: Domain
    enforcement: Enforcement
    rule: RuleProvenance
    severity: str = "medium"

    variable_ids: tuple[int, ...] = ()
    component: str = ""
    source: object = None
    """Modelica provenance of the entity constrained, when known."""

    evidence: dict = field(default_factory=dict)
    """What matched this rule to this model — quantity, unit, connector role."""

    premise: str = "unknown"
    """Whether the rule's premise --- that this object *is* the component the
    rule is about --- was established, refuted, or never settled. A first-class
    field rather than a severity, so a later stage cannot promote an advisory
    back into an error by changing one number."""

    authority: str = "quantity_or_unit"
    """What supplied that premise: a component contract, a user assumption, or
    the declared quantity."""

    canonical_declaration: str = ""

    def __str__(self) -> str:
        return f"[{self.domain.value}] {self.predicate}  ({self.rule.rule_id})"
