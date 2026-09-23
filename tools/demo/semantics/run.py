#!/usr/bin/env python3
"""The three binding cases, run end to end against a real compile.

Case A  unit/quantity alone is enough, and still works.
Case B  the declaring class supports a stronger claim than the unit could.
Case C  nothing in the model can say what the object is, and the user must.

Also shown, because they are the cases that decide whether the layer is
trustworthy: the false positive the class-level binding removes, the conflict
an inconsistent user mapping produces, and the ambiguity that binds nothing.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path[:0] = ["packages/rumoca-bitcode", "packages/modelsan"]

from modelsan.analysis import AnalysisContext                    # noqa: E402
from modelsan.dae import load                                    # noqa: E402
from modelsan.sanitizers import PhysicalSan                      # noqa: E402
from modelsan.semantics import SemanticBinder, SemanticConfig    # noqa: E402

HERE = Path(__file__).parent
RUMOCA = "./target/debug/rumoca"
MSL = "target/msl/ModelicaStandardLibrary-4.1.0"


def compile_model(path: Path, model: str, work: Path):
    artifact = work / f"{model}.rbc"
    done = subprocess.run(
        [RUMOCA, "compile", str(path), "--model", model,
         "--emit-bitcode", str(artifact), "--source-root", MSL],
        capture_output=True, text=True)
    if not artifact.exists():
        print(f"  could not compile {model}: {(done.stdout + done.stderr)[:200]}")
        return None
    return load(artifact)


def show(findings) -> None:
    if not findings:
        print("    (no findings)")
    for finding in findings:
        matched = finding.evidence.get("matched_by", {})
        detail = finding.evidence.get("required") or finding.evidence.get("role", "")
        print(f"    [{finding.severity.value:6}] {finding.kind:32} {detail}")
        if matched.get("semantic_role"):
            print(f"             via {matched['semantic_role']} "
                  f"({matched.get('binding_source')})")


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)

        print("== Case A: unit/quantity binding, declaring class not catalogued ==")
        model = compile_model(HERE / "CaseA.mo", "CaseA", work)
        if model:
            show(PhysicalSan().analyze(model, AnalysisContext(model)))
            print("    the quantity carries it; reported as an assumption")

        print("\n== Case B: the declaring class supports the stronger claim ==")
        print("    (Inertia, not Resistor: MSL documents R as 'allowed to be")
        print("     positive, zero, or negative', so no passive claim holds there)")
        model = compile_model(HERE / "CaseB.mo", "CaseB", work)
        if model:
            show(PhysicalSan().analyze(model, AnalysisContext(model)))

        print("\n== the false positive class-level binding removes ==")
        chua = compile_model(
            Path(MSL) / "Modelica 4.1.0/Electrical/Analog/Examples/ChuaCircuit.mo",
            "Modelica.Electrical.Analog.Examples.ChuaCircuit", work)
        if chua:
            binder = SemanticBinder()
            semantics = binder.bind(chua)
            for name in ("Nr.Ga", "Nr.Gb"):
                variable = next((v for v in chua.variables if v.name == name), None)
                if variable is None:
                    continue
                roles = semantics.role_names(variable.id)
                print(f"    {name}: quantity={variable.physical_quantity} "
                      f"unit={variable.unit} -> roles {sorted(roles)}")
            violations = [f for f in PhysicalSan().analyze(chua, AnalysisContext(chua))
                          if f.kind == "physical-invariant-violated"]
            print(f"    physical violations reported: {len(violations)} "
                  f"(quantity-only matching reported 2)")

        print("\n== Case C: only the user can say which rad/s is a wheel ==")
        model = compile_model(HERE / "CaseC.mo", "CaseC", work)
        if model:
            print("  without semantics.toml:")
            show(PhysicalSan().analyze(model, AnalysisContext(model)))
            print("  with semantics.toml:")
            config = SemanticConfig.load(HERE / "semantics.toml")
            show(PhysicalSan(config=config).analyze(model, AnalysisContext(model)))

            print("\n  a user mapping that contradicts the model:")
            conflicted = SemanticBinder(
                user_mappings={"w_fan": "automotive.wheel.radius"},
                origin="semantics.toml").bind(model)
            for conflict in conflicted.conflicts:
                print("    " + conflict.describe().replace("\n", "\n    "))

            # Only an *inferred* role can be ambiguous. A user glob matching
            # four wheels is one deliberate statement, not a guess, so it is
            # exempt; a name heuristic matching two candidates is exactly the
            # case that must refuse to pick one.
            print("\n  a role two objects could fill, inferred rather than stated:")
            ambiguous = SemanticBinder(heuristics=True).bind(model)
            for item in ambiguous.ambiguities:
                print("    " + item.describe().replace("\n", "\n    "))
            print(f"    get() returns "
                  f"{ambiguous.get('automotive.vehicle_speed')} — nothing is bound")
    return 0


if __name__ == "__main__":
    sys.exit(main())
