"""Unknown physical intent is a question, not silence and not an error.

An SI quantity says what kind of value something is. It does not say what the
component is *for*: `SI.Resistance` describes a passive resistor, an active
negative impedance, a linearised incremental model, an optimisation variable
and a fault-injection input alike. So the predicate (`R > 0`) and the authority
for applying it here are two separate facts, and this module pins the second.

Three states, carried in the finding rather than encoded as a severity:

    ESTABLISHED  a component contract or a user assumption applies  -> enforce
    REFUTED      an authoritative contract permits the value        -> record
    UNKNOWN      only quantity, unit or a name matched              -> ask

The failure this guards against is not a false positive. It is the temptation
to fix false positives by suppressing every unknown case, which would buy
precision with recall and hide the negative resistance nobody catalogued.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "packages" / "rumoca-bitcode"),
                str(ROOT / "packages" / "modelsan")]

from modelsan.analysis.context import AnalysisContext                # noqa: E402
from modelsan.contracts import AssumptionSet                         # noqa: E402
from modelsan.sanitizers import PhysicalSan                          # noqa: E402

RUMOCA = ROOT / "target" / "debug" / "rumoca"
ROOTS = ["target/msl/ModelicaStandardLibrary-4.1.0",
         "target/corpus/ModelicaStandardLibrary-4.1.0",
         "target/cmm/CMM-a642c381"]
ADVISORY = "physical-intent-question"
_CACHE: dict[str, object] = {}


def check(condition: bool, label: str) -> None:
    print(f"  {'ok  ' if condition else 'FAIL'} {label}")
    assert condition, label


def inline_model(source: str, name: str):
    if not RUMOCA.exists():
        return None
    work = tempfile.mkdtemp()
    path = Path(work) / f"{name}.mo"
    path.write_text(source)
    artifact = Path(work) / f"{name}.rbc"
    subprocess.run([str(RUMOCA), "compile", str(path), "--model", name,
                    "--emit-bitcode", str(artifact)],
                   capture_output=True, cwd=ROOT)
    if not artifact.exists():
        return None
    import rumoca_bitcode
    return rumoca_bitcode.Model.load(artifact)


def corpus_model(name: str):
    if name in _CACHE:
        return _CACHE[name]
    path = None
    for line in (ROOT / "tools/sweep/ALL.list").read_text().splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[1].strip() == name:
            path = parts[0]
    _CACHE[name] = None
    if path is None or not RUMOCA.exists():
        return None
    work = tempfile.mkdtemp()
    artifact = Path(work) / "m.rbc"
    command = [str(RUMOCA), "compile", path, "--model", name,
               "--emit-bitcode", str(artifact)]
    for root in ROOTS:
        command += ["--source-root", root]
    subprocess.run(command, capture_output=True, cwd=ROOT)
    if artifact.exists():
        import rumoca_bitcode
        _CACHE[name] = rumoca_bitcode.Model.load(artifact)
    return _CACHE[name]


def findings_for(model, assumptions=None):
    context = AnalysisContext(model)
    if assumptions is not None:
        context.assumptions = assumptions
    return PhysicalSan().analyze(model, context)


def about(findings, needle: str) -> list:
    return [f for f in findings if needle in str(f.evidence)]


# ── unknown intent must remain visible ───────────────────────────────────────

UNCATALOGUED_RESISTANCE = """
model Mystery
  parameter Real R(quantity = "Resistance", unit = "Ohm") = -1;
  Real x(start = 1, fixed = true);
equation
  der(x) = R - x;
end Mystery;
"""

UNCATALOGUED_MASS = """
model MysteryMass
  parameter Real m(quantity = "Mass", unit = "kg") = -1;
  Real x(start = 1, fixed = true);
equation
  der(x) = m - x;
