#!/usr/bin/env python3
"""ModelSan over OpenModelica: parameter search on models any front end can build.

One model per invocation so the corpus can be fanned out with xargs -P; each
build is independent and the builds dominate the cost.

Prints one JSON object per model on stdout.
"""
import json, sys, tempfile
from pathlib import Path

sys.path[:0] = ["packages/rumoca-bitcode", "packages/modelsan"]
from modelsan.omc_backend import build, probes, run, tier

MSL = ("/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/"
       "Modelica 4.1.0/package.mo")
CORPUS = "/data/mrumoca/rumoca/target/corpus/ModelicaStandardLibrary-4.1.0"


def libraries(model: str) -> list[str]:
    if model.startswith("ModelicaTest."):
        return [f"{CORPUS}/Modelica/package.mo", f"{CORPUS}/ModelicaTest/package.mo"]
    return [MSL]


def sweep_one(model: str, t_end: float, per_model: int, timeout: float) -> dict:
    out = {"model": model, "status": "", "trials": 0, "findings": []}
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        built = build(model, libraries(model), work, t_end)
        if not built.ok:
            out["status"] = "build-failed"
            out["detail"] = built.message[:200]
            return out
        out["parameters"] = len(built.parameters)

        # A finding is only attributable if the declared configuration works.
        base = run(built, {}, work, timeout)
        if not base.ok:
            out["status"] = "fails-nominally"
            out["detail"] = base.detail[:200]
            return out
        out["status"] = "searched"

        for parameter in built.parameters[:per_model]:
            for value, why in probes(parameter):
                out["trials"] += 1
                got = run(built, {parameter.name: value}, work, timeout)
                if got.ok:
                    continue
                out["findings"].append({
                    "parameter": parameter.name,
                    "value": value,
                    "declared_min": parameter.min,
                    "declared_start": parameter.start,
                    "tier": tier(parameter),
                    "claim": why,
                    "blamed": got.blamed,
                    "nonfinite": got.nonfinite,
                    "detail": got.detail,
                })
                break  # one probe per parameter is enough to establish it
    return out


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("model")
    p.add_argument("--t-end", type=float, default=0.5)
    p.add_argument("--per-model", type=int, default=60)
    p.add_argument("--timeout", type=float, default=90)
    a = p.parse_args()
    print(json.dumps(sweep_one(a.model, a.t_end, a.per_model, a.timeout)), flush=True)
