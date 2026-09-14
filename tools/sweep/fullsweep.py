#!/usr/bin/env python3
"""Run every ModelSan detector over a corpus and record everything."""
import json, re, subprocess, sys, tempfile, time
from pathlib import Path
sys.path[:0] = ["packages/rumoca-bitcode", "packages/modelsan"]
from rumoca_bitcode import Model
from modelsan.analysis import (declared_ranges, find_domain_sites, find_singular_risks,
                               incomplete, search_knobs)
from modelsan.mutate import candidates, minimize
from modelsan.runner import export, run
from modelsan import differential as diff

RUMOCA = "./target/debug/rumoca"

DIAG = re.compile(r"\[(E[A-Z]+\d+|W[A-Z]+\d+)\]")

def classify(err: str) -> str:
    """Bucket a compile failure by its diagnostic code, or by shape."""
    codes = DIAG.findall(err)
    if codes: return codes[0]
    if "panicked" in err: return "PANIC"
    if "unsupported semantic owner" in err: return "unsupported-owner"
    if "resolve/parse failed" in err: return "resolve-parse"
    if "not found" in err: return "model-not-found"
    return "other"

def sweep(jobs, roots, t_end, max_trials, timeout, do_diff, diff_limit):
    st = {k:0 for k in ("total","compiled","compile_failed","partial","panics",
                        "no_props","searched","fails_nominally","failures",
                        "diff_checked","diff_disagree")}
    findings, classes, risk_rows = [], {}, []
    with tempfile.TemporaryDirectory() as work:
        art = Path(work)/"m.rbc"
        for path, name in jobs:
            st["total"] += 1
            if art.exists(): art.unlink()
            try:
                export(RUMOCA, Path(path), name, art, roots)
            except Exception as e:
                st["compile_failed"] += 1
                cls = classify(str(e))
                if cls == "PANIC": st["panics"] += 1
                classes[cls] = classes.get(cls, 0) + 1
                findings.append({"model":name,"kind":"compile-"+cls,
                                 "detail":str(e).strip()[-220:],"trigger":{}})
                continue
            st["compiled"] += 1
            try: model = Model.load(art)
            except Exception: st["compile_failed"] += 1; continue
            gaps = incomplete(model)
            if gaps: st["partial"] += 1

            risks = find_singular_risks(model)
            for r in risks:
                risk_rows.append({"model":name,"param":r.parameter.name,"shape":r.shape,
                                  "min":r.declared_min,"source":r.source})

            sites, ranges = find_domain_sites(model), declared_ranges(model)
            knobs = search_knobs(model, sites)
            if not knobs and not ranges:
                st["no_props"] += 1
            else:
                base = run(RUMOCA, art, {}, t_end=t_end, timeout=timeout)
                if not base.ok and base.kind != "tool-error":
                    st["fails_nominally"] += 1
                    findings.append({"model":name,"kind":"fails-nominally",
                                     "detail":base.detail[:220],"trigger":{}})
                else:
                    st["searched"] += 1
                    for cand in candidates(knobs)[:max_trials]:
                        out = run(RUMOCA, art, cand.assignment, t_end=t_end, timeout=timeout)
                        if out.ok or out.kind == "tool-error": continue
                        minimal = minimize(cand.assignment,
                            lambda t: not run(RUMOCA, art, t, t_end=t_end, timeout=timeout).ok)
                        findings.append({"model":name,"kind":out.kind,
                                         "detail":out.detail[:220],"trigger":minimal,
                                         "partial":bool(gaps)})
                        st["failures"] += 1
                        break

            if do_diff and st["diff_checked"] < diff_limit and name.startswith("Modelica."):
                st["diff_checked"] += 1
                omc = diff.omc_check(name, timeout=120)
                for d in diff.compare_acceptance(name, True, omc):
                    st["diff_disagree"] += 1
                    findings.append({"model":name,"kind":"diff-"+d.kind,
                                     "detail":d.detail[:300],"trigger":{}})
    return st, findings, classes, risk_rows

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--list", required=True); p.add_argument("--root", action="append", default=[])
    p.add_argument("--max-trials", type=int, default=14); p.add_argument("--t-end", type=float, default=0.5)
    p.add_argument("--timeout", type=float, default=25); p.add_argument("--out", required=True)
    p.add_argument("--diff", action="store_true"); p.add_argument("--diff-limit", type=int, default=0)
    a = p.parse_args()
    jobs = []
    for line in Path(a.list).read_text().splitlines():
        if not line.strip(): continue
        parts = line.split("\t"); jobs.append((parts[0], parts[1] if len(parts)>1 else None))
    t0 = time.time()
    st, f, c, r = sweep(jobs, a.root, a.t_end, a.max_trials, a.timeout, a.diff, a.diff_limit)
    st["seconds"] = round(time.time()-t0, 1)
    Path(a.out).write_text(json.dumps({"stats":st,"findings":f,"classes":c,"risks":r}, indent=1))
    print(json.dumps({"stats":st,"classes":c,"risk_count":len(r)}, indent=1))
