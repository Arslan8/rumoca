"""Rules whose subject is a group, and sign rules scoped by component.

Two false-positive families, 268 reports between them:

    182  inertia-tensor entries checked one at a time against `> 0`
     86  resistance and conductance judged by `SI.Resistance` alone

The first is a *shape* error: the constraint on an inertia tensor is that the
assembled matrix is positive semidefinite, and the off-diagonal entries are
signed products of inertia that mean nothing on their own. Checking them
individually is both noisy and unsound --- `[[1,2,0],[2,1,0],[0,0,1]]` passes
every scalar check and has a negative eigenvalue.

The second is an *authority* error: `Basic.Resistor.R` is documented as
"allowed to be positive, zero, or negative", a machine winding is nonnegative
with zero the ideal lossless limit, and a negative-impedance converter is
signed by construction. One quantity, three contracts.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "packages" / "rumoca-bitcode"),
                str(ROOT / "packages" / "modelsan")]

from modelsan.analysis.context import AnalysisContext                # noqa: E402
from modelsan.contracts import AssumptionSet                         # noqa: E402
from modelsan.divisor import build                                   # noqa: E402
from modelsan.physical import aggregate                              # noqa: E402
from modelsan.sanitizers import PhysicalSan                          # noqa: E402

RUMOCA = ROOT / "target" / "debug" / "rumoca"
ROOTS = ["target/msl/ModelicaStandardLibrary-4.1.0",
         "target/corpus/ModelicaStandardLibrary-4.1.0",
         "target/cmm/CMM-a642c381"]
_CACHE: dict[str, object] = {}


def check(condition: bool, label: str) -> None:
    print(f"  {'ok  ' if condition else 'FAIL'} {label}")
    assert condition, label


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


def naming(findings, needle: str) -> list:
    return [f for f in findings if needle in str(f.evidence)]


# ── the tensor mathematics ───────────────────────────────────────────────────

VALID = {
    "identity": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    "valid negative cross-term": [[2, -1, 0], [-1, 2, 0], [0, 0, 1]],
    "semidefinite": [[1, 0, 0], [0, 1, 0], [0, 0, 0]],
}
INVALID = {
    "negative diagonal": [[-1, 0, 0], [0, 1, 0], [0, 0, 1]],
    "positive diagonals, negative eigenvalue": [[1, 2, 0], [2, 1, 0], [0, 0, 1]],
}


def _tolerance(m):
    return 1e-12 * max(abs(x) for row in m for x in row)


def test_valid_tensors_pass():
    print("\n== tensors a rigid body can have ==")
    for label, m in VALID.items():
        check(aggregate._failed_minor(m, _tolerance(m)) is None,
              f"{label} is positive semidefinite")


def test_invalid_tensors_fail():
    print("\n== tensors no rigid body can have ==")
    for label, m in INVALID.items():
        failed = aggregate._failed_minor(m, _tolerance(m))
        check(failed is not None, f"{label} is rejected")
        check(min(aggregate.eigenvalues(m)) < 0,
              f"{label} has a negative eigenvalue ({failed[0]} = {failed[1]:g})")


def test_all_principal_minors_are_used_not_only_the_leading_ones():
    print("\n== Sylvester's criterion is about definiteness, not semi- ==")
    # Leading minors 0, 0, 0 --- every one non-negative --- and an eigenvalue
    # of -1. Only a non-leading principal minor catches it.
    m = [[0, 0, 0], [0, 1, 0], [0, 0, -1]]
    check(aggregate._failed_minor(m, 0.0) is not None,
          "a zero leading block does not hide a negative diagonal entry")


def test_eigenvalues_match_a_known_spectrum():
    print("\n== the closed-form eigenvalue solver ==")
    values = aggregate.eigenvalues([[2, -1, 0], [-1, 2, 0], [0, 0, 1]])
    check(all(abs(a - b) < 1e-9 for a, b in zip(values, (1.0, 1.0, 3.0))),
          f"eigenvalues are 1, 1, 3 (got {values})")


def test_realizability_is_diagnostic_and_never_a_verdict():
    print("\n== a valid tensor may fail the triangle inequality ==")
    m = [[2, -1, 0], [-1, 2, 0], [0, 0, 1]]
    check(aggregate._failed_minor(m, _tolerance(m)) is None,
          "the spec requires this tensor to pass")
    check(aggregate._realizable(aggregate.eigenvalues(m), 0.0) is False,
          "and its principal moments are 1, 1, 3, so 3 > 1 + 1")


# ── the tensor as it reaches a model ─────────────────────────────────────────


def test_a_body_tensor_produces_no_scalar_findings():
    print("\n== one tensor, not six positivity findings ==")
    model = corpus_model("Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody")
    if model is None:
        print("  skip: corpus model unavailable")
        return
    found = findings_for(model)
    for field in ("I_11", "I_22", "I_33", "I_21", "I_31", "I_32"):
        hits = [f for f in found if f".{field}" in str(f.evidence)]
        check(not hits, f"nothing reports {field} on its own (got {len(hits)})")


def test_a_valid_tensor_is_recognised_and_decided():
    print("\n== the tensors in FreeBody are assembled and found valid ==")
    model = corpus_model("Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody")
    if model is None:
        print("  skip: corpus model unavailable")
        return
    found = aggregate.tensors(model, build(model))
    check(len(found) == 2, f"two tensors are recognised (got {len(found)})")
    for tensor in found:
        check(tensor.verdict is aggregate.Verdict.VALID,
              f"{tensor.owner} is valid ({tensor.reason})")
        check(set(tensor.fields) == set(aggregate.FIELDS),
              "all six fields were found")


def test_an_invalid_tensor_is_reported_once():
    print("\n== a bad tensor yields one finding, with the failed minor ==")
    model = inline_model("""
