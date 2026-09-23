#!/usr/bin/env python3
"""Round-trip audit: does every construct that exports also import?

BUG-008 was export and import disagreeing on one construct (enumerations) while
every hand-written fixture passed. Fidelity has to be asserted per construct,
so this runs the widest set of constructs available and reports any model that
exports cleanly and then fails to come back.
"""
import os, subprocess, sys, tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

RUMOCA = "./target/debug/rumoca"


def classify(path, model, roots, art, timeout=180):
    cmd = [RUMOCA, "compile", str(path), "--model", model, "--emit-bitcode", str(art)]
    for root in roots:
        cmd += ["--source-root", root]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "export-timeout", ""
    if out.returncode or not art.exists():
        return "does-not-export", _reason((out.stdout + out.stderr).replace("\x1b", ""))

    try:
        back = subprocess.run([RUMOCA, "compile-bitcode", str(art), "--summary"],
                              capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "import-timeout", ""
    text = (back.stdout + back.stderr).replace("\x1b", "")
    if "cannot rebuild" in text:
        detail = text.split("cannot rebuild", 1)[1]
        return "EXPORTS-BUT-CANNOT-IMPORT", " ".join(detail.split())[:200]
    if back.returncode:
        return "import-error", _reason(text)
    return "round-trips", ""


def _reason(text: str) -> str:
    """The compiler's own wording, with the noise stripped.

    Aggregating over 500 models only works if the same cause produces the same
    string, so the line is cut at the first identifier-looking token and the
    box-drawing characters the diagnostic renderer inserts are removed.
    """
    import re
    text = re.sub(r"\x1b\[[0-9;]*m", "", text)
    text = re.sub(r"[│─┌└├╭╰]", " ", text)
    for marker in ("cannot rebuild", "malformed bitcode", "error:", "Error:"):
        if marker in text:
            text = text.split(marker, 1)[1]
            break
    text = " ".join(text.split())
    text = re.sub(r"`[^`]*`", "`_`", text)
    text = re.sub(r"\b\d+\b", "N", text)
    return text[:150]


def default_jobs():
    """Bound by memory, not cores: a compile peaks near 1.8 GB, and a 24-way
    fan-out on this machine was an OOM rather than a speed-up."""
    cpu = os.cpu_count() or 4
    try:
        with open("/proc/meminfo") as f:
            fields = dict(
                (line.split(":")[0], int(line.split()[1])) for line in f if ":" in line
            )
        # `MemAvailable`, not `MemTotal`: the earlier 24-way fan-out sized
        # itself off total, ignored what the rest of the machine already held,
        # and was killed by the OOM reaper mid-sweep.
        free_kb = fields.get("MemAvailable", fields.get("MemTotal", 0))
        by_memory = max(1, int(free_kb / (3.0 * 1024 * 1024)))
    except Exception:
        by_memory = 4
    return max(1, min(cpu, by_memory, 16))


def _one(job):
    path, model, roots = job
    with tempfile.TemporaryDirectory() as work:
        return classify(path, model, roots, Path(work) / "m.rbc")


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("paths", nargs="+", help="model files, or list files with path<TAB>name")
    p.add_argument("--root", action="append", default=[])
    p.add_argument("--jobs", type=int, default=default_jobs())
    a = p.parse_args()

    jobs = []
    for entry in a.paths:
        path = Path(entry)
        if path.suffix == ".list":
            for line in path.read_text().splitlines():
                if line.strip():
                    parts = line.split("\t")
                    jobs.append((parts[0], parts[1]))
        else:
            jobs.append((str(path), path.stem))

    counts, bad = {}, []
    reasons: dict[str, int] = {}
    # `executor.map` streams results in input order, so the report is
    # byte-comparable between a serial and a parallel run.
    with ProcessPoolExecutor(max_workers=a.jobs) as pool:
        for (path, model), (kind, detail) in zip(
            jobs, pool.map(_one, [(path, model, a.root) for path, model in jobs])
        ):
            counts[kind] = counts.get(kind, 0) + 1
            if detail and kind != "round-trips":
                reasons[f"{kind}: {detail}"] = reasons.get(f"{kind}: {detail}", 0) + 1
            if kind == "EXPORTS-BUT-CANNOT-IMPORT":
                bad.append((model, detail))
                print(f"### {model}\n    {detail}", flush=True)

    print("\n=== round-trip audit ===")
    for kind, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {n:4}  {kind}")
    # Grouped by outcome, not pooled: `does-not-export` is a compiler
    # limitation and `import-error` is a bitcode gap, and the first is common
    # enough to hide every instance of the second in one ranked list.
    for kind in sorted({r.split(":", 1)[0] for r in reasons}):
        rows = [(r.split(": ", 1)[1], n) for r, n in reasons.items()
                if r.startswith(kind + ":")]
        print(f"\n=== why {kind}, most common first ===")
        for reason, n in sorted(rows, key=lambda kv: -kv[1])[:20]:
            print(f"  {n:4}  {reason}")
    print(f"\n{len(bad)} construct(s) export but cannot import")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