end MysteryMass;
"""


def _one_advisory(source: str, name: str, leaf: str):
    model = inline_model(source, name)
    if model is None:
        print("  skip: rumoca not built")
        return None
    found = about(findings_for(model), f"{leaf} ")
    check(len(found) == 1, f"exactly one finding for {leaf} (got {len(found)})")
    finding = found[0]
    check(finding.kind == ADVISORY,
          f"and it is an advisory (got {finding.kind})")
    check(finding.severity.value == "low",
          f"at low severity (got {finding.severity.value})")
    check(finding.evidence.get("premise_state") == "unknown",
          f"with premise_state=unknown (got {finding.evidence.get('premise_state')})")
    check("question" in finding.evidence,
          "and a question addressed to the author")
    check("?" in str(finding.evidence.get("question", "")),
          "which is phrased as one")
    return finding


def test_an_uncatalogued_negative_resistance_asks_rather_than_asserts():
    print("\n== negative resistance, no component contract ==")
    finding = _one_advisory(UNCATALOGUED_RESISTANCE, "Mystery", "R")
    if finding is None:
        return
    check(finding.evidence.get("observation") == "observed-value",
          "the advisory says it is about the value it holds")
    check(finding.evidence.get("authority") == "quantity_or_unit",
          f"on quantity/unit authority (got {finding.evidence.get('authority')})")


def test_an_uncatalogued_mass_is_not_special_cased_to_electrical_names():
    print("\n== the same for a mass-like parameter ==")
    _one_advisory(UNCATALOGUED_MASS, "MysteryMass", "m")


def test_an_unbounded_uncatalogued_declaration_asks_too():
    print("\n== permissive declaration, no component contract ==")
    model = inline_model("""
model Permissive
  parameter Real R(quantity = "Resistance", unit = "Ohm") = 1;
  Real x(start = 1, fixed = true);
equation
  der(x) = R - x;
end Permissive;
""", "Permissive")
    if model is None:
        print("  skip: rumoca not built")
        return
    found = about(findings_for(model), "R ")
    check(len(found) == 1, f"exactly one finding (got {len(found)})")
    check(found[0].kind == ADVISORY,
          f"the unbounded path asks too (got {found[0].kind})")
    check(found[0].evidence.get("observation") == "permissive-declaration",
          "and says it is about the declaration rather than a value")
    check(found[0].severity.value == "low",
          f"at low severity (got {found[0].severity.value})")


def test_an_advisory_is_never_silence():
    print("\n== the fix for false positives is not suppression ==")
    for source, name, leaf in ((UNCATALOGUED_RESISTANCE, "Mystery", "R"),
                               (UNCATALOGUED_MASS, "MysteryMass", "m")):
        model = inline_model(source, name)
        if model is None:
            print("  skip: rumoca not built")
            return
        check(bool(about(findings_for(model), f"{leaf} ")),
              f"{leaf} is still reported")


# ── explicit contracts still enforce ─────────────────────────────────────────


def test_a_catalogued_passive_resistance_still_produces_a_violation():
    print("\n== an established premise is enforced ==")
    from modelsan.semantics import SemanticBinder, role as roles
    from modelsan.semantics.catalog import ClassCatalog, ClassSemantics

    model = inline_model("""
model Passive
  parameter Real R(quantity = "Resistance", unit = "Ohm") = -1;
  Real x(start = 1, fixed = true);
equation
  der(x) = R - x;
