"""The library-scope unit audit, over type declarations rather than models.

`QuantitySan` reads a compiled model and therefore only sees quantities some
model instantiates. These checks read `Units.mo` directly, because the defects
they find are in declarations that may have no user yet — which is exactly why
no model-driven analysis had found them.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "packages" / "rumoca-bitcode"),
                str(ROOT / "packages" / "modelsan")]

_spec = importlib.util.spec_from_file_location(
    "library_audit", ROOT / "tools" / "units" / "library_audit.py")
library_audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(library_audit)

audit, declarations = library_audit.audit, library_audit.declarations


def checks(findings, name):
    return [f for f in findings if f["check"] == name]


def test_a_quantity_declared_in_two_dimensions_is_high():
    source = '''
    type Energy = Real (final quantity="Energy", final unit="J");
    type Wrong  = Real (final quantity="Energy", final unit="kg");
    '''
    found = checks(audit(source), "quantity-maps-to-two-dimensions")
    assert len(found) == 1 and found[0]["severity"] == "high"
    assert found[0]["quantity"] == "Energy"


def test_a_non_si_unit_beside_the_si_one_is_reported_separately():
    """Upstream #3158: `Angle` is declared in both radians and degrees.

    Dimensionally these agree — degrees are dimensionless too — so this is not
    a conflict. It is reported at low severity as a question about the
    interface, which is what the intent policy requires of a claim the source
    does not settle.
    """
    source = '''
    type Angle     = Real (final quantity="Angle", final unit="rad");
    type Angle_deg = Real (final quantity="Angle", final unit="deg");
    '''
    findings = audit(source)
    assert checks(findings, "quantity-maps-to-two-dimensions") == []
    found = checks(findings, "quantity-non-si-unit")
    assert len(found) == 1 and found[0]["severity"] == "low"
    assert found[0]["non_si"] == {"deg": ["Angle_deg"]}


def test_volt_amperes_beside_watts_is_not_a_non_si_unit():
    """`V.A` is watts spelled compositely, and is how apparent power is
    conventionally written. Reporting it would report a convention."""
    source = '''
    type Power         = Real (final quantity="Power", final unit="W");
    type ApparentPower = Real (final quantity="Power", final unit="V.A");
    '''
    assert checks(audit(source), "quantity-non-si-unit") == []


def test_a_unit_with_no_quantity_is_graded_by_whether_it_has_a_dimension():
    """Upstream #4086. A dimensionless ratio with no quantity risks nothing;
    a pressure with no quantity cannot be matched by any rule keyed on one."""
    source = '''
    type Stress  = Real (final unit="Pa");
    type PerUnit = Real (final unit="1");
    '''
    found = {f["type"]: f["severity"]
             for f in checks(audit(source), "unit-without-quantity")}
    assert found == {"Stress": "medium", "PerUnit": "low"}


def test_a_display_unit_is_not_read_as_the_unit():
    source = 'type T = Real (final quantity="Angle", final unit="rad", displayUnit="deg");'
    assert [d for d in declarations(source)] == [("T", "Angle", "rad")]


def test_the_shipped_library_reproduces_the_open_issues_it_is_known_to_have():
    """Against real MSL, when the corpus is present.

    Named rather than asserted loosely: these are the counts the upstream
    issues state, and a change in them is either a library update or a
    regression in this audit. Either way somebody should look.
    """
    units = library_audit.DEFAULT_UNITS
    if not units.is_file():
        import pytest
        pytest.skip("MSL corpus not present")
    findings = audit(units.read_text())

    missing = checks(findings, "unit-without-quantity")
    assert len(missing) == 11, [f["type"] for f in missing]          # #4086

    non_si = {f["quantity"] for f in checks(findings, "quantity-non-si-unit")}
    assert "Angle" in non_si                                          # #3158
    assert "Energy" in non_si                                         # #4062