model Skewed
  parameter Real I_11(quantity = "MomentOfInertia", unit = "kg.m2") = 1;
  parameter Real I_22(quantity = "MomentOfInertia", unit = "kg.m2") = 1;
  parameter Real I_33(quantity = "MomentOfInertia", unit = "kg.m2") = 1;
  parameter Real I_21(quantity = "MomentOfInertia", unit = "kg.m2") = 2;
  parameter Real I_31(quantity = "MomentOfInertia", unit = "kg.m2") = 0;
  parameter Real I_32(quantity = "MomentOfInertia", unit = "kg.m2") = 0;
  Real x(start = 1, fixed = true);
equation
  der(x) = I_11 + I_21 - x;
end Skewed;
""", "Skewed")
    if model is None:
        print("  skip: rumoca not built")
        return
    found = [f for f in findings_for(model)
             if f.kind.startswith("physical-inertia-tensor")]
    check(len(found) == 1, f"exactly one finding for one tensor (got {len(found)})")
    evidence = found[0].evidence
    check(found[0].kind == "physical-inertia-tensor-not-semidefinite",
          f"it says the tensor is not semidefinite (got {found[0].kind})")
    check("I_11*I_22 - I_21^2" in str(evidence.get("violated_minor")),
          f"and names the minor that failed ({evidence.get('violated_minor')})")
    check("eigenvalues" in evidence, "the diagnostic carries the eigenvalues")
    check("[[1, 2, 0], [2, 1, 0], [0, 0, 1]]" in evidence.get("matrix", ""),
          f"and the assembled matrix ({evidence.get('matrix')})")


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


# ── resistance, scoped by component ──────────────────────────────────────────


def test_a_generic_resistor_is_signed():
    print("\n== Basic.Resistor.R = -1 and = 0 are both documented ==")
    model = corpus_model("Modelica.Electrical.Analog.Examples.CauerLowPassSC")
    if model is None:
        print("  skip: corpus model unavailable")
        return
    kinds = {f.kind for f in naming(findings_for(model), "R4.R")}
    check("physical-invariant-violated" not in kinds,
          f"R = -1 is not a violation here (got {sorted(kinds)})")


def test_polyphase_resistance_inherits_the_scalar_contract():
    print("\n== Polyphase.Basic.Resistor is an array of the scalar one ==")
    model = corpus_model(
        "Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking")
    if model is None:
        print("  skip: corpus model unavailable")
        return
    hits = naming(findings_for(model), "imc.rs.R >")
    kinds = {f.kind for f in hits}
    check(not (kinds & {"physical-domain-unenforced", "physical-invariant-violated"}),
          f"no positivity claim against a signed component (got {sorted(kinds)})")


def test_machine_winding_resistance_allows_zero_and_forbids_negative():
    print("\n== a winding is nonnegative: not positive, not signed ==")
    model = corpus_model(
        "Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking")
    if model is None:
        print("  skip: corpus model unavailable")
        return
    hits = naming(findings_for(model), "imcData.Rs")
    check(bool(hits), "the winding is still checked")
    required = {str(f.evidence.get("required", "")) for f in hits}
    check(any(">= 0" in r for r in required),
          f"the claim is >= 0, so zero is allowed (got {sorted(required)})")
    check(not any("> 0" in r and ">= 0" not in r for r in required),
          f"and nothing demands a strictly positive winding (got {sorted(required)})")


def test_a_quantity_only_match_cannot_confirm_a_violation():
    print("\n== SI.Resistance alone is not a passive resistor ==")
    model = inline_model("""
