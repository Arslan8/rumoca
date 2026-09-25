"""QuantitySan — a declaration whose `unit` disagrees with its `quantity`.

1. Bug class    `quantity="LogarithmicDecrement"` with `unit="1/S"`, where `S`
                is siemens: the declared unit is ohms for a quantity that is a
                ratio. 21 open MSL issues share this mechanism, the largest
                recurring cluster in the tracker.
2. Overlap      none with `DimensionSan`. That one reads *equations* and asks
                whether two operands can be added. This reads *declarations*
                and asks whether one declaration is self-consistent. A model
                with no equations at all still has this defect.
3. Signal       static: two declarations name one `quantity` and carry units of
                different SI dimension, or a declaration carries a unit and no
                quantity at all.
4. Needs        `unit` and `physical_quantity` on variables. Nothing at runtime.
5. Transform    no.
6. Fuzzing      none — there is no value to perturb.
7. Signature    the quantity and the disagreeing units.

**Why the reference is the corpus and not a table in this file.** MLS §4.8
makes `quantity` the semantic identity of what a variable measures, so within
one library the map quantity → dimension must be a function. That is checkable
without knowing which unit is *correct*: two declarations that disagree prove a
defect between them even when nothing here knows which one to fix. A hardcoded
"correct unit per quantity" table would be one more record that silently falls
behind the library — the exact failure this project keeps meeting.

**Conservative by construction**, in the same way `DimensionSan` is:

- a unit the parser does not recognise yields *no* dimensional claim;
- a variable the compiler generated is skipped, because its unit was inferred
  rather than written by anyone;
- units that differ in spelling but agree in dimension are not a conflict.
  `W` and `V.A` are both watts dimensionally, and apparent power is
  conventionally written `V.A`; reporting that would be reporting a convention.
"""

from __future__ import annotations

import collections
import re

from ..analysis.context import AnalysisContext
from ..findings.finding import Finding, Severity
from ..findings.location import locate
from ..instrumentation.capability import Capability
from ..runtime.anchors import CanonicalAnchor, EntityKind
from ..dae import BinaryOp, Literal, UnaryOp, ops
from ..units.constants import dimension_of_literal
from ..units.dimension import ONE, Dimension, parse

#: SI symbols that are coherent: the base units and the named derived units
#: that are products of them with factor 1.
COHERENT_SYMBOLS = frozenset({
    "1", "m", "kg", "g", "s", "A", "K", "mol", "cd", "rad", "sr",
    "Hz", "N", "Pa", "J", "W", "C", "V", "F", "Ohm", "S", "Wb", "T", "H",
    "lm", "lx", "Bq", "Gy", "Sv", "kat",
})

#: Splits a unit string into its symbols, dropping exponents and separators.
_SYMBOL = re.compile(r"[A-Za-z]+")


def is_si_coherent(unit: str) -> bool:
    """Whether every symbol in a unit string is an SI-coherent one.

    Tested per symbol rather than on the whole string, because a unit may be a
    legitimate composite: `V.A` is watts spelled as volt-amperes, which is how
    apparent power is conventionally written and is *not* a non-SI unit. An
    earlier version compared the whole string against a set and reported every
    `ApparentPower` declaration in the library.
    """
    text = (unit or "").strip()
    if not text:
        return False
    if text == "1":            # the coherent unit of a dimensionless quantity
        return True
    symbols = _SYMBOL.findall(text)
    return bool(symbols) and all(s in COHERENT_SYMBOLS for s in symbols)


def _declarations(model):
    """Source-written variables carrying a unit, a quantity, or both.

    Generated variables are excluded: their attributes were inferred by the
    compiler, so a disagreement among them is this tool's defect to fix, not
    the library's.
    """
    for variable in model.variables:
        if not getattr(variable, "from_source", True):
            continue
        unit = getattr(variable, "unit", None)
        quantity = getattr(variable, "physical_quantity", None)
        if unit or quantity:
            yield variable, unit, quantity


