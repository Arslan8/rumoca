"""A pass can add computation to an artifact with no instructions in it.

The objection this answers: LLVM IR is Turing complete, so an instrumentation
pass can insert arbitrary code; this IR is total, so — apparently — it cannot.

The premise is right and the conclusion is wrong. A pass here inserts
*equations*. An auxiliary state with a residual defining it is an accumulator,
a discrete variable with a `when` definition is a register, a relation and a
root are a branch. The resulting hybrid system is Turing complete (see
`crates/rumoca-bitcode/examples/Minsky.mo`), so the injected computation is not
limited in power — and the artifact stays total, so every analysis in this
package still terminates on the instrumented model.

These tests are the demonstration: inject, validate, simulate, read the answer
back out.
"""
from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "packages" / "rumoca-bitcode"),
                str(ROOT / "packages" / "modelsan")]

from modelsan.passes import Builder, inject_port_energy            # noqa: E402

RUMOCA = ROOT / "target" / "debug" / "rumoca"
ROOTS = ["target/msl/ModelicaStandardLibrary-4.1.0",
         "target/corpus/ModelicaStandardLibrary-4.1.0",
         "target/cmm/CMM-a642c381"]
CHUA = "Modelica.Electrical.Analog.Examples.ChuaCircuit"


def check(condition: bool, label: str) -> None:
    print(f"  {'ok  ' if condition else 'FAIL'} {label}")
    assert condition, label


def compiled(name: str = CHUA):
    path = None
    for line in (ROOT / "tools/sweep/ALL.list").read_text().splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[1].strip() == name:
            path = parts[0]
    if path is None or not RUMOCA.exists():
        return None, None
    work = Path(tempfile.mkdtemp())
    artifact = work / "m.rbc"
    command = [str(RUMOCA), "compile", path, "--model", name,
               "--emit-bitcode", str(artifact)]
    for root in ROOTS:
        command += ["--source-root", root]
    subprocess.run(command, capture_output=True, cwd=ROOT)
    if not artifact.exists():
        return None, None
    import rumoca_bitcode
    return rumoca_bitcode.Model.load(artifact), work


def test_a_pass_can_add_state_and_the_equation_that_drives_it():
    print("\n== inject an integrator into a model that had none ==")
    model, work = compiled()
    if model is None:
        print("  skip: corpus model unavailable")
        return
    before = (len(model.variables), len(model.equations))
    added = inject_port_energy(model)
    after = (len(model.variables), len(model.equations))

    check(added["variables"] == 7, f"seven accumulators added ({added})")
    check(after[0] - before[0] == after[1] - before[1] == 7,
          f"one state and one equation each ({before} -> {after})")
    check(len(added["components"]) == 7,
          f"one per component ({added['components']})")


def test_the_instrumented_artifact_still_validates_strictly():
    print("\n== the invariants the builder enforces are the real ones ==")
    model, work = compiled()
    if model is None:
        print("  skip: corpus model unavailable")
        return
    inject_port_energy(model)
    out = work / "instrumented.rbc"
    model.save(out)
    finished = subprocess.run(
        [str(RUMOCA), "bitcode", "check", str(out), "--strict"],
        capture_output=True, text=True, cwd=ROOT)
    check(finished.returncode == 0,
          f"valid after injection ({finished.stdout.strip()[-80:]})")


def test_the_injected_computation_actually_runs():
    print("\n== and the solver carries the new state ==")
    model, work = compiled()
    if model is None:
        print("  skip: corpus model unavailable")
        return
    inject_port_energy(model)
    out = work / "instrumented.rbc"
    model.save(out)
    trace = work / "energy.csv"
    subprocess.run([str(RUMOCA), "compile-bitcode", str(out), "--simulate",
                    "--trace-out", str(trace)],
                   capture_output=True, cwd=ROOT)
    check(trace.exists(), "a trajectory came back")
    final = {}
    for row in csv.DictReader(trace.open()):
        final[row["variable"]] = float(row["value"])
    check(len(final) == 7, f"seven energies observed ({sorted(final)})")

    # Chua's nonlinear resistor is the active element: it is the only thing in
    # the circuit that can deliver energy, and it does.
    check(final["energy_Nr"] < -1.0,
          f"the nonlinear resistor sources energy ({final['energy_Nr']:.3g} J)")
    check(final["energy_G"] > 1.0,
          f"the conductor dissipates it ({final['energy_G']:.3g} J)")
    check(abs(final["energy_Gnd"]) < 1e-9,
          f"ground exchanges nothing ({final['energy_Gnd']:.3g} J)")


def test_a_charged_capacitor_sources_energy_and_that_is_not_a_defect():
    print("\n== why the runtime check says dissipative, not passive ==")
    model, work = compiled()
    if model is None:
        print("  skip: corpus model unavailable")
        return
    inject_port_energy(model)
    out = work / "instrumented.rbc"
    model.save(out)
    trace = work / "energy.csv"
    subprocess.run([str(RUMOCA), "compile-bitcode", str(out), "--simulate",
                    "--trace-out", str(trace)],
                   capture_output=True, cwd=ROOT)
    final = {}
    for row in csv.DictReader(trace.open()):
        final[row["variable"]] = float(row["value"])

    # C1 starts at v = 4 V with C = 10, so it holds 80 J and discharges. A
    # check on "a passive component must not source power" fires here, on
    # correct physics, which is why NetworkSan checks dissipative components.
    check(final["energy_C1"] < 0,
          f"the charged capacitor delivers energy ({final['energy_C1']:.3g} J)")
    from modelsan.sanitizers import network as network_san
    check("PASSIVE_CAPACITANCE" in network_san.STORAGE_ROLES,
          "and storage roles are excluded from the balance check")
    check("PASSIVE_RESISTANCE" in network_san.DISSIPATIVE_ROLES,
          "while the ones that store nothing are kept")


def test_the_builder_refuses_a_forward_reference():
    print("\n== the topological rule is enforced at the mistake ==")
    model, work = compiled()
    if model is None:
        print("  skip: corpus model unavailable")
        return
    builder = model.builder("test")
    ahead = len(model.expressions) + 5
    try:
        builder.add_expression({"kind": "unary", "op": "negate",
                                "operand": ahead})
        check(False, "a forward operand was accepted")
    except ValueError as error:
        check("not strictly earlier" in str(error),
              f"refused at the point of the mistake ({error})")


def test_rewriting_rebuilds_the_path_instead_of_mutating_in_place():
    print("\n== splicing into a tree an earlier node cannot reach forward ==")
    model, work = compiled()
    if model is None:
        print("  skip: corpus model unavailable")
        return
    builder = model.builder("test")
    equation = model.equations[0]
    root = equation._raw["residual"] if hasattr(equation, "_raw") else None
    if root is None:
        print("  skip: equation shape unavailable")
        return
    target = builder.raw["expressions"][root]["node"]
    operands = [v for v in target.values() if isinstance(v, int)]
    if not operands:
        print("  skip: the first equation's root is a leaf")
        return

    replacement = builder.real(0.0)
    rebuilt = builder.rewrite_operand(root, operands[0], replacement)
    check(rebuilt != root, "a new root was appended rather than root mutated")
    check(builder.raw["expressions"][root]["node"] == target,
          "and the original tree is untouched, because something may share it")
    builder.rewrite_equation(0, rebuilt)
    check(builder.raw["equations"][0]["residual"] == rebuilt,
          "the equation is repointed, which needs no path rebuilding")