model Anonymous
  parameter Real R(quantity = "Resistance", unit = "Ohm") = -1;
  Real x(start = 1, fixed = true);
equation
  der(x) = R - x;
end Anonymous;
""", "Anonymous")
    if model is None:
        print("  skip: rumoca not built")
        return
    found = [f for f in findings_for(model) if "R " in str(f.evidence)]
    kinds = {f.kind for f in found}
    check("physical-invariant-violated" not in kinds,
          f"no confirmed violation without a declaring class (got {sorted(kinds)})")
    check("physical-intent-question" in kinds,
          f"an advisory is still raised (got {sorted(kinds)})")


# ── the assumption fallback ──────────────────────────────────────────────────


def test_an_aggregate_assumption_is_parsed_and_carries_its_origin():
    print("\n== [[contracts]] aggregate = symmetric_inertia_tensor ==")
    found = AssumptionSet.from_dict({"contracts": [{
        "match": "declaration", "target": "MyLibrary.Body.I",
        "aggregate": "symmetric_inertia_tensor",
        "domain": "positive_semidefinite",
        "reason": "Rigid-body inertia tensor about the center of mass"}]},
        origin="my.toml")
    check(len(found.aggregates) == 1, "the entry is recognised as an aggregate")
    entry = found.aggregates[0]
    check(entry.domain == "positive_semidefinite", "the domain is kept")
    check("my.toml" in entry.origin or entry.origin == "my.toml",
          f"the file is retained ({entry.origin})")
    check("center of mass" in entry.explain(), "so is the reason")


def test_a_role_assumption_selects_the_rule():
    print("\n== [[contracts]] role = machine_winding_resistance ==")
    found = AssumptionSet.from_dict({"contracts": [{
        "match": "declaration", "target": "MyLibrary.Motor.Rs",
        "role": "machine_winding_resistance", "sign_domain": "nonnegative",
        "reason": "Copper resistance; zero permits an ideal lossless winding"}]})
    check(list(found.roles) == ["MyLibrary.Motor.Rs"], "the role is indexed")
    entry = found.roles["MyLibrary.Motor.Rs"]
    check(entry.role == "component.machine.winding_resistance",
          f"and resolved to a semantic role ({entry.role})")
    check(entry.sign_domain == "nonnegative", "with its sign domain")
    check(entry.zero_behavior is None,
          "a role entry states no zero behaviour and is not made to invent one")


def test_an_unknown_aggregate_or_role_is_refused():
    print("\n== a typo that silently does nothing is worse than an error ==")
    for entry in ({"target": "x", "aggregate": "tensor"},
                  {"target": "x", "role": "wizard"},
                  {"target": "x", "role": "active_resistance",
                   "sign_domain": "upward"}):
        try:
            AssumptionSet.from_dict({"contracts": [entry]}, origin="bad.toml")
            check(False, f"{entry} was accepted")
        except ValueError as error:
            check(True, f"refused: {str(error).split(';')[0]}")
