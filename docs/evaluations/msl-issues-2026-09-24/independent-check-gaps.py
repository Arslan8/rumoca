#!/usr/bin/env python3
"""Read-only discriminating checks for gaps uncovered by the recall run."""
import importlib.util
import json
from pathlib import Path
import subprocess

from modelsan.analysis.context import AnalysisContext
from modelsan.backends.rumoca import RumocaBackend
from modelsan.dae import load
from modelsan.divisor import build
from modelsan.fuzz.testcase import NOMINAL
from modelsan.pipeline import Pipeline


def main():
    spec = importlib.util.spec_from_file_location("audit", Path(__file__).with_name("independent-evaluate.py"))
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    repo = Path.cwd()
    original = repo / "target/msl-issue-evaluation-20260924/independent/run-01"
    output = original.parent / "discriminating-checks"
    output.mkdir(exist_ok=False)
    executable = repo / "target/debug/rumoca"
    result = {"omc_version": subprocess.check_output(["omc", "--version"], text=True).strip()}
    pwm = original / "pwm/nominal.rbc"
    model = load(pwm)
    backend = RumocaBackend(str(executable), t_end=.01, timeout=30)
    try:
        outcome = Pipeline(audit.registry(), backend).run(model, str(pwm), model.name)
        result["pwm_actual_pipeline"] = {
            "note": outcome.note, "executed": outcome.executed,
            "findings": [f for bug in outcome.database.bugs for f in bug.findings],
            "coverage": outcome.coverage,
        }
    finally:
        backend.close()
    critical = original / "critical-blocks/nominal.rbc"
    model = load(critical)
    environment = build(model)
    result["critical_contracts"] = []
    for variable in model.variables:
        if variable.name in ("dut.n", "dut.normalized", "dut.x"):
            result["critical_contracts"].append({"variable": variable._raw,
                "binding_expression": repr(variable.binding),
                "environment_declared_value": environment.values.get(variable.id)})
    backend = RumocaBackend(str(executable), t_end=.1, timeout=30)
    try:
        backend.prepare_from_artifact(critical)
        run = backend.run(NOMINAL)
        traces = {str(path.relative_to(backend._work.name)): path.read_text()
                  for path in Path(backend._work.name).glob("**/*.csv")}
        result["critical_trace_transport"] = {"status": run.status, "failure": run.failure,
                                              "csv_files": traces}
    finally:
        backend.close()
    result["transformer_without_instrumentation"] = audit.command([
        str(executable), "compile-bitcode", str(original / "transformer/nominal.rbc"),
        "--simulate", "--t-end", ".1", "--dt", ".01"], repo, output / "transformer-uninstrumented", timeout=30)
    audit.save(output / "results.json", result)
    print(output / "results.json")


if __name__ == "__main__":
    main()
