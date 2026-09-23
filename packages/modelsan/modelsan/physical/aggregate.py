"""Rules whose subject is a group of declarations, not one of them.

A moment of inertia is not a positive scalar. `Modelica.Mechanics.MultiBody
.Parts.Body` declares six fields that assemble into

    I = | I_11  I_21  I_31 |
        | I_21  I_22  I_32 |
        | I_31  I_32  I_33 |

and the constraint on that object is that it is symmetric positive
semidefinite. The off-diagonal entries are *products* of inertia: they are
signed, the declaration says so with `min = -Modelica.Constants.inf`, and a
zero off-diagonal means the body's principal axes are aligned with the frame,
which is the common case rather than a defect.

Checking each field against `> 0` produced **182 reports** on valid tensors and
would have missed an invalid one: a tensor can have three positive diagonal
entries and a negative eigenvalue. `[[1,2,0],[2,1,0],[0,0,1]]` is the smallest
example, and every scalar rule passes on it.

So the group is the subject. One tensor yields at most one finding, its fields
are removed from the scalar rule, and the diagnostic carries the assembled
matrix and either the eigenvalues or the principal minor that failed.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum

#: The six scalar fields of a symmetric inertia tensor, in the order MSL
#: declares them, with the position each occupies.
FIELDS: dict[str, tuple[int, int]] = {
    "I_11": (0, 0), "I_22": (1, 1), "I_33": (2, 2),
    "I_21": (1, 0), "I_31": (2, 0), "I_32": (2, 1),
}

#: The assembled matrix, declared alongside the fields and bound to them.
MATRIX = "I"

#: Quantities a 3x3 declaration of this shape carries.
TENSOR_QUANTITIES = frozenset({"MomentOfInertia", "Inertia"})


class Verdict(str, Enum):
    VALID = "valid"
    INVALID = "invalid"
    UNKNOWN = "unknown"


@dataclass
class Tensor:
    """One component instance's inertia tensor."""

    owner: str
    """The instance path: `body.body` for `body.body.I_11`."""

    declaring_class: str
    fields: dict[str, object] = field(default_factory=dict)
    """Field name -> the variable declaring it."""

    matrix: object = None
    """The assembled 3x3 variable, when the class declares one."""

    values: dict[str, float] = field(default_factory=dict)
    verdict: Verdict = Verdict.UNKNOWN
    reason: str = ""
    eigenvalues: tuple[float, float, float] | None = None
    failed_minor: str = ""
    realizable: bool | None = None
    """Whether each principal moment is at most the sum of the other two.
    `None` when the tensor is not numerically known."""

    @property
    def variable_ids(self) -> set[int]:
        found = {v.id for v in self.fields.values()}
        if self.matrix is not None:
            found.add(self.matrix.id)
        return found

    @property
    def field_names(self) -> tuple[str, ...]:
        prefix = f"{self.owner}." if self.owner else ""
        if not self.fields:
            return (f"{prefix}{MATRIX}",)
        return tuple(f"{prefix}{name}" for name in FIELDS)

    @property
    def rows(self) -> list[list[float]] | None:
        if len(self.values) != len(FIELDS):
            return None
        m = [[0.0] * 3 for _ in range(3)]
        for name, (i, j) in FIELDS.items():
            m[i][j] = m[j][i] = self.values[name]
        return m

    def render(self) -> str:
        """The assembled matrix, or the field names when it is symbolic."""
        rows = self.rows
        if rows is None:
            return ("[[I_11, I_21, I_31], [I_21, I_22, I_32], "
                    "[I_31, I_32, I_33]] (not numerically known)")
        return "[" + ", ".join(
            "[" + ", ".join(f"{x:g}" for x in row) + "]" for row in rows) + "]"


def tensors(model, environment=None) -> list[Tensor]:
    """Every recognised inertia tensor in the model, decided where possible.

    Recognition needs **all six** fields under one instance path and one
    declaring class. A class that declares three of them is not this idiom and
    keeps the ordinary scalar rule, because suppressing a rule on a partial
    match is how a real defect goes quiet.
    """
    groups: dict[tuple[str, str], Tensor] = {}
    matrices: dict[tuple[str, str], object] = {}

    for variable in model.variables:
        name = variable.name
        owner, _, leaf = name.rpartition(".")
        contract = getattr(variable, "contract", None)
        declaring = getattr(contract, "declared_in", None) or ""
        if leaf in FIELDS:
            found = groups.setdefault((owner, declaring),
                                      Tensor(owner=owner,
                                             declaring_class=declaring))
            found.fields[leaf] = variable
        elif leaf == MATRIX:
            matrices[(owner, declaring)] = variable

    complete = []
    taken = set()
    for key, tensor in groups.items():
        if set(tensor.fields) != set(FIELDS):
            continue
        tensor.matrix = matrices.get(key)
        if tensor.matrix is not None:
            taken.add(tensor.matrix.id)
        _decide(tensor, environment)
        complete.append(tensor)

    # A tensor declared only as a matrix. `Parts.BodyBox` computes its inertia
    # from the box geometry and never declares the six fields, so the group
    # above does not see it --- and the scalar rule compared a 3x3 with zero
    # and reported `boxBody1.I > 0`, which is not a proposition. It is the same
    # subject and gets the same treatment.
    for key, variable in matrices.items():
        if variable.id in taken:
            continue
        if getattr(variable, "scalar_count", 1) != 9:
            continue
        if getattr(variable, "physical_quantity", None) not in TENSOR_QUANTITIES:
            continue
        owner, declaring = key
        tensor = Tensor(owner=owner, declaring_class=declaring,
                        matrix=variable)
        tensor.verdict = Verdict.UNKNOWN
        tensor.reason = (f"`{variable.name}` is declared as a 3x3 tensor whose "
                         f"entries this analysis cannot evaluate, so neither "
                         f"its validity nor its invalidity is claimed")
        complete.append(tensor)
    return complete


