#!/usr/bin/env python3
"""Batched differential check: one OMC session for many models.

Loading MSL costs ~15 s and was being paid once per model. Checking
every model inside a single session is what makes the whole corpus reachable.
"""
import json, os, subprocess, sys, tempfile
from pathlib import Path

ROOT = "target/msl/ModelicaStandardLibrary-4.1.0"
RUMOCA = "./target/debug/rumoca"

def omc_batch(names, timeout=3600):
    # Load the SAME MSL the other tool sees. `loadModel(Modelica)` picks OMC's
    # bundled copy — 4.0.0 here against Rumoca's 4.1.0 — and every model added
    # since 4.0.0 then reads as "Class not found", which looks exactly like a
    # soundness disagreement and is not one.
    lines = ['loadFile("/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/package.mo"); getErrorString();']
    for n in names:
        lines.append(f'print("@@MODEL {n}\\n");')
        lines.append(f'checkModel({n}); getErrorString();')
    with tempfile.TemporaryDirectory() as work:
        script = Path(work) / "b.mos"
        script.write_text("\n".join(lines) + "\n")
        try:
            r = subprocess.run(["omc", str(script)], cwd=work, capture_output=True,
                               text=True, timeout=timeout,
                               env={**os.environ, "CC": "gcc"})
        except subprocess.TimeoutExpired as e:
            out = (e.stdout or "") + (e.stderr or "")
            if isinstance(out, bytes): out = out.decode(errors="replace")
            return parse(out)
        out = r.stdout + r.stderr
    return parse(out)

def parse(out):
    result = {}
    for chunk in out.split("@@MODEL ")[1:]:
        nl = chunk.find("\n")
        name, body = chunk[:nl].strip(), chunk[nl:]
        result[name] = ("completed successfully" in body, body.strip()[:400])
    return result

def main(listfile, outfile, limit):
    jobs = [l.split("\t") for l in Path(listfile).read_text().splitlines() if l.strip()]
    jobs = [(p, n) for p, n in jobs if n.startswith("Modelica.")][:limit]
    names = [n for _, n in jobs]
    print(f"omc: checking {len(names)} models in one session", flush=True)
    omc = omc_batch(names)
    print(f"omc: {len(omc)} verdicts", flush=True)

    rum = {}
    with tempfile.TemporaryDirectory() as work:
        art = Path(work) / "m.rbc"
        for i, (path, name) in enumerate(jobs, 1):
            if art.exists(): art.unlink()
            try:
                r = subprocess.run([RUMOCA, "compile", path, "--model", name,
                                    "--source-root", ROOT, "--emit-bitcode", str(art)],
                                   capture_output=True, text=True, timeout=180)
                rum[name] = (r.returncode == 0 and art.exists(), r.stderr[-300:])
            except Exception as e:
                rum[name] = (False, str(e)[:200])
            if i % 50 == 0: print(f"rumoca: {i}/{len(jobs)}", flush=True)

    stats = dict(checked=0, agree=0, rumoca_only=0, omc_only=0, both_reject=0, omc_missing=0)
    rows = []
    for name in names:
        if name not in omc:
            stats["omc_missing"] += 1; continue
        stats["checked"] += 1
        o_ok, o_msg = omc[name]
        r_ok, r_msg = rum.get(name, (False, "missing"))
        if r_ok and o_ok: stats["agree"] += 1
        elif r_ok and not o_ok:
            stats["rumoca_only"] += 1
            rows.append({"model": name, "kind": "accepts-what-omc-rejects", "omc": o_msg})
        elif o_ok and not r_ok:
            stats["omc_only"] += 1
            rows.append({"model": name, "kind": "rejects-what-omc-accepts", "rumoca": r_msg})
        else:
            stats["both_reject"] += 1
    Path(outfile).write_text(json.dumps({"stats": stats, "rows": rows}, indent=1))
    print(json.dumps(stats, indent=1), flush=True)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
