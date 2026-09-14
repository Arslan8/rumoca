#!/usr/bin/env python3
"""Cross-confirm each finding in OpenModelica before reporting it.

A failure in one tool is ambiguous: it can be a defect in the model, or a gap
in that tool. `Inductor.L = 0` looked like a strong MSL finding and could just
as easily have been Rumoca failing to re-index a degenerate equation — the only
way to tell is to ask a second, independent implementation.

A finding is reportable when, in *both* tools, the model runs at its declared
values and fails at the value its own declaration permits.
"""
import json, os, re, subprocess, sys, tempfile
from pathlib import Path

MSL = ("/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/"
       "Modelica 4.1.0/package.mo")
# ModelicaTest lives beside its own Modelica copy; loading the pair together
# keeps one library version in scope for both.
CORPUS = "/data/mrumoca/rumoca/target/corpus/ModelicaStandardLibrary-4.1.0"
MODELICA_TEST = f"{CORPUS}/ModelicaTest/package.mo"
OK = re.compile(r'resultFile = "(?!")[^"]+"')


def omc_batch(cases, t_end, out_dir, timeout):
    """Run every (model, override) case in one OMC session.

    `cases` is [(tag, model, override_or_None)]; None means the declared
    configuration, which is the baseline each finding is judged against.
    """
    needs_test = any(model.startswith("ModelicaTest.") for _, model, _ in cases)
    if needs_test:
        lines = [f'loadFile("{CORPUS}/Modelica/package.mo"); getErrorString();',
                 f'loadFile("{MODELICA_TEST}"); getErrorString();']
    else:
        lines = [f'loadFile("{MSL}"); getErrorString();']
    for i, (_, model, override) in enumerate(cases):
        flags = f', simflags="-override {override}"' if override else ""
        lines.append(f'print("@@CASE {i}\\n");')
        lines.append(
            f'simulate({model}, stopTime={t_end}, numberOfIntervals=20,'
            f' fileNamePrefix="c{i}"{flags}); getErrorString();'
        )
    script = out_dir / "cross.mos"
    script.write_text("\n".join(lines) + "\n")
    try:
        done = subprocess.run(["omc", str(script)], cwd=out_dir, capture_output=True,
                              text=True, timeout=timeout,
                              env={**os.environ, "CC": "gcc"})
        text = done.stdout + done.stderr
    except subprocess.TimeoutExpired as expired:
        text = (expired.stdout or "") + (expired.stderr or "")
        if isinstance(text, bytes):
            text = text.decode(errors="replace")

    verdicts = {}
    for chunk in text.split("@@CASE ")[1:]:
        head, _, body = chunk.partition("\n")
        try:
            index = int(head.strip())
        except ValueError:
            continue
        verdicts[cases[index][0]] = bool(OK.search(body))
    return verdicts


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--findings", required=True, help="ALL.json from fullsweep.py")
    p.add_argument("--t-end", type=float, default=0.5)
    p.add_argument("--timeout", type=float, default=2400)
    p.add_argument("--out", required=True)
    a = p.parse_args()

    data = json.loads(Path(a.findings).read_text())
    findings = [
        f for f in data["findings"]
        if f.get("trigger") and f["model"].startswith(("Modelica.", "ModelicaTest."))
    ]

    cases = []
    for i, f in enumerate(findings):
        override = ",".join(f"{k}={v}" for k, v in f["trigger"].items())
        cases.append((f"{i}:base", f["model"], None))
        cases.append((f"{i}:trigger", f["model"], override))

    with tempfile.TemporaryDirectory() as work:
        verdicts = omc_batch(cases, a.t_end, Path(work), a.timeout)

    rows, counts = [], {"confirmed": 0, "omc-disagrees": 0, "omc-baseline-fails": 0,
                        "omc-no-verdict": 0}
    for i, f in enumerate(findings):
        base = verdicts.get(f"{i}:base")
        trigger = verdicts.get(f"{i}:trigger")
        if base is None or trigger is None:
            verdict = "omc-no-verdict"
        elif not base:
            verdict = "omc-baseline-fails"
        elif trigger:
            verdict = "omc-disagrees"
        else:
            verdict = "confirmed"
        counts[verdict] += 1
        rows.append({"model": f["model"], "trigger": f["trigger"],
                     "rumoca": f["detail"][:120], "verdict": verdict})
        print(f"{verdict:20} {f['model']}  {f['trigger']}", flush=True)

    Path(a.out).write_text(json.dumps({"counts": counts, "rows": rows}, indent=1))
    print("\n" + json.dumps(counts, indent=1))


if __name__ == "__main__":
    main()
