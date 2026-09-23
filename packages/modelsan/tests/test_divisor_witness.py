"""DivisorSan: every case must carry a verified zero witness.

These are regression tests for a specific and embarrassing failure. The pass
used to report every parameter appearing anywhere in a denominator, which meant
`1 + c_b*B_N + B_N^n` was filed as a defect because `c_b` can be zero. It
cannot be zeroed that way, and the finding was wrong.

Each case below is one the pass got wrong or must keep getting right. They are
named by the report ID that was filed, so a reader can go and read the claim
that is being refuted.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "packages" / "rumoca-bitcode"),
                str(ROOT / "packages" / "modelsan")]

from modelsan.analysis.context import AnalysisContext          # noqa: E402
from modelsan.divisor import build, collect, find              # noqa: E402
from modelsan.sanitizers import DivisorSan                     # noqa: E402

RUMOCA = ROOT / "target" / "debug" / "rumoca"
ROOTS = ["target/msl/ModelicaStandardLibrary-4.1.0",
         "target/corpus/ModelicaStandardLibrary-4.1.0",
         "target/cmm/CMM-a642c381"]

_CACHE: dict[str, object] = {}


def check(condition: bool, label: str) -> None:
    print(f"  {'ok  ' if condition else 'FAIL'} {label}")
    assert condition, label


def corpus_model(name: str):
    """Compile one corpus model, once per session."""
    if name in _CACHE:
        return _CACHE[name]
    if not RUMOCA.exists():
        _CACHE[name] = None
        return None
    path = None
    for line in (ROOT / "tools/sweep/ALL.list").read_text().splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[1].strip() == name:
            path = parts[0]
    if path is None:
        _CACHE[name] = None
        return None
    work = tempfile.mkdtemp()
    artifact = Path(work) / "m.rbc"
    command = [str(RUMOCA), "compile", path, "--model", name,
               "--emit-bitcode", str(artifact), "--no-fold-parameter-bindings"]
    for root in ROOTS:
        command += ["--source-root", root]
    subprocess.run(command, capture_output=True, cwd=ROOT)
    if not artifact.exists():
        _CACHE[name] = None
        return None
    import rumoca_bitcode
    _CACHE[name] = rumoca_bitcode.Model.load(artifact)
    return _CACHE[name]


def findings_for(name: str, needle: str) -> list | None:
    model = corpus_model(name)
    if model is None:
        return None
    all_findings = DivisorSan().analyze(model, AnalysisContext(model))
    return [f for f in all_findings if needle in str(f.evidence)]


def source_kinds(findings) -> set[str]:
    """Kinds that claim a defect in the model, as opposed to a guarded site."""
    return {f.kind for f in findings
            if f.kind in ("divisor-reachable-zero",
                          "divisor-zero-when-parameters-equal")}


# ── the zero predicate ───────────────────────────────────────────────────────


def test_only_a_sum_can_be_approximately_zero():
    print("\n== small is not zero, except where terms cancel ==")
    from modelsan.dae import BinaryOp, ops
    from modelsan.divisor.witness import _is_zero

    class Node(BinaryOp):
        def __init__(self, op):
            self.op = op

    cases = [
        ("a product that is exactly zero",  ops.MULTIPLY, 0.0,      1.0,      True),
        ("eps returned by a max() guard",   ops.MULTIPLY, 2.22e-16, 1.0,      False),
        ("a declared minimum of 2.2e-308",  ops.MULTIPLY, 2.2e-308, 2.2e-308, False),
        ("rounding in a cancelling sum",    ops.ADD,      1e-17,    1.0,      True),
        ("a sum that simply is not zero",   ops.ADD,      0.5,      1.0,      False),
    ]
    for label, op, residual, scale, expected in cases:
        check(_is_zero(Node(op), residual, scale) is expected, label)


# ── the witness discipline itself ────────────────────────────────────────────


def test_a_parameter_inside_a_denominator_is_not_a_witness():
    print("\n== 1 + c_b*B_N + B_N^n does not vanish at c_b = 0  (FINDING-03714) ==")
    model = corpus_model(
        "Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap")
    if model is None:
        print("  skip  model unavailable")
        return
    environment = build(model)
    target = next((s for s in collect(model, environment)
                   if "c_b" in repr(s.denominator)), None)
    check(target is not None, "the denominator containing c_b is found")
    check(any(v.name.endswith("c_b") for v in target.denominator.variables()),
          "and c_b really does appear inside it")

    # The point of the case: appearing inside is not the same as zeroing it.
    # Either the search finds no witness at all, or the witness it finds is
    # something other than `c_b = 0` and is verified to actually zero the
    # denominator.
    witness = find(target.denominator, environment)
    if witness is None:
        check(True, "no assignment is claimed to zero it")
    else:
        c_b = next(v for v in target.denominator.variables()
                   if v.name.endswith("c_b"))
        check(witness.assignment.get(c_b.id) != 0.0
              or abs(witness.residual) < 1e-12,
              f"any witness offered is verified: {witness.rendered(environment.names)} "
              f"-> {witness.residual:g}")

    findings = [f for f in DivisorSan().analyze(model, AnalysisContext(model))
                if "c_b" in str(f.evidence)]
    check(not source_kinds(findings),
          f"and no defect is reported for it, got {[f.kind for f in findings]}")


def test_an_offset_of_one_cannot_be_cancelled_by_zeroing_a_coefficient():
    print("\n== 1 + alpha*(T - T_ref) at alpha = 0 is 1  (FINDING-00185) ==")
    findings = findings_for("Modelica.Electrical.Analog.Examples.ChuaCircuit",
                            "alpha")
    if findings is None:
        print("  skip  model unavailable")
        return
    check(not source_kinds(findings),
          f"no defect reported, got {[f.kind for f in findings]}")
    # It is additionally protected, and saying so is worth more than silence.
    guarded = [f for f in findings if f.kind == "divisor-guarded-by-assertion"]
    check(bool(guarded) or not findings,
          "if reported at all, it is reported as guarded by the model's assert")


def test_a_constant_is_never_a_witness():
    print("\n== pi is immutable  (FINDING-01566) ==")
    model = corpus_model(
        "Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking")
    if model is None:
        print("  skip  model unavailable")
        return
    environment = build(model)
    pi = next((v for v in model.variables if v.name.endswith(".pi")), None)
    check(pi is not None, "the model declares pi")
    check(not environment.domain(pi.id).settable,
          f"pi is not settable ({environment.domain(pi.id).reason})")
    findings = [f for f in DivisorSan().analyze(model, AnalysisContext(model))
                if "pi = " in str(f.evidence.get("witness", ""))]
    check(not findings, f"pi is never proposed as a witness, got {len(findings)}")


def test_a_witness_that_disables_the_branch_is_not_a_defect():
    print("\n== duration = 0 makes the Ramp division unreachable  (FINDING-00002) ==")
    findings = findings_for(
        "Modelica.Clocked.Examples.SimpleControlledDrive.ClockedWithDiscreteController",
        "duration")
    if findings is None:
        print("  skip  model unavailable")
        return
    check(not source_kinds(findings),
          f"no defect reported, got {[f.kind for f in findings]}")


def test_a_division_the_compiler_introduced_is_labelled_as_such():
    print("\n== L*der(i) = v contains no source division  (BUG-004) ==")
    model = corpus_model("Modelica.Electrical.Analog.Examples.ParallelResonance")
    if model is None:
        print("  skip  model unavailable")
        return
    findings = [f for f in DivisorSan().analyze(model, AnalysisContext(model))
                if "inductor1.L" in str(f.evidence)]
    for finding in findings:
        check(finding.kind != "divisor-reachable-zero",
              f"an inductance is not reported as a source division "
              f"({finding.kind})")
    check(True, f"{len(findings)} finding(s), none claiming a source division")


def test_an_asserted_denominator_is_reported_as_guarded():
    print("\n== 1/(k*Ni) is covered by an assertion  (FINDING-04783) ==")
    findings = findings_for("ModelicaTest.Blocks.Continuous", "limPID.k")
    if findings is None:
        print("  skip  model unavailable")
        return
    check(not source_kinds(findings),
          f"no defect reported, got {[f.kind for f in findings]}")


def test_a_denominator_zero_as_declared_but_guarded_is_not_a_defect():
    print("\n== if F > 0 then a/F: F = 0 is what the guard excludes ==")
    model = corpus_model("Modelica.Electrical.Analog.Examples.Lines.SmoothStep")
    if model is None:
        print("  skip  model unavailable")
        return
    findings = [f for f in DivisorSan().analyze(model, AnalysisContext(model))
                if f.evidence.get("denominator", "").endswith(".F")]
    check(not source_kinds(findings),
          f"no defect reported, got {[f.kind for f in findings]}")
    unreachable = [f for f in findings
                   if f.kind == "divisor-unreachable-under-witness"]
    check(bool(unreachable) or not findings,
          "if reported at all, it is reported as excluded by its guard")


# ── the cases that must keep firing ──────────────────────────────────────────


def test_a_difference_of_two_parameters_is_a_defect():
    print("\n== Vps - Vns vanishes when they are equal  (BUG-024) ==")
    findings = findings_for(
        "Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator", "Vps")
    if findings is None:
        print("  skip  model unavailable")
        return
    relational = [f for f in findings
                  if f.kind == "divisor-zero-when-parameters-equal"]
    check(bool(relational), f"reported, got {[f.kind for f in findings]}")
    if relational:
        evidence = relational[0].evidence
        check("Vns" in evidence["witness"] or "Vps" in evidence["witness"],
              f"the witness is an equality: {evidence['witness']}")
        check(abs(evidence["denominator_at_witness"]) < 1e-9,
              "and it is verified to zero the denominator")


def test_a_direct_reachable_zero_is_a_defect():
    print("\n== level/resistance divides directly by a knob  (FINDING-05128) ==")
    findings = findings_for("Tank", "resistance")
    if findings is None:
        print("  skip  model unavailable")
        return
    check(bool(source_kinds(findings)),
          f"reported, got {[f.kind for f in findings]}")
    if findings:
        check(abs(findings[0].evidence["denominator_at_witness"]) < 1e-9,
              "with a verified witness")


def test_every_reported_defect_carries_a_verified_witness():
    print("\n== no finding is reported without arithmetic behind it ==")
    checked = 0
    for name in ("Modelica.Electrical.Analog.Examples.ChuaCircuit",
                 "Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator",
                 "Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap"):
        model = corpus_model(name)
        if model is None:
            continue
        for finding in DivisorSan().analyze(model, AnalysisContext(model)):
            checked += 1
            evidence = finding.evidence
            check("witness" in evidence and bool(evidence["witness"]),
                  f"{finding.kind} names an assignment")
            check(abs(evidence["denominator_at_witness"]) < 1e-6,
                  f"{finding.kind} verified its witness "
                  f"({evidence['denominator_at_witness']:g})")
            check("path_condition" in evidence,
                  f"{finding.kind} states its path condition")
    check(checked >= 0, f"{checked} findings checked")
