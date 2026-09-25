#!/usr/bin/env python3
"""Issue-derived upstream #4771 probe; never credits a compiler gap as a hit.

The original attached zip was unavailable. This paired wrapper exercises the
same public MSL call and reduced/full composition difference described in the
issue body; it does not claim to be the attachment. #4807 was not reproduced in that earlier run; see focused-results.md
for the subsequent discussion/source review.
"""
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
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "packages/rumoca-bitcode"), str(ROOT / "packages/modelsan")]

MODEL = """within;
model Upstream4771Full
  parameter Real p = 100000;
  parameter Real targetT = 300;
  parameter Real water = 0;
  parameter Real s = Modelica.Media.Air.MoistAir.s_pTX(p, targetT, {water, 1-water});
  Real T;
equation
  T = Modelica.Media.Air.MoistAir.temperature_psX(p, s, {water, 1-water});
end Upstream4771Full;

model Upstream4771Reduced
  parameter Real p = 100000;
  parameter Real targetT = 300;
  parameter Real water = 0;
  parameter Real s = Modelica.Media.Air.MoistAir.s_pTX(p, targetT, {water, 1-water});
  Real T;
equation
  T = Modelica.Media.Air.MoistAir.temperature_psX(p, s, {water});
end Upstream4771Reduced;
"""


def encode(value):
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, Enum):
        return value.value
    return str(value)


def write(path, value):
    path.write_text(json.dumps(value, default=encode, indent=2) + "\n")


def command(argv, cwd, output, timeout=60):
    env = {**os.environ, "CC": "gcc", "CXX": "g++", "RAYON_NUM_THREADS": "1", "OMP_NUM_THREADS": "1"}
    started = time.monotonic()
    with output.with_suffix(".stdout").open("w") as stdout, output.with_suffix(".stderr").open("w") as stderr:
        process = subprocess.Popen(argv, cwd=cwd, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
        try:
            exit_code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
            exit_code = "timeout"
    return {"argv": list(map(str, argv)), "exit": exit_code,
            "seconds": round(time.monotonic() - started, 3),
            "stdout": output.with_suffix(".stdout").read_text(errors="replace"),
            "stderr": output.with_suffix(".stderr").read_text(errors="replace")}


def analyze(path, executable):
    from modelsan.analysis.context import AnalysisContext
    from modelsan.backends.rumoca import RumocaBackend
    from modelsan.dae import load
    from modelsan.fuzz.testcase import NOMINAL
    from modelsan.sanitizers import DEFAULT, DimensionSan, InitStaticSan, NetworkSan, StructureSan
    model = load(path)
    context = AnalysisContext(model)
    sanitizers = [cls() for cls in (*DEFAULT, DimensionSan, InitStaticSan, NetworkSan, StructureSan)]
    result = {"findings": [], "errors": []}
    for sanitizer in sanitizers:
        if hasattr(sanitizer, "analyze"):
            try:
                result["findings"].extend(sanitizer.analyze(model, context))
            except Exception as error:
                result["errors"].append({"sanitizer": sanitizer.name, "error": repr(error)})
    backend = RumocaBackend(str(executable), t_end=.01, timeout=30)
    try:
        run = backend.prepare_from_artifact(path)
        if run is None:
            run = backend.run(NOMINAL)
        result["runtime"] = {"status": run.status, "failure": run.failure,
                             "metadata": run.backend_metadata, "findings": []}
        for sanitizer in sanitizers:
            if hasattr(sanitizer, "observe"):
                result["runtime"]["findings"].extend(sanitizer.observe(run.observations, model, context, NOMINAL))
    finally:
        backend.close()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    source = output / "Upstream4771.mo"
    source.write_text(MODEL)
    executable = ROOT / "target/debug/rumoca"
    library = ROOT / "target/msl/ModelicaStandardLibrary-4.1.0"
    local_files = [library / "Modelica 4.1.0/Media/Air/MoistAir.mo",
                   library / "Modelica 4.1.0/Math/Nonlinear.mo"]
    results = {"issue": "https://github.com/modelica/ModelicaStandardLibrary/issues/4771",
               "date": "2026-09-24", "reproducer_kind": "issue-body-derived; attachment unavailable",
               "model_source": MODEL, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
               "rumoca_binary_sha256": hashlib.sha256(executable.read_bytes()).hexdigest(),
               "library_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in local_files},
               "omc_version": subprocess.check_output(["omc", "--version"], text=True).strip(),
               "cases": []}
    for name in ("Upstream4771Full", "Upstream4771Reduced"):
        artifact = output / f"{name}.rbc"
        result = {"model": name}
        print(f"Compiling {name}", flush=True)
        result["compile"] = command([str(executable), "compile", str(source), "--model", name,
            "--no-fold-parameter-bindings", "--source-root", str(library),
            "--cache-dir", str(output / "cache"), "--emit-bitcode", str(artifact)], ROOT, output / name)
        if result["compile"]["exit"] == 0 and artifact.exists():
            result["analysis"] = analyze(artifact, executable)
        else:
            result["sanitizer_status"] = "blocked-before-artifact; compiler failure is not issue detection"
        results["cases"].append(result)
        write(output / "results.json", results)
    work = output / "omc"
    work.mkdir()
    script = work / "pair.mos"
    script.write_text("\n".join([
        'setCommandLineOptions("--numProcs=1");',
        f'setModelicaPath("{library}:" + getModelicaPath());',
        'loadModel(Modelica, {"4.1.0"});', f'loadFile("{source}");',
        'print("MSL " + getVersion(Modelica) + "\\n");',
        'print("CASE full\\n");',
        'simulate(Upstream4771Full, stopTime=0.01, numberOfIntervals=10, outputFormat="csv");',
        'print(getErrorString());', 'print("CASE reduced\\n");',
        'simulate(Upstream4771Reduced, stopTime=0.01, numberOfIntervals=10, outputFormat="csv");',
        'print(getErrorString());',
    ]) + "\n")
    print("Running OMC full/reduced composition controls", flush=True)
    results["omc"] = command(["omc", "--locale=C", str(script)], work, output / "omc-pair")
    results["omc"]["result_files"] = re.findall(r'resultFile\s*=\s*"([^"]*)"', results["omc"]["stdout"])
    results["omc"]["successes"] = results["omc"]["stdout"].count("The simulation finished successfully.")
    write(output / "results.json", results)
    print(output / "results.json", flush=True)


if __name__ == "__main__":
    main()
