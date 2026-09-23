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
    """Record and *assert*.

    This module collected failures into a list for its `main()` and never
    asserted, so under pytest every test in it passed whatever it found. The
    list is kept for the standalone runner; the assertion is what makes the
    suite mean something.
    """
    print(f"{'PASS' if condition else 'FAIL'}  {label}")
    if not condition:
        FAILURES.append(label)
    assert condition, label


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


class Bin:
    def __init__(self, op, lhs, rhs): self.op, self.lhs, self.rhs = op, lhs, rhs


class Neg2:
    """A unary node with an explicit operator, for `not`."""

    def __init__(self, op, inner): self.op, self.operand = op, inner


class Cond:
    """`if c1 then v1 ... else fallback`, as the DAE represents it."""

    def __init__(self, branches, fallback):
        self.branches, self.fallback = branches, fallback


class Ref:
    """A reference to a variable, as the DAE spells it.

    ``kind`` follows the variable's variability, so `is_derivative` and
    `is_previous` — not the kind string — say whether this names a value or a
    trajectory.
    """

    def __init__(self, variable, derivative=False, previous=False):
        self.variable = variable
        self.is_derivative, self.is_previous = derivative, previous


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

    class Opaque:
        op = None
    check(constant_value(Opaque()) is None,
          "a non-constant expression is undecided, not assumed")


def test_parameter_chains_are_followed():
    print("\n== a value written in two steps is still a value ==")
    # `parameter Real scale = 2.5; parameter SI.Resistance R = -scale * 5;`
    # Rumoca folds this chain only when the result is an exact integer, so
    # reading bindings literally made the verdict depend on whether the
    # arithmetic happened to land on a whole number: `-2 * 5` was reported as
    # a violation and the identical `-2.5 * 5` only as an unbounded
    # declaration. Following the chain decides on the model instead.
    scale = FakeVar(1, "scale", binding=Lit(2.5))
    check(constant_value(Neg(Bin("multiply", Ref(scale), Lit(5)))) == -12.5,
          "a chain through a parameter folds")

    check(constant_value(Bin("power", Lit(3.0), Lit(2.0))) == 9.0,
          "a power over constants folds")

    # A state's trajectory is not its declaration, whatever it starts at.
    state = FakeVar(2, "x", parameter=False, binding=Lit(1.0))
    check(constant_value(Ref(state)) is None, "a non-parameter is not a value")
    check(constant_value(Ref(scale, derivative=True)) is None,
          "der(p) names a trajectory, not the declaration")
    check(constant_value(Ref(scale, previous=True)) is None,
          "pre(p) names a trajectory, not the declaration")

    # `start` is a solver's guess; treating one as fixed partway down a chain
    # would report a violation the declaration never commits to.
    guessed = FakeVar(3, "g")
    guessed.start = Lit(-4.0)
    check(constant_value(Ref(guessed)) is None,
          "a start part-way down a chain is not a fixed value")

    # A self-referential binding must terminate rather than recurse.
    loop = FakeVar(4, "loop")
    loop.binding = Bin("add", Ref(loop), Lit(1.0))
    check(constant_value(Ref(loop)) is None, "a cyclic binding is not a value")


def test_decidable_conditionals_are_values():
    print("\n== a branch the declaration decides is a value ==")
    # MSL writes derived parameters as `if PRef <= 0 then 0 else <expr>`
    # (`DCSE_Start` does, for three of them). Rumoca resolves the branch itself
    # when the arm is an exact integer, so skipping conditionals here made the
    # verdict depend on which arm the declaration happened to land on.
    p_ref = FakeVar(1, "PRef", binding=Lit(0.0))
    taken = Cond([(Bin("less_equal", Ref(p_ref), Lit(0)), Lit(0.0))], Lit(-5.0))
    check(constant_value(taken) == 0.0, "the selected arm is the value")

    p_ref.binding = Lit(10.0)
    check(constant_value(taken) == -5.0, "a false condition falls through")

    # A condition the declaration does not decide leaves the whole thing open;
    # guessing an arm would report a violation the model never commits to.
    free = FakeVar(2, "x", parameter=False)
    check(constant_value(Cond([(Bin("less", Ref(free), Lit(1)), Lit(-1.0))],
                              Lit(2.0))) is None,
          "an undecided condition is not a value")

    # Boolean parameters and negation decide arms too.
    flag = FakeVar(3, "useX", binding=Lit(True))
    check(constant_value(Cond([(Ref(flag), Lit(7.0))], Lit(0.0))) == 7.0,
          "a Boolean parameter decides its arm")
    check(constant_value(Cond([(Neg2("not", Ref(flag)), Lit(7.0))], Lit(0.0))) == 0.0,
          "negation decides its arm")

    # A comparison is not a number: `a < b` must never read back as 0.0.
    check(constant_value(Bin("less", Lit(1.0), Lit(2.0))) is None,
          "a comparison is not a value")


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
    # None of these doubles carries a declaring class, so no component
    # establishes the rule's premise: a bad value is *reported*, and reported
    # as a question rather than as a violation. Asserting on
    # `physical-invariant-violated` here would be asserting that the analyzer
    # knows an intent nobody wrote down.
    for label, variables, expected in cases:
        model = FakeModel(variables)
        findings = attach(san.analyze(model, AnalysisContext(model)))
        reported = [f for f in findings
                    if f.kind in ("physical-invariant-violated",
                                  "physical-intent-question")
                    and f.evidence.get("observed") is not None]
        check(len(reported) == expected, f"{label}: {len(reported)} reported")
        check(all(f.kind == "physical-intent-question" for f in reported),
              f"{label}: uncatalogued, so asked rather than asserted")


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


