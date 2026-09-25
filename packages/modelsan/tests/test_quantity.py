"""QuantitySan: a declaration whose unit disagrees with its quantity.

The cases here are the ones the MSL corpus actually produced, named after what
they assert rather than after an issue number, so that a reader who has never
opened the tracker can still tell what is being claimed.

The false-positive cases matter as much as the detections. Two of them are
mistakes this sanitizer made on its first sweep of the library and no longer
makes; leaving them unnamed would let a later refactor reintroduce them.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parents[2] / "rumoca-bitcode"),
                str(Path(__file__).resolve().parents[1])]

from modelsan.analysis.context import AnalysisContext          # noqa: E402
from modelsan.sanitizers.quantity import QuantitySan, is_si_coherent  # noqa: E402
from rumoca_bitcode.model import BinaryOp, Literal, VariableRef  # noqa: E402

#: The expression classes are the real ones. Doubles were tried first and
#: silently matched nothing: `_value_dimension` dispatches on `isinstance`, so
#: a stand-in produces an empty result that reads exactly like a clean model.
_next_id = iter(range(1000, 9999))


class Var:
    """Enough of a DAE variable for a declaration-level check."""

    def __init__(self, id, name, quantity=None, unit=None, binding=None,
                 from_source=True):
        self.id, self.name = id, name
        self.physical_quantity, self.unit = quantity, unit
        self.binding, self.from_source = binding, from_source
        self.source = None
        self.is_derivative = False


def Ref(variable):
    return VariableRef(next(_next_id), None, "coordinate", variable)


def Num(value):
    """A numeric literal, which in a *binding* is a pure number."""
    return Literal(next(_next_id), None, "real", value)


def Bin(op, lhs, rhs):
    return BinaryOp(next(_next_id), None, op, lhs, rhs)


class Model:
    def __init__(self, variables):
        self.variables = variables
        self.equations = self.initial_equations = self.expressions = []
        self.events = []


def run(*variables):
    model = Model(list(variables))
    return QuantitySan().analyze(model, AnalysisContext(model))


def kinds(findings):
    return sorted(f.kind for f in findings)


# ── the mechanism the corpus is full of ──────────────────────────────────────


def test_a_capacitance_bound_to_a_reciprocal_inductance_is_a_conflict():
    """Modelica.Electrical.Analog.Examples.CauerLowPassAnalog, upstream #4079.

    `parameter SI.Capacitance c2 = 1/(1.704992^2*l1)` with `l1` an inductance.
    The declaration is internally consistent and the equations are silent; the
    disagreement is between the declaration and its own binding.
    """
    l1 = Var(1, "l1", "Inductance", "H", Num(1.304))
    c2 = Var(2, "c2", "Capacitance", "F", Bin(
        "divide", Num(1), Bin("multiply", Num(2.9), Ref(l1))))
    findings = run(l1, c2)
    assert kinds(findings) == ["binding-unit-conflict"], kinds(findings)
    evidence = findings[0].evidence
    assert evidence["variable"] == "c2"
    assert evidence["declared_dimension"] != evidence["binding_dimension"]
    assert "l1[H]" in evidence["reads"]


def test_a_resistance_bound_to_a_voltage_over_a_bare_number_is_a_conflict():
    """Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive.

    `R = 0.05*dcpmData.VaNominal/1000`, where the 1000 is an unstated current.
    Not in the upstream tracker; found by this check on its first sweep.
    """
    v = Var(1, "VaNominal", "Voltage", "V", Num(100.0))
    r = Var(2, "R", "Resistance", "Ohm", Bin(
        "divide", Bin("multiply", Num(0.05), Ref(v)), Num(1000)))
    assert kinds(run(v, r)) == ["binding-unit-conflict"]


def test_one_quantity_declared_with_two_dimensions_is_a_conflict():
    findings = run(Var(1, "a", "Energy", "J"), Var(2, "b", "Energy", "kg"))
    assert kinds(findings) == ["quantity-unit-dimension-conflict"]
    assert findings[0].evidence["quantity"] == "Energy"


# ── what must stay silent ────────────────────────────────────────────────────


def test_a_literal_binding_on_a_dimensional_parameter_is_not_a_conflict():
    """How every parameter in the library is written.

    A bare number carries no dimension, so comparing it to the declaration
    would report the entire standard library.
    """
    assert run(Var(1, "l1", "Inductance", "H", Num(1.304))) == []


def test_apparent_power_in_volt_amperes_is_not_a_non_si_unit():
    """`V.A` is watts spelled compositely, and is how MSL writes apparent power.

    The first version of this check compared whole unit strings against a set
    of atomic symbols and reported every `ApparentPower` declaration in
    Modelica.Electrical.PowerConverters.
    """
    assert run(Var(1, "P", "Power", "W"), Var(2, "S", "Power", "V.A")) == []


def test_a_dimensionless_value_without_a_quantity_is_not_reported():
    """24 of these in one MultiBody model were direction-vector components."""
    assert run(Var(1, "n", None, "1"), Var(2, "n_x", None, "1")) == []


def test_a_generated_variable_is_not_judged():
    """Its attributes were inferred by the compiler, so a disagreement among
    them is this project's defect, not the library's."""
    assert run(Var(1, "tmp", "Energy", "J", from_source=False),
               Var(2, "tmp2", "Energy", "kg", from_source=False)) == []


def test_an_unrecognised_unit_yields_no_claim():
    assert run(Var(1, "a", "Odd", "furlong"), Var(2, "b", "Odd", "J")) == []


# ── the coherence predicate itself ───────────────────────────────────────────


def test_coherence_is_decided_per_symbol_not_per_string():
    assert is_si_coherent("V.A") and is_si_coherent("N.m/s")
    assert is_si_coherent("1") and is_si_coherent("Ohm")
    assert not is_si_coherent("deg") and not is_si_coherent("degC")
    assert not is_si_coherent("eV") and not is_si_coherent("")


def test_a_dimensional_unit_without_a_quantity_is_reported_once_per_unit():
    """Grouped per unit: a missing quantity on a type is missing on every
    variable of that type, and 300 findings for one omission is noise."""
    findings = run(Var(1, "a", None, "m3/s2"), Var(2, "b", None, "m3/s2"))
    assert kinds(findings) == ["quantity-missing"]
    assert findings[0].evidence["count"] == 2


def test_a_folded_physical_constant_does_not_look_dimensionless():
    """TOOLBUG-028. MSL's `mu_r = B_r/(mu_0*H_cB)` is correct and must be silent.

    `mu_0` reaches the artifact as the bare literal 1.25663706212e-06 with its
    `H/m` discarded, which made three correct FluxTubes declarations look
    dimensionally inconsistent on the first full-corpus sweep. The unit is
    recovered by exact value from the library's own constants.
    """
    b_r = Var(1, "B_r", "MagneticFluxDensity", "T", Num(1.0))
    h_cb = Var(2, "H_cB", "MagneticFieldStrength", "A/m", Num(720000.0))
    mu_r = Var(3, "mu_r", "RelativePermeability", "1", Bin(
        "divide", Ref(b_r),
        Bin("multiply", Num(1.25663706212e-06), Ref(h_cb))))
    assert run(b_r, h_cb, mu_r) == []


def test_an_ordinary_number_is_still_dimensionless():
    """The recovery speaks only on an exact match, so `1000` stays a number and
    the DCPM_Drive finding above is unaffected."""
    from modelsan.units.constants import dimension_of_literal
    assert dimension_of_literal(1000.0) is None
    assert dimension_of_literal(1.25663706212e-06) is not None