def _decide(tensor: Tensor, environment) -> None:
    for name, variable in tensor.fields.items():
        value = _value_of(variable, environment)
        if value is None:
            binding = getattr(variable, "binding", None)
            tensor.verdict = Verdict.UNKNOWN
            tensor.reason = (
                f"`{variable.name}` is bound to `{binding}`, which this "
                f"analysis cannot evaluate, so the tensor cannot be assembled"
                if binding is not None else
                f"`{variable.name}` has no value this analysis can resolve, "
                f"so the tensor cannot be assembled")
            return
        if not math.isfinite(value):
            tensor.values[name] = value
            tensor.verdict = Verdict.INVALID
            tensor.reason = f"`{tensor.owner}.{name}` is not finite ({value})"
            return
        tensor.values[name] = value

    rows = tensor.rows
    scale = max((abs(x) for row in rows for x in row), default=0.0)
    tolerance = 1e-12 * scale
    failing = _failed_minor(rows, tolerance)
    tensor.eigenvalues = eigenvalues(rows)
    tensor.realizable = _realizable(tensor.eigenvalues, tolerance)
    if failing is None:
        tensor.verdict = Verdict.VALID
        tensor.reason = ("the assembled tensor is symmetric positive "
                         "semidefinite")
        return
    label, value = failing
    tensor.verdict = Verdict.INVALID
    tensor.failed_minor = label
    tensor.reason = (f"the assembled tensor is not positive semidefinite: "
                     f"{label} = {value:g}, which must be >= 0")


def _value_of(variable, environment) -> float | None:
    """The declared value, following bindings as far as they go."""
    if environment is not None:
        from ..divisor.witness import Unevaluable, evaluate

        binding = getattr(variable, "binding", None)
        if binding is not None:
            try:
                return float(evaluate(binding, environment, {}))
            except (Unevaluable, ZeroDivisionError, OverflowError, ValueError):
                pass
        value = environment.values.get(variable.id)
        if value is not None:
            return float(value)

    from .engine import constant_value

    value = constant_value(getattr(variable, "binding", None))
    try:
        return None if value is None else float(value)
    except (TypeError, ValueError):
        return None


def _failed_minor(m, tolerance: float):
    """The first principal minor that is negative, or None.

    **All** principal minors, not only the leading ones. Sylvester's criterion
    with leading minors alone decides positive *definiteness*; semidefiniteness
    needs every principal minor, and `[[0,0,0],[0,1,0],[0,0,-1]]` is the
    standard counterexample — its leading minors are 0, 0, 0.
    """
    order = ["I_11", "I_22", "I_33"]
    for name, index in zip(order, range(3)):
        if m[index][index] < -tolerance:
            return (name, m[index][index])

    pairs = (((0, 1), "I_11*I_22 - I_21^2"),
             ((0, 2), "I_11*I_33 - I_31^2"),
             ((1, 2), "I_22*I_33 - I_32^2"))
    for (i, j), label in pairs:
        minor = m[i][i] * m[j][j] - m[i][j] * m[j][i]
        if minor < -tolerance:
            return (label, minor)

    determinant = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                   - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                   + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    if determinant < -tolerance:
        return ("det(I)", determinant)
    return None


def eigenvalues(m) -> tuple[float, float, float]:
    """The three eigenvalues of a symmetric 3x3 matrix, ascending.

    Closed form (Smith, 1961) rather than an iterative solver, so this needs no
    numerical library: a symmetric 3x3 has a real characteristic cubic whose
    roots are expressible in trigonometric form.
    """
    p1 = m[0][1] ** 2 + m[0][2] ** 2 + m[1][2] ** 2
    trace = m[0][0] + m[1][1] + m[2][2]
    if p1 == 0.0:
        return tuple(sorted((m[0][0], m[1][1], m[2][2])))

    q = trace / 3.0
    p2 = ((m[0][0] - q) ** 2 + (m[1][1] - q) ** 2 + (m[2][2] - q) ** 2
          + 2.0 * p1)
    p = math.sqrt(p2 / 6.0)
    if p == 0.0:
        return (q, q, q)

    b = [[(m[i][j] - (q if i == j else 0.0)) / p for j in range(3)]
         for i in range(3)]
    determinant = (b[0][0] * (b[1][1] * b[2][2] - b[1][2] * b[2][1])
                   - b[0][1] * (b[1][0] * b[2][2] - b[1][2] * b[2][0])
                   + b[0][2] * (b[1][0] * b[2][1] - b[1][1] * b[2][0]))
    r = max(-1.0, min(1.0, determinant / 2.0))
    phi = math.acos(r) / 3.0

    high = q + 2.0 * p * math.cos(phi)
    low = q + 2.0 * p * math.cos(phi + 2.0 * math.pi / 3.0)
    middle = trace - high - low
    return tuple(sorted((low, middle, high)))


def _realizable(values, tolerance: float) -> bool:
    """Whether the principal moments could belong to a rigid body.

    For any rigid body each principal moment is at most the sum of the other
    two: the triangle inequality on the mass distribution. A positive
    semidefinite tensor that violates it is mathematically fine and physically
    impossible, which is a weaker observation than a failed PSD check and is
    reported as one.
    """
    a, b, c = sorted(values)
    return c <= a + b + tolerance
