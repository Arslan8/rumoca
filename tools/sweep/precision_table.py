#!/usr/bin/env python3
"""Precision per stratum on one run, from whichever samples still apply.

A sample belongs to the run it was drawn from. When a fix changes what the
sanitizers report, the draws that *survive* into the new run are still a simple
random sample of the subset they survive into, so they stay usable; the ones
that no longer appear are dropped rather than scored, because a finding that is
not made cannot be right or wrong.

Where several samples cover the same stratum the largest surviving one is used.
Strata that are not defect claims --- a suppression, a proof of safety, an
explicit "unresolved" --- are listed and excluded from the weighted figure,
because scoring them either way would be wrong.

    tools/sweep/precision_table.py [run.jsonl]
"""
import collections
import json
import math
import sys

AS_JSON = "--json" in sys.argv[1:]
_positional = [a for a in sys.argv[1:] if not a.startswith("-")]
RUN = _positional[0] if _positional else "docs/runs/data/STATIC_AGGREGATE.jsonl"
SAMPLES=["SAMPLE.json","SAMPLE_SAT_DIVISORS.json",
         "SAMPLE_BOUND_AFTER_CONTRACTS.json",
         "SAMPLE_BOUND_AFTER_AGGREGATE.json",
         "SAMPLE_UNENFORCED_AFTER_CONTRACTS.json"]
NOT_A_CLAIM={"divisor-guarded-by-assertion","divisor-unreachable-under-witness",
             "divisor-zero-unresolved","divisor-zero-at-declared-values",
             "physical-zero-is-a-supported-limit","divisor-introduced-by-translation",
             "physical-rule-does-not-apply",
             "physical-inertia-tensor-undecided",
             "physical-intent-question"}
def tgt(e):
    if e.get("parameter"): return str(e["parameter"])
    for k in ("required","where"):
        w=str(e.get(k,"")).split()
        if w: return w[0]
    return ""
def wilson(k,n,z=1.96):
    if n==0: return (0.0,1.0)
    p=k/n; d=1+z*z/n
    c=(p+z*z/(2*n))/d
    s=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return (max(0.0,c-s), min(1.0,c+s))
cur=collections.Counter()
for line in open(RUN):
    r=json.loads(line)
    for f in r.get("findings",[]): cur[(r["model"],f["kind"],tgt(f["evidence"]))]+=1
sizes=collections.Counter()
for (_,k,_),n in cur.items(): sizes[k]+=n
# newest sample per kind wins
draws=collections.defaultdict(list)
for name in SAMPLES:
    for e in json.load(open("docs/runs/data/"+name)):
        key=(e["model"],e["kind"],e.get("target") or tgt(e["evidence"]))
        if key in cur: draws[(e["kind"],name)].append(e)
best={}
for (kind,name),items in draws.items():
    if kind not in best or len(items)>len(best[kind][1]): best[kind]=(name,items)
report={"run": RUN, "strata": [], "total": {}}
say = (lambda *a, **k: None) if AS_JSON else print
say(f"{'stratum':<38}{'pop':>6}{'n':>5}{'decl':>5}{'TP':>4}{'FP':>4}{'?':>4}"
    f"  precision      95% CI   sample")
say("-"*108)
total=weighted=low_t=high_t=0
for kind in sorted(sizes, key=lambda k:-sizes[k]):
    pop=sizes[kind]
    if kind in NOT_A_CLAIM:
        report["strata"].append({"kind": kind, "population": pop,
                                 "defect_claim": False})
        say(f"{kind:<38}{pop:>6}    —   —   —   —   not a defect claim"); continue
    total+=pop
    name,items=best.get(kind,("",[]))
    c=collections.Counter(e["verdict"] for e in items)
    judged=c["true-positive"]+c["false-positive"]
    p=c["true-positive"]/judged if judged else 0.0
    lo,hi=wilson(c["true-positive"],judged)
    weighted+=pop*p; low_t+=pop*lo; high_t+=pop*hi
    # How many *distinct declarations* the draws cover. Stratifying by finding
    # kind does not stratify by declaration: one stratum was once reported at
    # 100% on a sample that was twenty-nine copies of one parameter.
    distinct=len({(e.get('source') or '').strip() or e.get('target','') for e in items})
    report["strata"].append({
        "kind": kind, "population": pop, "defect_claim": True,
        "draws": len(items), "declarations": distinct,
        "true_positive": c["true-positive"], "false_positive": c["false-positive"],
        "undecidable": c["undecidable"], "precision": round(p*100, 1),
        "ci": [round(lo*100, 1), round(hi*100, 1)], "sample": name})
    say(f"{kind:<38}{pop:>6}{len(items):>5}{distinct:>5}"
        f"{c['true-positive']:>4}{c['false-positive']:>4}"
        f"{c['undecidable']:>4}  {p*100:>6.1f}%   [{lo*100:>5.1f},{hi*100:>6.1f}]  {name}")
say("-"*108)
report["total"]={"population": total, "precision": round(weighted/total*100, 1),
                 "ci": [round(low_t/total*100, 1), round(high_t/total*100, 1)]}
say(f"{'WEIGHTED TOTAL':<38}{total:>6}{'':>17}  {weighted/total*100:>6.1f}%   "
    f"[{low_t/total*100:>5.1f},{high_t/total*100:>6.1f}]")
if AS_JSON:
    print(json.dumps(report, indent=1))