class QuantitySan:
    name = "quantity"

    requires = {"static": frozenset({Capability.CANONICAL_MODEL})}

    def analyze(self, model, context: AnalysisContext) -> list[Finding]:
        findings = []
        findings += self._conflicting_units(model)
        findings += self._binding_conflicts(model)
        findings += self._unit_without_quantity(model)
        return findings

    def _binding_conflicts(self, model) -> list[Finding]:
        """A declared unit that its own binding expression contradicts.

        `parameter SI.Capacitance c2 = 1/(1.704992^2*l1)` with `l1` an
        inductance: the declaration promises farads and the binding computes
        reciprocal henries. Neither `DimensionSan` nor the unit cross-check
        above sees it, because it is not an equation and the declaration is
        internally consistent — the disagreement is between a declaration and
        its own value.
        """
        findings = []
        for variable, unit, _quantity in _declarations(model):
            declared = parse(unit)
            binding = getattr(variable, "binding", None)
            if declared is None or binding is None:
                continue
            # A bare number bound to a dimensional parameter is how every
            # parameter in the library is written. Only a binding that reads
            # another *declared* quantity can contradict anything.
            if not _reads_a_dimensioned_variable(binding):
                continue
            actual = _value_dimension(binding)
            if actual is None or actual == declared:
                continue
            findings.append(Finding(
                sanitizer=self.name,
                kind="binding-unit-conflict",
                severity=Severity.HIGH,
                canonical_anchors=[
                    CanonicalAnchor(EntityKind.VARIABLE, variable.id, variable.name)],
                source_locations=locate(variable),
                evidence={
                    "variable": variable.name,
                    "declared_unit": unit,
                    "declared_dimension": str(declared),
                    "binding": repr(binding)[:140],
                    "binding_dimension": str(actual),
                    "reads": ", ".join(
                        f"{v.name}[{v.unit}]"
                        for v in _dimensioned_reads(binding)[:5]),
                    "note": "the declaration promises one dimension and its own "
                            "binding expression computes another; no choice of "
                            "values reconciles them",
                },
                signature=f"binding-unit:{variable.name}:"
                          f"{declared}!={actual}",
            ))
        return findings

    def _conflicting_units(self, model) -> list[Finding]:
        """One `quantity`, two units. Dimensional disagreement is the defect."""
        by_quantity: dict[str, dict[str, list]] = collections.defaultdict(
            lambda: collections.defaultdict(list))
        for variable, unit, quantity in _declarations(model):
            if unit and quantity:
                by_quantity[quantity][unit].append(variable)

        findings = []
        for quantity, units in sorted(by_quantity.items()):
            if len(units) < 2:
                continue
            dimensions = {unit: parse(unit) for unit in units}
            # An unrecognised unit makes no claim, so it cannot disagree.
            known = {u: d for u, d in dimensions.items() if d is not None}
            if len(known) < 2:
                continue
            distinct = {str(d) for d in known.values()}

            if len(distinct) > 1:
                findings.append(self._conflict(quantity, units, known))
            else:
                finding = self._non_si(quantity, units)
                if finding is not None:
                    findings.append(finding)
        return findings

    def _conflict(self, quantity, units, known) -> Finding:
        witnesses = [v for group in units.values() for v in group][:4]
        return Finding(
            sanitizer=self.name,
            kind="quantity-unit-dimension-conflict",
            severity=Severity.HIGH,
            canonical_anchors=[
                CanonicalAnchor(EntityKind.VARIABLE, v.id, v.name) for v in witnesses],
            source_locations=[loc for v in witnesses for loc in locate(v)][:4],
            evidence={
                "quantity": quantity,
                "units": ", ".join(f"{u} [{known[u]}]" for u in sorted(known)),
                "declarations": ", ".join(
                    f"{v.name}={v.unit}" for v in witnesses),
                "note": "one quantity is declared with units of different SI "
                        "dimension; MLS 4.8 makes quantity the identity of "
                        "what is measured, so at most one of these can be right",
            },
            signature=f"quantity-conflict:{quantity}:"
                      f"{','.join(sorted(str(d) for d in known.values()))}",
        )

    def _non_si(self, quantity, units) -> Finding | None:
        """Same dimension, different spellings, one of them SI-coherent.

        Reported below the dimensional conflict because it is a convention
        question, not an arithmetic one: `deg` is a real angle, just not the SI
        one, and a model using it is wrong only about its interface.
        """
        coherent = sorted(u for u in units if is_si_coherent(u))
        other = sorted(u for u in units if not is_si_coherent(u))
        if not coherent or not other:
            return None
        witnesses = [v for u in other for v in units[u]][:4]
        return Finding(
            sanitizer=self.name,
            kind="quantity-unit-not-si-coherent",
            severity=Severity.LOW,
            canonical_anchors=[
                CanonicalAnchor(EntityKind.VARIABLE, v.id, v.name) for v in witnesses],
            source_locations=[loc for v in witnesses for loc in locate(v)][:4],
            evidence={
                "quantity": quantity,
                "si_unit": ", ".join(coherent),
                "also_declared": ", ".join(other),
                "declarations": ", ".join(f"{v.name}={v.unit}" for v in witnesses),
                "note": "the same quantity is declared both in its SI unit and "
                        "in another of the same dimension; the non-SI spelling "
                        "is a question about the interface, not an error in it",
            },
            signature=f"quantity-non-si:{quantity}:{','.join(other)}",
        )

    def _unit_without_quantity(self, model) -> list[Finding]:
        """A unit with no quantity: measurable, but not identified.

        Grouped into one finding per unit rather than one per variable. A
        library that omits the quantity on a type omits it on every variable of
        that type, and 300 findings for one missing attribute is noise.
        """
        by_unit: dict[str, list] = collections.defaultdict(list)
        for variable, unit, quantity in _declarations(model):
            dimension = parse(unit) if unit else None
            # A dimensionless value with no quantity carries no dimensional
            # risk and is ordinary throughout the library — 24 of these in one
            # MultiBody model were direction-vector components. Naming a
            # quantity for them is style, and this is not a style checker.
            if unit and not quantity and dimension is not None \
                    and not dimension.dimensionless:
                by_unit[unit].append(variable)

        findings = []
        for unit, variables in sorted(by_unit.items()):
            witnesses = variables[:4]
            findings.append(Finding(
                sanitizer=self.name,
                kind="quantity-missing",
                severity=Severity.LOW,
                canonical_anchors=[
                    CanonicalAnchor(EntityKind.VARIABLE, v.id, v.name)
                    for v in witnesses],
                source_locations=[loc for v in witnesses for loc in locate(v)][:4],
                evidence={
                    "unit": unit,
                    "count": len(variables),
                    "declarations": ", ".join(v.name for v in witnesses),
                    "note": "a unit is declared without a quantity, so nothing "
                            "states what is being measured and no rule keyed on "
                            "quantity can apply to it",
                },
                signature=f"quantity-missing:{unit}",
            ))
        return findings