end Passive;
""", "Passive")
    if model is None:
        print("  skip: rumoca not built")
        return
    catalog = ClassCatalog().register(ClassSemantics(
        klass="Passive", members={"R": roles.PASSIVE_RESISTANCE},
        note="a passive resistor for the purposes of this test"))
    san = PhysicalSan(binder=SemanticBinder(catalog=catalog))
    found = about(san.analyze(model, AnalysisContext(model)), "R ")
    kinds = {f.kind for f in found}
    check("physical-invariant-violated" in kinds,
          f"a passive resistance at -1 is a violation (got {sorted(kinds)})")
    violation = next(f for f in found if f.kind == "physical-invariant-violated")
    check(violation.evidence.get("premise_state") == "established",
          f"premise_state=established (got {violation.evidence.get('premise_state')})")
    check(violation.severity.value == "high",
          f"at high severity (got {violation.severity.value})")


def test_a_machine_winding_allows_zero_and_rejects_negative():
    print("\n== nonnegative is neither positive nor signed ==")
    model = corpus_model(
        "Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking")
    if model is None:
        print("  skip: corpus model unavailable")
        return
    required = {str(f.evidence.get("required", ""))
                for f in about(findings_for(model), "imcData.Rs")}
    check(any(">= 0" in r for r in required),
          f"the winding claim is >= 0 (got {sorted(required)})")
    check(not any(r.endswith("> 0") for r in required),
          f"and never a strict > 0 (got {sorted(required)})")


def test_a_user_assumption_promotes_an_advisory_to_a_violation():
    print("\n== sign_domain = nonnegative establishes the premise ==")
    model = inline_model(UNCATALOGUED_RESISTANCE, "Mystery")
    if model is None:
        print("  skip: rumoca not built")
        return
    assumptions = AssumptionSet.from_dict({"contracts": [{
        "match": "declaration", "target": "Mystery.R",
        "sign_domain": "nonnegative",
        "reason": "copper resistance; zero is the ideal lossless limit"}]},
        origin="intent.toml")
    found = about(findings_for(model, assumptions), "R ")
    kinds = {f.kind for f in found}
    check("physical-invariant-violated" in kinds,
          f"the advisory is promoted (got {sorted(kinds)})")
    violation = next(f for f in found if f.kind == "physical-invariant-violated")
    check(violation.evidence.get("premise_state") == "established",
          "premise_state=established")
    check(violation.evidence.get("authority") == "user_assumption",
          f"on user authority (got {violation.evidence.get('authority')})")
    check(">= 0" in str(violation.evidence.get("required", "")),
          f"and the claim is the one the user stated "
          f"({violation.evidence.get('required')})")
    check("lossless" in str(violation.evidence.get("premise_reason", "")),
          "the reason from the file travels with it")


def test_a_signed_assumption_refutes_the_generic_heuristic():
    print("\n== sign_domain = signed refutes it ==")
    model = inline_model(UNCATALOGUED_RESISTANCE, "Mystery")
    if model is None:
        print("  skip: rumoca not built")
        return
    assumptions = AssumptionSet.from_dict({"contracts": [{
        "match": "declaration", "target": "Mystery.R",
        "sign_domain": "signed",
        "reason": "an active negative-impedance element"}]})
    found = about(findings_for(model, assumptions), "R ")
    kinds = {f.kind for f in found}
    check("physical-invariant-violated" not in kinds,
          f"no violation (got {sorted(kinds)})")
    check(ADVISORY not in kinds, f"and no advisory either (got {sorted(kinds)})")
    check("physical-rule-does-not-apply" in kinds,
          f"the refusal is recorded (got {sorted(kinds)})")
    record = next(f for f in found if f.kind == "physical-rule-does-not-apply")
    check(record.evidence.get("premise_state") == "refuted",
          "premise_state=refuted")


# ── the reviewed false positives stay fixed ──────────────────────────────────


def test_the_reviewed_signed_and_zero_limit_cases_stay_fixed():
    print("\n== the four reviewed groups ==")
    cases = [
        ("Modelica.Electrical.Analog.Examples.CauerLowPassSC", "R4.R",
         "SwitchedCapacitor.R = -1 is what the component is for"),
        ("Modelica.Electrical.Analog.Examples.ChuaCircuit", "Nr.Ga",
         "Chua's negative slope is the device"),
        ("Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking",
         "imc.rs.R", "a polyphase resistor inherits the signed scalar contract"),
        ("Modelica.Electrical.Analog.Examples.ChuaCircuit", "L.L",
         "L = 0 is the ideal-short algebraic limit"),
    ]
    banned = {"physical-invariant-violated", "physical-domain-unenforced",
              "physical-bound-permits-zero"}
    for name, target, why in cases:
        model = corpus_model(name)
        if model is None:
            print(f"  skip: {name} unavailable")
            continue
        kinds = {f.kind for f in about(findings_for(model), target)}
        check(not (kinds & banned), f"{why} (got {sorted(kinds)})")


def test_an_off_diagonal_inertia_entry_is_never_judged_alone():
    print("\n== a product of inertia is signed ==")
    model = corpus_model("Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody")
    if model is None:
        print("  skip: corpus model unavailable")
        return
    for field in ("I_21", "I_31", "I_32"):
        check(not about(findings_for(model), f".{field}"),
              f"nothing reports {field} on its own")


# ── independent numerical failures are untouched ─────────────────────────────


def test_a_zero_contract_does_not_excuse_a_negative_value():
    print("\n== ALGEBRAIC_LIMIT excuses zero, not -1 ==")
    from modelsan.contracts import ZeroBehavior, resolve
    from modelsan.divisor import build

    model = inline_model("""
model Coil
  parameter Real L(quantity = "Inductance", unit = "H") = -1;
  Real i(start = 0, fixed = true);
  Real v;
equation
  L * der(i) = v;
  v = 1;
