#!/usr/bin/env python3
"""Trajectory differential: Rumoca against OpenModelica on models both accept.

Acceptance agreement is a weak signal — two tools can agree a model is valid and
still integrate it to different answers. This compares the numbers.

Rumoca reports only declared trace points, so each artifact is instrumented with
trace_all.py first. OMC simulations run in one session; loading MSL costs ~15 s
and there is no reason to pay it per model.
"""
import csv, json, math, os, subprocess, sys, tempfile
from collections import defaultdict
from pathlib import Path

sys.path[:0] = ["packages/rumoca-bitcode", "packages/modelsan"]
from modelsan.legacy.differential import Disagreement, OmcResult

RUMOCA = "./target/debug/rumoca"
TRACE_ALL = "examples/bitcode-passes/trace_all.py"


def rumoca_run(path, name, roots, art_dir, t_end, intervals, timeout):
    """Compile -> instrument -> simulate. Returns (names, times, rows) or None."""
    raw, traced, csv_out = (art_dir / f"{n}" for n in ("m.rbc", "t.rbc", "t.csv"))
    for f in (raw, traced, csv_out):
        if f.exists():
            f.unlink()
    cmd = [RUMOCA, "compile", str(path), "--model", name, "--emit-bitcode", str(raw)]
    for root in roots:
        cmd += ["--source-root", root]
    if subprocess.run(cmd, capture_output=True, timeout=timeout).returncode or not raw.exists():
        return None
    env = {**os.environ, "PYTHONPATH": "packages/rumoca-bitcode:packages/modelsan"}
    if subprocess.run([sys.executable, TRACE_ALL, str(raw), "-o", str(traced), "--quiet"],
                      capture_output=True, env=env, timeout=timeout).returncode:
        return None
    if subprocess.run([RUMOCA, "compile-bitcode", str(traced), "--simulate",
                       "--t-end", str(t_end), "--trace-out", str(csv_out)],
                      capture_output=True, timeout=timeout).returncode or not csv_out.exists():
        return None

    # Long format: time,trace_id,connection,variable,quantity,unit,value
    series = defaultdict(dict)
    with csv_out.open() as handle:
        for row in csv.DictReader(handle):
            try:
                series[row["variable"]][float(row["time"])] = float(row["value"])
            except ValueError:
                continue
    if not series:
        return None
    times = sorted(next(iter(series.values())))
    names = sorted(series)
    return names, times, [[series[n].get(t, float("nan")) for t in times] for n in names]


def omc_batch(jobs, t_end, intervals, out_dir, timeout):
    """Simulate every model in one OMC session; return {model: OmcResult}.

    `jobs` is [(path, name)]. MSL models come from the loaded 4.1.0 tree;
    anything else has to be loaded from its own file first.
    """
    # Same MSL as Rumoca; see the note in diffbatch.py.
    lines = ['loadFile("/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/package.mo"); getErrorString();']
    for path, name in jobs:
        if not name.startswith("Modelica."):
            lines.append(f'loadFile("{Path(path).resolve()}"); getErrorString();')
    names = [n for _, n in jobs]
    for i, name in enumerate(names):
        lines.append(f'print("@@MODEL {name}\\n");')
        lines.append(
            f'simulate({name}, stopTime={t_end}, numberOfIntervals={intervals},'
            f' outputFormat="csv", fileNamePrefix="m{i}");'
        )
        lines.append("getErrorString();")
    script = out_dir / "batch.mos"
    script.write_text("\n".join(lines) + "\n")
    try:
        subprocess.run(["omc", str(script)], cwd=out_dir, capture_output=True,
                       text=True, timeout=timeout, env={**os.environ, "CC": "gcc"})
    except subprocess.TimeoutExpired:
        pass

    results = {}
    for i, name in enumerate(names):
        result = out_dir / f"m{i}_res.csv"
        if not result.exists():
            results[name] = OmcResult(accepted=False, message="no result file")
            continue
        columns = defaultdict(list)
        with result.open() as handle:
            reader = csv.reader(handle)
            header = next(reader, None)
            if not header:
                results[name] = OmcResult(accepted=False, message="empty result")
                continue
            for row in reader:
                for key, cell in zip(header, row):
                    try:
                        columns[key].append(float(cell))
                    except ValueError:
                        columns[key].append(float("nan"))
        times = columns.pop("time", [])
        results[name] = OmcResult(accepted=True, trajectory=dict(columns), times=times)
    return results


