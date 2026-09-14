#!/usr/bin/env python3
"""Round-trip audit: does every construct that exports also import?

BUG-008 was export and import disagreeing on one construct (enumerations) while
every hand-written fixture passed. Fidelity has to be asserted per construct,
so this runs the widest set of constructs available and reports any model that
exports cleanly and then fails to come back.
"""
import subprocess, sys, tempfile
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
        return "does-not-export", ""

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
        return "import-error", " ".join(text.split())[-160:]
    return "round-trips", ""


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("paths", nargs="+", help="model files, or list files with path<TAB>name")
    p.add_argument("--root", action="append", default=[])
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
    with tempfile.TemporaryDirectory() as work:
        art = Path(work) / "m.rbc"
        for path, model in jobs:
            if art.exists():
                art.unlink()
            kind, detail = classify(path, model, a.root, art)
            counts[kind] = counts.get(kind, 0) + 1
            if kind == "EXPORTS-BUT-CANNOT-IMPORT":
                bad.append((model, detail))
                print(f"### {model}\n    {detail}", flush=True)

    print("\n=== round-trip audit ===")
    for kind, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {n:4}  {kind}")
    print(f"\n{len(bad)} construct(s) export but cannot import")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