# ── the premise matrix: two paths, three states ──────────────────────────────
#
# The predicate and the authority for applying it are separate facts, and both
# paths through the sanitizer have to ask the second one. The observed-value
# path already did; the declaration path did not, and reported an unestablished
# premise as a medium-severity domain defect.


def _premise_case(variable, catalog=None, assumptions=None):
    from modelsan.semantics import SemanticBinder

    model = FakeModel([variable])
    binder = SemanticBinder(catalog=catalog) if catalog else SemanticBinder()
    context = AnalysisContext(model)
    if assumptions is not None:
        context.assumptions = assumptions
    found = PhysicalSan(binder=binder).analyze(model, context)
    return [f for f in found if variable.name in str(f.evidence)]


def _passive_catalog(klass, member):
    from modelsan.semantics import role as roles
    from modelsan.semantics.catalog import ClassCatalog, ClassSemantics

    return ClassCatalog().register(ClassSemantics(
        klass=klass, members={member: roles.PASSIVE_RESISTANCE},
        note="a passive resistor, for the purposes of this test"))


def _signed_catalog(klass, member):
    from modelsan.semantics import role as roles
    from modelsan.semantics.catalog import ClassCatalog, ClassSemantics

    return ClassCatalog().register(ClassSemantics(
        klass=klass, members={member: roles.UNRESTRICTED_RESISTANCE},
        note="documented as permitting either sign"))


def test_the_declaration_path_asks_when_the_premise_is_unknown():
    print("\n-- unenforced declaration, premise UNKNOWN --")
    variable = FakeVar(1, "mystery.R", quantity="Resistance", unit="Ohm",
                       binding=Lit(1.0))
    found = _premise_case(variable)
    kinds = {f.kind for f in found}
    check(kinds == {"physical-intent-question"},
          f"an unbounded uncatalogued declaration asks (got {sorted(kinds)})")
    check(found[0].severity.value == "low", "at low severity")
    check(found[0].evidence.get("observation") == "permissive-declaration",
          "about the declaration rather than a value")


def test_the_declaration_path_enforces_when_the_premise_is_established():
    print("\n-- unenforced declaration, premise ESTABLISHED --")
    variable = FakeVar(1, "shunt.R", quantity="Resistance", unit="Ohm",
                       binding=Lit(1.0))
    variable.declaring_class = "Vendor.PassiveShunt"
    found = _premise_case(variable, _passive_catalog("Vendor.PassiveShunt", "R"))
    kinds = {f.kind for f in found}
    check("physical-domain-unenforced" in kinds,
          f"a known passive resistor keeps the domain claim (got {sorted(kinds)})")
    claim = next(f for f in found if f.kind == "physical-domain-unenforced")
    check(claim.evidence.get("premise_state") == "established",
          f"premise_state=established (got {claim.evidence.get('premise_state')})")


def test_the_declaration_path_stands_down_when_the_premise_is_refuted():
    print("\n-- unenforced declaration, premise REFUTED --")
    variable = FakeVar(1, "nic.R", quantity="Resistance", unit="Ohm",
                       binding=Lit(1.0))
    variable.declaring_class = "Vendor.SignedResistor"
    found = _premise_case(variable, _signed_catalog("Vendor.SignedResistor", "R"))
    kinds = {f.kind for f in found}
    check("physical-domain-unenforced" not in kinds,
          f"no domain claim against a signed component (got {sorted(kinds)})")
    check("physical-intent-question" not in kinds,
          "and nothing to ask: the component already answered")


def test_the_observed_value_path_covers_the_same_three_states():
    print("\n-- observed value, all three states --")
    unknown = FakeVar(1, "mystery.R", quantity="Resistance", unit="Ohm",
                      binding=Lit(-1.0))
    kinds = {f.kind for f in _premise_case(unknown)}
    check(kinds == {"physical-intent-question"},
          f"UNKNOWN asks (got {sorted(kinds)})")

    established = FakeVar(1, "shunt.R", quantity="Resistance", unit="Ohm",
                          binding=Lit(-1.0))
    established.declaring_class = "Vendor.PassiveShunt"
    kinds = {f.kind for f in _premise_case(
        established, _passive_catalog("Vendor.PassiveShunt", "R"))}
    check("physical-invariant-violated" in kinds,
          f"ESTABLISHED enforces (got {sorted(kinds)})")

    refuted = FakeVar(1, "nic.R", quantity="Resistance", unit="Ohm",
                      binding=Lit(-1.0))
    refuted.declaring_class = "Vendor.SignedResistor"
    kinds = {f.kind for f in _premise_case(
        refuted, _signed_catalog("Vendor.SignedResistor", "R"))}
    check("physical-invariant-violated" not in kinds,
          f"REFUTED does not (got {sorted(kinds)})")
