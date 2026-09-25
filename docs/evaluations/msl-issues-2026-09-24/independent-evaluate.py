#!/usr/bin/env python3
"""Bounded recall audit of the original seven LLM-report witness variants.

Run from the repository root with the in-tree packages on PYTHONPATH. This
script creates evidence, not production fixes. No synthetic replacement model
is credited as one of these original MSL probes.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, is_dataclass
from enum import Enum
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import time

from modelsan.analysis.context import AnalysisContext
from modelsan.backends.rumoca import RumocaBackend
from modelsan.dae import load
from modelsan.fuzz.testcase import NOMINAL, TestCase
from modelsan.pipeline import Pipeline
from modelsan.sanitizers import (DEFAULT, DimensionSan, InitStaticSan,
                                NetworkSan, SanitizerRegistry, StructureSan)


CASES = [
    ("LLM-BUG-001", "firstorder", "LLM_FirstOrderZero.mo",
     "LLM_FirstOrderNominal", "LLM_FirstOrderZero", "dut.T", 0.1),
    ("LLM-BUG-002", "critical-blocks", "LLM_BlocksCriticalDampingOrderZero.mo",
     "LLM_BlocksCriticalDampingOrderTwo", "LLM_BlocksCriticalDampingOrderZero", "dut.n", 0.1),
    ("LLM-BUG-002", "critical-clocked", "LLM_CriticalDampingOrderZero.mo",
     "LLM_CriticalDampingOrderTwo", "LLM_CriticalDampingOrderZero", "dut.n", 0.1),
    ("LLM-BUG-003", "thyristor-itm", "LLM_ThyristorITMZero.mo",
     "LLM_ThyristorITMNominal", "LLM_ThyristorITMZero", "dut.ITM", 0.001),
    ("LLM-BUG-003", "thyristor-ih", "LLM_ThyristorITMZero.mo",
     "LLM_ThyristorITMNominal", "LLM_ThyristorIHZero", "dut.IH", 0.001),
    ("LLM-BUG-004", "pwm", "LLM_SignalPWMFrequencyZero.mo",
     "LLM_SignalPWMFrequencyNominal", "LLM_SignalPWMFrequencyZero", "dut.f", 0.01),
    ("LLM-BUG-005", "transformer", "LLM_CompareTransformersRatioZero.mo",
     "LLM_CompareTransformersRatioNominal", "LLM_CompareTransformersRatioZero", "n", 0.1),
]


def encode(value):
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (set, frozenset)):
        return sorted(value)
    return repr(value)


def save(path, value):
    path.write_text(json.dumps(value, default=encode, indent=2, allow_nan=True) + "\n")


def command(argv, cwd, stem, timeout=120, env=None):
    start = time.monotonic()
    with stem.with_suffix(".stdout").open("w") as out, stem.with_suffix(".stderr").open("w") as err:
        process = subprocess.Popen(argv, cwd=cwd, env=env, stdout=out, stderr=err,
                                   start_new_session=True)
        timed_out = False
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGKILL)
            code = process.wait()
    return {"argv": argv, "returncode": code, "timeout": timed_out,
            "seconds": round(time.monotonic() - start, 3),
            "stdout_file": str(stem.with_suffix(".stdout")),
            "stderr_file": str(stem.with_suffix(".stderr")),
            "stdout": stem.with_suffix(".stdout").read_text(errors="replace"),
            "stderr": stem.with_suffix(".stderr").read_text(errors="replace")}


def registry():
    result = SanitizerRegistry()
    for constructor in (*DEFAULT, StructureSan, InitStaticSan, DimensionSan, NetworkSan):
        result.register(constructor())
    return result


def compile_model(repo, output, executable, source, name, label):
    artifact = output / f"{label}.rbc"
    argv = [str(executable), "compile", str(source), "--model", name,
            "--source-root", str(repo / "target/msl/ModelicaStandardLibrary-4.1.0"),
            "--no-fold-parameter-bindings", "--emit-bitcode", str(artifact),
            "--cache-dir", str(output.parent / "cache")]
    result = command(argv, repo, output / f"{label}-compile")
    result["artifact"] = str(artifact) if result["returncode"] == 0 and artifact.exists() else None
    return result


def runtime_result(result, pipeline, model, context, case):
    return {"status": result.status, "failure": result.failure,
            "trace_samples": len(result.trace) if result.trace else 0,
            "metadata": result.backend_metadata,
            "findings": pipeline.judge(result, model, context, case)}


def analyze_artifact(artifact, executable, stop, parameter, output):
    model = load(artifact)
    context = AnalysisContext(model)
    reg = registry()
    findings, hints, errors = [], [], []
    for sanitizer in reg.static_analyzers():
        try:
            findings.extend(sanitizer.analyze(model, context))
        except Exception as error:
            errors.append({"sanitizer": sanitizer.name, "stage": "static", "error": repr(error)})
    for sanitizer in reg.hint_providers():
        try:
            hints.extend(sanitizer.hints(model, context))
        except Exception as error:
            errors.append({"sanitizer": sanitizer.name, "stage": "hints", "error": repr(error)})
    result = {"model": model.name, "has_execution": model.has_execution,
              "static_findings": findings, "hints": hints, "analysis_errors": errors,
              "target_variable": [v._raw for v in model.variables if v.name == parameter]}
    backend = RumocaBackend(str(executable), t_end=stop, timeout=60)
    pipeline = Pipeline(reg, backend)
    try:
        failure = backend.prepare_from_artifact(Path(artifact))
        result["coverage"] = pipeline.plan(model, context).skipped_sanitizers()
        if failure:
            result["prepare_failure"] = runtime_result(failure, pipeline, model, context, NOMINAL)
        else:
            nominal = backend.run(NOMINAL)
            result["nominal"] = runtime_result(nominal, pipeline, model, context, NOMINAL)
            # Run even if baseline fails to expose the capability boundary; this
            # is NOT credited as causal runtime verification without a good pair.
            witness = TestCase(parameters={parameter: 0.0})
            trial = backend.run(witness)
            result["witness"] = runtime_result(trial, pipeline, model, context, witness)
            result["witness_causally_comparable"] = nominal.ok
        save(output / "analysis.json", result)
    finally:
        backend.close()
    return result


def omc_pair(repo, output, source, nominal, trigger, stop):
    work = output / "omc"
    work.mkdir()
    script = work / "pair.mos"
    script.write_text("\n".join([
        'setCommandLineOptions("--numProcs=1");',
        f'setModelicaPath("{repo}/target/msl/ModelicaStandardLibrary-4.1.0:" + getModelicaPath());',
        'loadModel(Modelica, {"4.1.0"});', f'loadFile("{source}");',
        'print("MSL " + getVersion(Modelica) + "\\n");',
        'print("CASE nominal\\n");',
        f'simulate({nominal}, stopTime={stop}, numberOfIntervals=10);',
        'print(getErrorString());', 'print("CASE trigger\\n");',
        f'simulate({trigger}, stopTime={stop}, numberOfIntervals=10);',
        'print(getErrorString());',
    ]) + "\n")
    env = {**os.environ, "CC": "gcc", "CXX": "g++", "OMP_NUM_THREADS": "1"}
    result = command(["omc", "--locale=C", str(script)], work, output / "omc-pair", env=env)
    result["result_files"] = re.findall(r'resultFile\s*=\s*"([^"]*)"', result["stdout"])
    result["successful_simulations"] = result["stdout"].count("The simulation finished successfully.")
    return result


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--output", type=Path, required=True)
    args.add_argument("--only", action="append")
    args.add_argument("--skip-omc", action="store_true")
    options = args.parse_args()
    repo = Path.cwd()
    executable = repo / "target/debug/rumoca"
    output = options.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    version = subprocess.run([str(executable), "--version"], capture_output=True, text=True).stdout.strip()
    summary = {"run_started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
               "dirty_tree": True, "binary_sha256": hashlib.sha256(executable.read_bytes()).hexdigest(),
               "version": version, "sanitizers": registry().names(), "cases": []}
    for report, name, file, nominal, trigger, parameter, stop in CASES:
        if options.only and name not in options.only:
            continue
        case_dir = output / name
        case_dir.mkdir()
        source = repo / "docs/llm/bugs/repro" / file
        case = {"report": report, "variant": name, "source": str(source),
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "nominal_model": nominal, "trigger_model": trigger,
                "parameter": parameter, "value": 0.0}
        print(f"{name}: compiling nominal", flush=True)
        case["nominal_compile"] = compile_model(repo, case_dir, executable, source, nominal, "nominal")
        print(f"{name}: compiling exact source trigger", flush=True)
        case["trigger_compile"] = compile_model(repo, case_dir, executable, source, trigger, "trigger")
        if case["nominal_compile"]["artifact"]:
            print(f"{name}: analyzing/running nominal artifact and runtime override", flush=True)
            case["analysis"] = analyze_artifact(case["nominal_compile"]["artifact"], executable,
                                                stop, parameter, case_dir)
        if case["trigger_compile"]["artifact"]:
            target = case_dir / "trigger-analysis"
            target.mkdir()
            print(f"{name}: analyzing/running exact-source artifact", flush=True)
            case["source_trigger_analysis"] = analyze_artifact(case["trigger_compile"]["artifact"],
                                                               executable, stop, parameter, target)
        if not options.skip_omc:
            print(f"{name}: OMC source-paired controls (serial)", flush=True)
            case["omc"] = omc_pair(repo, case_dir, source, nominal, trigger, stop)
        save(case_dir / "result.json", case)
        summary["cases"].append(case)
        save(output / "results.json", summary)
    print(f"Wrote {len(summary['cases'])} variants to {output}/results.json", flush=True)


if __name__ == "__main__":
    main()
