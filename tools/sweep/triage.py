#!/usr/bin/env python3
"""Turn raw sweep output into a bug-report-shaped summary."""
import json, sys
from collections import Counter, defaultdict
from pathlib import Path

def main(path, diff=None):
    d = json.load(open(path))
    st, findings, classes, risks = d["stats"], d["findings"], d.get("classes",{}), d.get("risks",[])
    print("="*66); print("CORPUS SWEEP"); print("="*66)
    for k,v in st.items(): print(f"  {k:<22} {v}")

    print("\n" + "="*66); print("COMPILE FAILURES BY DIAGNOSTIC CLASS"); print("="*66)
    for code,n in Counter(classes).most_common():
        tag = "  <-- PANIC, no diagnostic" if code=="PANIC" else ""
        print(f"  {n:>4}  {code}{tag}")

    print("\n" + "="*66); print("RUNTIME FINDINGS BY KIND"); print("="*66)
    runtime = [f for f in findings if not f["kind"].startswith("compile-")]
    for k,n in Counter(f["kind"] for f in runtime).most_common():
        print(f"  {n:>4}  {k}")

    print("\n" + "="*66); print("PARAMETER-TRIGGERED FAILURES (confirmed by simulation)"); print("="*66)
    conf = [f for f in runtime if f.get("trigger")]
    by_param = defaultdict(list)
    for f in conf:
        for p in f["trigger"]: by_param[p.split(".")[-1]].append(f["model"])
    print(f"  {len(conf)} confirmed across {len(set(f['model'] for f in conf))} models")
    for p,models in sorted(by_param.items(), key=lambda x:-len(x[1]))[:15]:
        print(f"    {len(models):>3}x  parameter `{p}`")

    print("\n" + "="*66); print("STATIC SINGULAR-PARAMETER RISKS"); print("="*66)
    print(f"  {len(risks)} risk sites across {len(set(r['model'] for r in risks))} models")
    print("  by shape:")
    for s,n in Counter(r["shape"] for r in risks).most_common(): print(f"    {n:>4}  {s}")
    print("  by declared bound:")
    nomin = sum(1 for r in risks if r["min"] is None)
    zero  = sum(1 for r in risks if r["min"] == 0.0)
    print(f"    {nomin:>4}  no min declared")
    print(f"    {zero:>4}  min = 0 (explicitly admits the fatal value)")

    if diff and Path(diff).exists():
        dd = json.load(open(diff))
        print("\n" + "="*66); print("DIFFERENTIAL vs OpenModelica"); print("="*66)
        for k,v in dd["stats"].items(): print(f"  {k:<22} {v}")
        sound = [r for r in dd["rows"] if r["kind"]=="accepts-what-omc-rejects"]
        print(f"\n  CANDIDATE SOUNDNESS BUGS (rumoca accepts, omc rejects): {len(sound)}")
        for r in sound[:10]: print(f"    {r['model']}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else None)
