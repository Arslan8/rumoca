#!/usr/bin/env python3
"""Cross-confirm every verified candidate, automatically.

Five confirmed findings against 147 verified candidates is a verification
backlog, not a detection limit. Confirming one by hand took several minutes;
this does the whole queue.

For each candidate it walks that candidate's models until it finds one Rumoca
can compile *and* whose declared configuration is clean, then applies the same
trigger. A candidate is:

  confirmed    both tools clean at declared values, both fail at the trigger
  excluded     Rumoca survives the trigger — the OMC failure is OMC's
  single-tool  no model of that candidate gives Rumoca a clean baseline

`single-tool` is not a verdict about the model, it is the absence of one.
"""
import json, subprocess, sys, tempfile
from pathlib import Path

RUMOCA = "./target/debug/rumoca"
ROOTS = ["target/msl/ModelicaStandardLibrary-4.1.0",
         "target/corpus/ModelicaStandardLibrary-4.1.0"]
FAIL = ("simulation-failure", "DAE structural", "below-min", "above-max")


def paths() -> dict[str, str]:
    out = {}
    for line in Path("tools/sweep/ALL.list").read_text().splitlines():
        parts = line.split("\t")
        if len(parts) > 1:
            out[parts[1].strip()] = parts[0]
    return out


_COMPLETE: dict[str, bool] = {}


def exported_completely(artifact: Path) -> bool:
    """Whether the artifact represents the whole model.

    Bitcode v1 marks expressions it cannot carry as `Unsupported`. A model
    holding any of them is a *different* model from the one the other tool ran,
    so its surviving a trigger is not evidence the trigger is benign — it may
    simply never have evaluated the equation.

    Without this guard, three of the highest-reach findings were excluded on
    models carrying 44, 12 and 11 unsupported expressions.
    """
    key = str(artifact)
    if key in _COMPLETE:
        return _COMPLETE[key]
    try:
        from rumoca_bitcode import Model, Unsupported
        model = Model.load(artifact)
        complete = not any(isinstance(e, Unsupported) for e in model.expressions)
    except Exception:
        complete = False
    _COMPLETE[key] = complete
    return complete


_COMPILED: dict[str, Path | None] = {}


def compile_model(path: str, model: str, cache: Path, timeout: float) -> Path | None:
    """Compile once per model and reuse it.

    Candidates overlap heavily — 29 models mention `Inertia.J`, 17 mention
    `Mass.m`, and many are the same file. Recompiling per candidate was the
    dominant cost.
    """
    if model in _COMPILED:
        return _COMPILED[model]
    art = cache / f"{abs(hash(model)):x}.rbc"
    cmd = [RUMOCA, "compile", path, "--model", model, "--emit-bitcode", str(art)]
    for root in ROOTS:
        cmd += ["--source-root", root]
    try:
        subprocess.run(cmd, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        _COMPILED[model] = None
        return None
    _COMPILED[model] = art if art.exists() else None
    return _COMPILED[model]


_BASELINE: dict[str, str] = {}


def simulate(art: Path, override: tuple[str, float] | None, timeout: float) -> str:
    cmd = [RUMOCA, "compile-bitcode", str(art), "--simulate", "--check", "--t-end", "0.5"]
    if override:
        cmd += ["--param", f"{override[0]}={override[1]:g}"]
    try:
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "timeout"
    text = done.stdout + done.stderr
    if "not a tunable parameter" in text:
        return "no-such-parameter"
    return "fail" if any(marker in text for marker in FAIL) else "clean"


def confirm(candidate, triggers, model_paths, art, timeout, max_models=6) -> dict:
    """Try several of the candidate's models, not just the first judgeable one.

    A component defect does not have to break every circuit that uses it: zero
    capacitance is fatal in `ChuaCircuit` and harmless in `CauerLowPassAnalog`.
    Deciding a component from one topology is therefore wrong, and the first
    version of this function did exactly that — it excluded `Mass.m` and
    `Inertia.J`, both already confirmed by hand, because the first model it
    could judge happened to survive.

    A candidate is confirmed if *any* model confirms it, and excluded only if
    every model Rumoca could judge survived the trigger.
    """
    judged = []
    for model in candidate["models"]:
        if len(judged) >= max_models:
            break
        path = model_paths.get(model)
        trigger = triggers.get((model, candidate["parameter"]))
        if not path or trigger is None:
            continue
        built = compile_model(path, model, art, timeout)
        if built is None:
            continue
        if model not in _BASELINE:
            _BASELINE[model] = simulate(built, None, timeout)
        if _BASELINE[model] != "clean":
            continue  # Rumoca cannot judge this model; try the next
        verdict = simulate(built, trigger, timeout)
        if verdict == "no-such-parameter":
            continue
        # Asymmetric on purpose. A partial export that *fails* still failed
        # because of the trigger — the baseline was clean and only that value
        # changed. A partial export that *survives* proves nothing, because the
        # equation in question may not be in the artifact at all. So a failure
        # counts, and a survival is not recorded as a judgement.
        if verdict == "clean" and not exported_completely(built):
            continue
        judged.append((model, trigger, verdict))
        if verdict == "fail":
            return {"verdict": "confirmed", "via": model,
                    "trigger": f"{trigger[0]}={trigger[1]:g}",
                    "models_judged": len(judged)}
    # `excluded` requires a *complete* export that ran cleanly and survived.
    if judged:
        return {"verdict": "excluded", "via": judged[0][0],
                "trigger": f"{judged[0][1][0]}={judged[0][1][1]:g}",
                "models_judged": len(judged)}
    return {"verdict": "single-tool", "via": None, "trigger": None,
            "models_judged": 0}


def main(verified: str, sweep: str, out: str, limit: int):
    data = json.loads(Path(verified).read_text())
    candidates = [v for v in data["verified"] if v["core_library"]][:limit]

    triggers = {}
    for line in Path(sweep).read_text().splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        for f in row.get("findings", []):
            leaf = f["parameter"].rsplit(".", 1)[-1]
            triggers[(row["model"], leaf)] = (f["parameter"], f["value"])

    results, counts = [], {"confirmed": 0, "excluded": 0, "single-tool": 0}
    with tempfile.TemporaryDirectory() as work:
        art = Path(work)
        for i, candidate in enumerate(candidates, 1):
            got = confirm(candidate, triggers, paths(), art, 150)
            counts[got["verdict"]] += 1
            results.append({**candidate, **got})
            mark = {"confirmed": "OK ", "excluded": "XX ", "single-tool": ".. "}[got["verdict"]]
            print(f"{mark}{candidate['class'].split('.',1)[1]:52} {candidate['parameter']:14}"
                  f" {candidate['model_count']:3} models", flush=True)
            if i % 20 == 0:
                print(f"    -- {i}/{len(candidates)}  {counts}", flush=True)

    Path(out).write_text(json.dumps({"counts": counts, "results": results}, indent=1))
    print("\n" + json.dumps(counts, indent=1))


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--verified", required=True)
    p.add_argument("--sweep", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--limit", type=int, default=10**9)
    a = p.parse_args()
    main(a.verified, a.sweep, a.out, a.limit)