def compare_scaled(names, times, data, omc, *, rtol, atol, max_reports=3):
    """Compare on each signal's own scale, not its instantaneous value.

    Judging a decaying quantity by pointwise relative error reports a finding
    every time it passes through zero: `damper1.f` at 8.3e-4 against 9.4e-4 is
    a 12% relative difference and a 1.1e-4 absolute one, on a force whose range
    over the run is order 1. Scaling the tolerance by the larger of the two
    trajectories' own magnitudes is what makes the threshold mean the same
    thing for every variable.
    """
    found = []
    for name in names:
        if len(found) >= max_reports:
            break
        if name not in omc.trajectory:
            continue
        left = data[names.index(name)]
        right = omc.trajectory[name]
        scale = max((abs(v) for v in left if not math.isnan(v)), default=0.0)
        scale = max(scale, max((abs(v) for v in right if not math.isnan(v)), default=0.0))
        limit = atol + rtol * scale
        for index, time in enumerate(times):
            if index >= len(left) or not omc.times:
                break
            nearest = min(range(len(omc.times)), key=lambda k: abs(omc.times[k] - time))
            if abs(omc.times[nearest] - time) > 1e-6 or nearest >= len(right):
                continue
            a, b = left[index], right[nearest]
            if math.isnan(a) and math.isnan(b):
                continue
            if math.isnan(a) != math.isnan(b):
                found.append(Disagreement(
                    "nan-disagreement",
                    "one implementation produced NaN and the other did not",
                    name, time, a, b))
                break
            if abs(a - b) > limit:
                found.append(Disagreement(
                    "trajectory-divergence",
                    f"|difference| {abs(a - b):.3g} exceeds {limit:.3g}"
                    f" (rtol={rtol:g} of signal scale {scale:.3g})",
                    name, time, a, b))
                break
    return found


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--list", required=True)
    p.add_argument("--root", action="append", default=[])
    p.add_argument("--t-end", type=float, default=1.0)
    p.add_argument("--intervals", type=int, default=50)
    p.add_argument("--timeout", type=float, default=180)
    p.add_argument("--limit", type=int, default=10**9)
    p.add_argument("--out", required=True)
    # Rumoca exposes no solver-tolerance flag, so a small gap cannot be
    # attributed to either tool: two integrators at their own defaults differ
    # by ~0.1% on smooth states and that is not a defect. Only a qualitative
    # gap is reportable. See docs/toolbugs/LIMITATION-002-no-solver-tolerance-control.md.
    p.add_argument("--rtol", type=float, default=0.05)
    p.add_argument("--atol", type=float, default=1e-6)
    a = p.parse_args()

    jobs = [l.split("\t") for l in Path(a.list).read_text().splitlines() if l.strip()]
    jobs = [(x[0], x[1]) for x in jobs][: a.limit]

    stats = dict(total=0, rumoca_ran=0, omc_ran=0, compared=0,
                 agree=0, diverged=0, no_common=0)
    rows = []
    with tempfile.TemporaryDirectory() as work:
        work_dir = Path(work)
        art_dir = work_dir / "art"
        art_dir.mkdir()

        rum = {}
        for i, (path, name) in enumerate(jobs, 1):
            stats["total"] += 1
            try:
                got = rumoca_run(path, name, a.root, art_dir, a.t_end, a.intervals, a.timeout)
            except Exception:
                got = None
            if got:
                rum[name] = got
                stats["rumoca_ran"] += 1
            if i % 25 == 0:
                print(f"rumoca: {i}/{len(jobs)} ({stats['rumoca_ran']} simulated)", flush=True)

        if not rum:
            Path(a.out).write_text(json.dumps({"stats": stats, "rows": rows}, indent=1))
            print(json.dumps(stats, indent=1))
            return

        print(f"omc: simulating {len(rum)} models in one session", flush=True)
        omc = omc_batch([(p, n) for p, n in jobs if n in rum],
                        a.t_end, a.intervals, work_dir, a.timeout * 4)

        for name, (names, times, data) in rum.items():
            result = omc.get(name)
            if not result or not result.accepted:
                continue
            stats["omc_ran"] += 1
            common = [n for n in names if n in result.trajectory]
            if not common:
                stats["no_common"] += 1
                continue
            stats["compared"] += 1
            found = compare_scaled(names, times, data, result,
                                   rtol=a.rtol, atol=a.atol)
            if not found:
                stats["agree"] += 1
                continue
            stats["diverged"] += 1
            rows.append({
                "model": name,
                "common_variables": len(common),
                "disagreements": [
                    {"kind": d.kind, "variable": d.variable, "time": d.time,
                     "rumoca": d.rumoca, "omc": d.omc, "detail": d.detail}
                    for d in found
                ],
            })

    Path(a.out).write_text(json.dumps({"stats": stats, "rows": rows}, indent=1))
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()