end Coil;
""", "Coil")
    if model is None:
        print("  skip: rumoca not built")
        return
    contracts = resolve(model, build(model))
    contract = next((contracts.get(v.id) for v in model.variables
                     if v.name == "L"), None)
    check(contract is not None
          and contract.behavior is ZeroBehavior.ALGEBRAIC_LIMIT,
          f"the contract is about zero (got {contract and contract.behavior})")
    kinds = {f.kind for f in about(findings_for(model), "L ")}
    check("physical-zero-is-a-supported-limit" not in kinds,
          f"and does not excuse a negative inductance (got {sorted(kinds)})")


def test_a_physical_contract_never_suppresses_a_live_denominator():
    print("\n== intent-independent source arithmetic outranks every contract ==")
    from modelsan.sanitizers import DivisorSan

    model = inline_model("""
model Tank
  parameter Real area(quantity = "Area", unit = "m2") = 1;
  Real level(start = 1, fixed = true);
equation
  der(level) = 1 / area;
end Tank;
""", "Tank")
    if model is None:
        print("  skip: rumoca not built")
        return
    assumptions = AssumptionSet.from_dict({"contracts": [{
        "match": "declaration", "target": "Tank.area",
        "zero_behavior": "allowed", "sign_domain": "signed",
        "reason": "the user insists this is fine"}]})
    context = AnalysisContext(model)
    context.assumptions = assumptions
    kinds = {f.kind for f in DivisorSan().analyze(model, context)}
    check("divisor-reachable-zero" in kinds,
          f"the division is still reported (got {sorted(kinds)})")


# ── advisories are not bugs, and do not fail a run ───────────────────────────


def test_an_advisory_only_run_exits_zero_and_counts_no_bug():
    print("\n== an advisory-only model is not a failure ==")
    if not RUMOCA.exists():
        print("  skip: rumoca not built")
        return
    work = Path(tempfile.mkdtemp())
    (work / "Mystery.mo").write_text(UNCATALOGUED_RESISTANCE)
    finished = subprocess.run(
        [sys.executable, "tools/sweep/check_one.py", str(work / "Mystery.mo"),
         "--model", "Mystery", "--sanitizer", "physical", "--json"],
        capture_output=True, text=True, cwd=ROOT,
        env={"PYTHONPATH": "packages/modelsan:packages/rumoca-bitcode",
             "PATH": "/usr/bin:/bin"})
    check(finished.returncode == 0,
          f"the run exits successfully (got {finished.returncode})")
    payload = json.loads(finished.stdout)
    kinds = {row["kind"] for row in payload["findings"]}
    check(kinds == {ADVISORY}, f"and reports only advisories (got {kinds})")
    check(all(row["severity"] == "low" for row in payload["findings"]),
          "all at low severity")
    check(all(row["evidence"].get("premise_state") == "unknown"
              for row in payload["findings"]),
          "each carrying the premise that was missing")


def test_the_advisory_kind_is_excluded_from_the_defect_population():
    print("\n== a question is not a defect claim ==")
    source = (ROOT / "tools/sweep/precision_table.py").read_text()
    start = source.index("NOT_A_CLAIM")
    excluded = source[start:source.index("}", start)]
    check(ADVISORY in excluded,
          "precision_table.py excludes advisories from the weighted figure")
    check("physical-rule-does-not-apply" in excluded,
          "and excludes refutations")


def test_the_execution_confirmed_physical_cases_are_not_downgraded():
    print("\n== an arithmetic failure is not a question about intent ==")
    cases = [
        ("Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator", "C",
         "OMC reports division by zero in C*R"),
        ("Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator", "R2",
         "OMC reports an invalid logarithm argument"),
    ]
    for name, target, why in cases:
        model = corpus_model(name)
        if model is None:
            print(f"  skip: {name} unavailable")
            continue
        found = [f for f in findings_for(model)
                 if str(f.evidence.get("required", "")).startswith(f"{target} ")]
        check(bool(found), f"{target} is still reported ({why})")
        kinds = {f.kind for f in found}
        check(ADVISORY not in kinds,
              f"and not as a question (got {sorted(kinds)})")
        check(all(f.evidence.get("premise_state") == "established"
                  for f in found),
              "its premise is established by the source arithmetic")
        check(all(f.evidence.get("authority") == "source_arithmetic"
                  for f in found),
              f"on that authority "
              f"({[f.evidence.get('authority') for f in found]})")
