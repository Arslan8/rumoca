#!/usr/bin/env python3
"""PhysicalSan: cross-domain invariants, and the properties that keep it general.

The point of these is not that a negative mass is caught — that is easy. It is
that the *engine* catches it without knowing what mass is, that a new domain
needs no core edit, and that matching does not fall back on variable names.

Run: python3 packages/modelsan/tests/test_physical.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "packages/rumoca-bitcode"), str(ROOT / "packages/modelsan")]

from modelsan.analysis import AnalysisContext                        # noqa: E402
from modelsan.findings.signature import attach                       # noqa: E402
from modelsan.physical.domains import BUILTIN                        # noqa: E402
from modelsan.physical.engine import PhysicalEngine, constant_value  # noqa: E402
from modelsan.physical.invariant import (                            # noqa: E402
    Comparison, Domain, Enforcement, Predicate, Term,
)
from modelsan.physical.matching import Confidence, match_variable    # noqa: E402
from modelsan.physical.rules import QuantityRule, RulePack, RuleRegistry  # noqa: E402
from modelsan.sanitizers import PhysicalSan                          # noqa: E402

FAILURES: list[str] = []


def check(condition: bool, label: str) -> None:
    print(f"{'PASS' if condition else 'FAIL'}  {label}")
    if not condition:
        FAILURES.append(label)


class FakeVar:
    """A variable double carrying only the metadata matching may use."""

    def __init__(self, id, name, quantity=None, unit=None, parameter=True,
                 binding=None, minimum=None):
        self.id, self.name = id, name
        self.physical_quantity, self.unit = quantity, unit
        self.is_parameter = parameter
        self.quantity = None          # connector role
        self.binding = binding
        self.start = self.maximum = None
        self.minimum = minimum
        self.source = None
        self.is_state = not parameter


class Lit:
    def __init__(self, value): self.value = value


class Neg:
    """`-x` as the DAE represents it: a unary operation, not a literal."""

    def __init__(self, inner): self.op, self.operand = "negate", inner


class FakeModel:
    def __init__(self, variables):
        self.variables = variables
        self.equations = self.initial_equations = self.expressions = self.events = []


# ── the representation is domain-independent ─────────────────────────────────


def test_domain_is_open():
    print("\n== a new domain needs no core edit ==")
    aero = Domain("aerodynamic")
    check(aero.value == "aerodynamic", "an unlisted domain is constructible")
    check(aero == Domain("aerodynamic"), "domains compare by value")
    pack = RulePack(domain=aero, rules=[QuantityRule(
        rule_id="aero.cd.positive", domain=aero,
        quantities=frozenset({"DragCoefficient"}), op=Comparison.GT, bound=0.0,
        origin="drag opposes motion")])
    registry = RuleRegistry()
    registry.register(pack)
    engine = PhysicalEngine(registry)
    model = FakeModel([FakeVar(0, "wing.cd", quantity="DragCoefficient",
                               binding=Neg(Lit(0.3)))])
    analysis = engine.analyze(model)
    check(len(analysis.static_violations) == 1,
          "the engine enforces a domain it has never heard of")
    check(analysis.static_violations[0].invariant.domain == aero,
          "the finding carries the new domain")


def test_predicate_supports_multiple_variables():
    print("\n== predicates are not limited to `x > constant` ==")
    total = Term.total((Term.variable(1, "i1"), Term.variable(2, "i2")))
    predicate = Predicate(left=total, op=Comparison.GE, right=Term.constant(0.0))
    check(set(predicate.variables()) == {1, 2}, "a term spans several variables")
    check(predicate.holds({1: 2.0, 2: -1.0}) is True, "multi-variable evaluation works")
    check(predicate.holds({1: -2.0, 2: -1.0}) is False, "and can be false")
    check(predicate.holds({1: 1.0}) is None,
          "an undetermined term yields None, not a guess")


# ── matching does not use names ──────────────────────────────────────────────


def test_matching_ignores_names():
    print("\n== matching is semantic, not lexical ==")
    quantities, units = frozenset({"Resistance"}), frozenset({"Ohm"})

    named_r = FakeVar(0, "R", quantity=None, unit=None)
    check(match_variable(named_r, quantities, units).confidence is Confidence.NONE,
          "a variable called R with no metadata does not match")

    declared = FakeVar(1, "somethingElse", quantity="Resistance", unit="Ohm")
    check(match_variable(declared, quantities, units).confidence
          is Confidence.QUANTITY_AND_UNIT,
          "a differently-named variable with the right quantity does match")

    unit_only = FakeVar(2, "z", quantity=None, unit="Ohm")
    got = match_variable(unit_only, quantities, units)
    check(got.confidence is Confidence.UNIT_ONLY, "unit alone is a weak match")
    rule = QuantityRule(rule_id="t", domain=Domain("electrical"),
                        quantities=quantities, units=units,
                        op=Comparison.GT, bound=0.0, origin="")
    check(rule.applies(unit_only) is None,
          "and a unit-only match is rejected: Ohm does not imply positivity")


# ── the negative-literal folding bug ─────────────────────────────────────────


def test_negative_declarations_are_read():
    print("\n== negative declarations are values, not absences ==")
    # `-2.0` reaches the DAE as a unary minus over a literal. Reading only bare
    # literals silently missed every negative declaration — the exact case this
    # sanitizer exists for.
    check(constant_value(Lit(3.0)) == 3.0, "a literal folds")
    check(constant_value(Neg(Lit(2.0))) == -2.0, "a negated literal folds")
    check(constant_value(None) is None, "an absent expression is not a value")

    class Ref:
        op = None
    check(constant_value(Ref()) is None,
          "a non-constant expression is undecided, not assumed")


# ── the model's own bound is respected ───────────────────────────────────────


def test_declared_bound_suppresses_the_invariant():
    print("\n== an already-guarded declaration is not reported ==")
    registry = RuleRegistry()
    for pack in BUILTIN:
        registry.register(pack)
    engine = PhysicalEngine(registry)

    guarded = FakeVar(0, "c.C", quantity="Capacitance", unit="F",
                      binding=Lit(1e-6), minimum=Lit(1e-9))
    exposed = FakeVar(1, "d.C", quantity="Capacitance", unit="F", binding=Lit(1e-6))
    left = {i.variable_ids[0] for i in engine.unbounded(FakeModel([guarded, exposed]))}
    check(1 in left, "a declaration with no bound is reported as unenforced")
    check(0 not in left,
          "a declaration whose own min already implies the invariant is not")


# ── end to end, four domains, valid and invalid ──────────────────────────────


def test_cross_domain_end_to_end():
    print("\n== four domains, valid and invalid ==")
    san = PhysicalSan()
    check(len(san.registry.domains) >= 4,
          f"at least four domains registered ({[d.value for d in san.registry.domains]})")

    cases = [
        ("electrical ok", [FakeVar(0, "r.R", "Resistance", "Ohm", binding=Lit(100.0))], 0),
        ("electrical bad", [FakeVar(0, "r.R", "Resistance", "Ohm", binding=Neg(Lit(100.0)))], 1),
        ("mechanical ok", [FakeVar(0, "b.m", "Mass", "kg", binding=Lit(2.0))], 0),
        ("mechanical bad", [FakeVar(0, "b.m", "Mass", "kg", binding=Neg(Lit(2.0)))], 1),
        ("thermal ok", [FakeVar(0, "h.C", "HeatCapacity", "J/K", binding=Lit(100.0))], 0),
        ("thermal bad", [FakeVar(0, "h.C", "HeatCapacity", "J/K", binding=Neg(Lit(100.0)))], 1),
        ("fluid ok", [FakeVar(0, "p.rho", "Density", "kg/m3", binding=Lit(998.0))], 0),
        ("fluid bad", [FakeVar(0, "p.rho", "Density", "kg/m3", binding=Neg(Lit(998.0)))], 1),
    ]
    for label, variables, expected in cases:
        model = FakeModel(variables)
        findings = attach(san.analyze(model, AnalysisContext(model)))
        violations = [f for f in findings if f.kind == "physical-invariant-violated"]
        check(len(violations) == expected, f"{label}: {len(violations)} violation(s)")


def test_provenance_is_preserved():
    print("\n== both provenances travel with the finding ==")
    san = PhysicalSan()
    model = FakeModel([FakeVar(0, "b.m", "Mass", "kg", binding=Neg(Lit(2.0)))])
    finding = attach(san.analyze(model, AnalysisContext(model)))[0]
    evidence = finding.evidence
    check(evidence["rule"] == "mech.mass.positive", "the rule id is recorded")
    check("m*a = f" in evidence["rule_origin"], "the physical justification is recorded")
    check(evidence["matched_by"]["quantity"] == "Mass",
          "the evidence that matched the rule is recorded")
    check(finding.canonical_anchors[0].dae_id == 0,
          "the finding anchors to the DAE variable")


def main() -> int:
    test_domain_is_open()
    test_predicate_supports_multiple_variables()
    test_matching_ignores_names()
    test_negative_declarations_are_read()
    test_declared_bound_suppresses_the_invariant()
    test_cross_domain_end_to_end()
    test_provenance_is_preserved()
    print(f"\n{'ALL PASS' if not FAILURES else str(len(FAILURES)) + ' FAILED'}")
    for failure in FAILURES:
        print(f"  - {failure}")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
