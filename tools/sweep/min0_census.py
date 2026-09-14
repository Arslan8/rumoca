#!/usr/bin/env python3
"""Census of the `min=0` idiom in Modelica source.

BUG-002 found that `Mass m(min=0)` admits a value the component cannot honour.
This asks how widespread that idiom is, and — the part that makes it a finding
rather than an observation — how often the *same library* writes the safe bound
for a parameter used the same way.
"""
import json, re, sys
from pathlib import Path

# A parameter declaration with modifiers, e.g.
#   parameter SI.Mass m(min=0, start=1) "Mass of the sliding mass";
DECL = re.compile(
    r"\bparameter\s+([\w.]+)\s+(\w+)\s*\(([^;]*?)\)\s*(?:=|\"|;)", re.S)
MIN = re.compile(r"\bmin\s*=\s*([^,)]+)")

def classify_bound(expr: str) -> str:
    e = expr.strip()
    if e in ("0", "0.0"):
        return "zero"
    if "eps" in e or "small" in e:
        return "guarded"
    return "other"

def guarded(body: str, name: str) -> bool:
    """Does the model exclude the degenerate value itself?

    MSL has two correct idioms besides tightening the bound: a structural
    branch (`if G > 0 then ... else V_m.re = 0`, EddyCurrent) and a guarded
    expression (`if rising > 0 then amplitude/rising else 0`, Logical). Both
    honour `min=0`, so neither is a finding.
    """
    n = re.escape(name)
    return bool(re.search(r"\b" + n + r"\s*(>|<>|>=)\s*0", body)
                or re.search(r"abs\s*\(\s*" + n + r"\s*\)\s*>", body))


def uses(body: str, name: str) -> set:
    """How `name` is used in equations. Divisor is the unambiguous case."""
    kinds = set()
    # `/ name` possibly parenthesised or with a component prefix
    if re.search(r"/\s*\(?\s*" + re.escape(name) + r"\b", body):
        kinds.add("divisor")
    # `name * der(...)` or `der(...) * name` - vanishing coefficient of a state
    if re.search(re.escape(name) + r"\s*\*\s*der\s*\(", body) or \
       re.search(r"der\s*\([^)]*\)\s*\*\s*" + re.escape(name) + r"\b", body):
        kinds.add("der-coefficient")
    return kinds

def scan(root: Path):
    rows = []
    for mo in sorted(root.rglob("*.mo")):
        try:
            text = mo.read_text(errors="replace")
        except OSError:
            continue
        # equations/algorithms only, so a default value isn't read as a use
        idx = text.find("equation")
        body = text[idx:] if idx >= 0 else ""
        for match in DECL.finditer(text):
            typ, name, mods = match.groups()
            m = MIN.search(mods)
            if not m:
                continue
            bound = classify_bound(m.group(1))
            if bound == "other":
                continue
            how = sorted(uses(body, name))
            rows.append({
                "file": str(mo.relative_to(root)),
                "type": typ, "param": name, "bound": bound,
                "uses": how,
                "guarded": guarded(body, name) if how else None,
            })
    return rows

if __name__ == "__main__":
    rows = scan(Path(sys.argv[1]))
    Path(sys.argv[2]).write_text(json.dumps(rows, indent=1))
    tot = {"zero": 0, "guarded": 0}
    used = {"zero": 0, "guarded": 0}
    unguarded = {"zero": 0, "guarded": 0}
    for r in rows:
        tot[r["bound"]] += 1
        if r["uses"]:
            used[r["bound"]] += 1
            if not r["guarded"]:
                unguarded[r["bound"]] += 1
    print(json.dumps({"declarations": tot, "used_in_unsafe_position": used,
                      "and_not_self_guarded": unguarded,
                      "rows": len(rows)}, indent=1))