def _value_dimension(expression) -> Dimension | None:
    """The dimension of a *value* expression, or None where it is not settled.

    This differs from `DimensionSan.dimension_of` in one deliberate way: there,
    a numeric literal makes *no claim*, because in `v/v_nominal + 1` the `1`
    takes its meaning from context. Here, in a binding, a literal is a pure
    number and therefore dimensionless — `2*l1` is henries and `1/l1` is
    reciprocal henries. Reusing the equation rule would silence every binding
    that contains a constant, which is nearly all of them.

    Unknown constructs still yield None, and None still propagates.
    """
    if expression is None:
        return None
    if isinstance(expression, Literal):
        # A folded physical constant reaches the artifact as a bare number with
        # its unit discarded (TOOLBUG-028). Treating it as dimensionless makes
        # correct code look wrong, so its unit is recovered by exact value.
        recovered = dimension_of_literal(expression.value)
        return recovered if recovered is not None else ONE

    variable = getattr(expression, "variable", None)
    if variable is not None:
        if getattr(expression, "is_derivative", False):
            base = parse(getattr(variable, "unit", None))
            return base / parse("s") if base is not None else None
        return parse(getattr(variable, "unit", None))

    if isinstance(expression, UnaryOp):
        return _value_dimension(expression.operand)

    if isinstance(expression, BinaryOp):
        left = _value_dimension(expression.lhs)
        right = _value_dimension(expression.rhs)
        if expression.op == ops.POWER:
            exponent = getattr(expression.rhs, "value", None)
            if left is None or not isinstance(exponent, (int, float)):
                return None
            # A non-integer power of a dimensional value has no SI dimension;
            # of a dimensionless one it is still dimensionless.
            if exponent != int(exponent):
                return ONE if left.dimensionless else None
            return left.power(int(exponent))
        if left is None or right is None:
            return None
        if expression.op == ops.MULTIPLY:
            return left * right
        if expression.op == ops.DIVIDE:
            return left / right
        if expression.op in (ops.ADD, ops.SUBTRACT):
            # Disagreeing operands are DimensionSan's finding, not this one.
            return left if left == right else None
    return None


def _dimensioned_reads(expression) -> list:
    """Variables the expression reads that carry a parseable unit."""
    found, stack = [], [expression]
    while stack:
        node = stack.pop()
        if node is None:
            continue
        variable = getattr(node, "variable", None)
        if variable is not None and parse(getattr(variable, "unit", None)) is not None:
            if not parse(variable.unit).dimensionless:
                found.append(variable)
        for attribute in ("lhs", "rhs", "operand"):
            child = getattr(node, attribute, None)
            if child is not None:
                stack.append(child)
    return found


def _reads_a_dimensioned_variable(expression) -> bool:
    return bool(_dimensioned_reads(expression))
