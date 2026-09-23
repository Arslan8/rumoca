#!/usr/bin/env python3
"""One report per static finding site, so no result from a corpus run is lost.

A corpus run produces tens of thousands of findings over hundreds of models.
Collapsed to a summary table they are unusable — nobody can act on "9288
physical-domain-unenforced" — and left in a JSONL in a temp directory they are
gone the moment the machine is cleaned.

So every distinct site gets a file: the declaration, its `file:line`, the claim
made about it, every model that reaches it, and the patch. A site is one
(declaration, parameter, claim) triple, which is one edit.

**These are candidates, not confirmed defects.** The separation is the whole
discipline of this project and collapsing it would turn 1247 sites into "1247
bugs" when 26 have been proven. Confirmed occurrences live in
`docs/verified bugs/` under their own IDs; these carry `SITE-` and say what
evidence they have and what they lack.
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

OUT = Path("docs/site-reports")

CLAIM = {
    "physical-domain-unenforced":
        ("nothing bounds this declaration at all",
         "No value has been observed breaking this. The declaration simply does "
         "not exclude one, and nothing else in the model does either."),
    "physical-bound-permits-zero":
        ("the declaration explicitly permits zero, via `min=0`",
         "Weaker than an absent bound, because `min=0` is the author stating "
         "that zero is allowed rather than failing to consider it — and for "
         "`IdealCommutingSwitch.Goff` the ideal off-state conductance really is "
         "zero. It is still recorded because `Mass.m(min=0)` has exactly this "
         "shape and zero provably breaks it in two tools (BUG-002). Which of "
         "the two a given site is cannot be decided statically."),
    "divisor-reachable-zero":
        ("a settable parameter reaches a denominator with nothing excluding zero",
         "Static reachability only. Whether zero actually breaks this model "
         "depends on topology — a vanishing divisor in an unused branch is "
         "harmless — so execution is the oracle."),
    "physical-invariant-violated":
        ("a declared value violates a physical invariant",
         "The value is fixed by the declaration and is outside the physical "
         "domain. Stronger than the others: no execution is needed to see that "
         "the declared number is wrong."),
    "divisor-zero-when-parameters-equal":
        ("a divisor vanishes when two parameters are equal",
         "No `min` can express a constraint *between* two parameters, so an "
         "assertion is the only mechanism available."),
}


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


def main() -> int:
    rows = [json.loads(l) for l in Path(sys.argv[1]).read_text().splitlines() if l.strip()]
    sites: dict[tuple, dict] = {}
    for row in rows:
        for finding in row["findings"]:
            evidence = finding["evidence"]
            predicate = evidence.get("required", "") or ""
            target = predicate.split()[0] if predicate else evidence.get("parameter", "?")
            parameter = target.rsplit(".", 1)[-1]
            key = (finding.get("source", "?"), parameter, finding["kind"])
            site = sites.setdefault(key, {
                "source": finding.get("source", "?"), "parameter": parameter,
                "kind": finding["kind"], "severity": finding["severity"],
                "models": set(), "targets": set(), "evidence": evidence,
                "sanitizer": finding["sanitizer"],
            })
            site["models"].add(row["model"])
            site["targets"].add(target)

    ordered = sorted(sites.values(),
                     key=lambda s: (-len(s["models"]), s["kind"], s["source"]))
    OUT.mkdir(parents=True, exist_ok=True)
    for stale in OUT.glob("SITE-*.md"):
        stale.unlink()

    index = []
    for number, site in enumerate(ordered, 1):
        headline, caveat = CLAIM.get(site["kind"], (site["kind"], ""))
        models = sorted(site["models"])
        targets = sorted(site["targets"])
        name = f"SITE-{number:04d}-{slugify(site['parameter'] + '-' + site['kind'])}.md"
        evidence = site["evidence"]
        matched = evidence.get("matched_by", {})

        rows_md = "\n".join(f"| `{m}` |" for m in models[:20])
        more = (f"\n\n…and {len(models) - 20} more; the full list is in "
                f"`docs/runs/data/`." if len(models) > 20 else "")

        body = f"""# SITE-{number:04d}: `{site['parameter']}` — {headline}

| | |
|---|---|
| **Declaration** | `{site['source']}` |
| **Parameter** | `{site['parameter']}` |
| **Reached as** | {", ".join(f"`{t}`" for t in targets[:4])}{" …" if len(targets) > 4 else ""} |
| **Finding** | `{site['kind']}` |
| **Severity** | {site['severity']} |
| **Sanitizer** | `{site['sanitizer']}` |
| **Models reaching it** | {len(models)} |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

{evidence.get('required') and f"`{evidence['required']}`" or headline}

{evidence.get('note', '')}

## What this evidence is, and is not

{caveat}

A confirmed occurrence of this class would live in
[`docs/verified bugs/`](../verified%20bugs/INSTANCES.md) with its own `BUG-` id
and a two-tool reproduction. This file has neither; it records a site the
analysis reached so the result is not lost between runs.

## How it was matched
"""
        # `static_eval.py` stringifies evidence values on write, so a nested
        # dict arrives as its repr. Both shapes are rendered rather than one
        # being assumed: a generator that crashes on last week's results is a
        # generator that cannot re-read the archive it exists to preserve.
        if isinstance(matched, dict) and matched:
            body += "\n" + "\n".join(
                f"- **{k}**: `{v}`" for k, v in matched.items()) + "\n"
        elif matched:
            body += f"\n- **matched by**: `{matched}`\n"
        else:
            for k in ("parameter", "shape", "path", "declared_min", "divisor_sites"):
                if k in evidence:
                    body += f"- **{k}**: `{evidence[k]}`\n"

        body += f"""
## Models that reach it

| Model |
|---|
{rows_md}{more}

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \\
  --out results.jsonl --keep-parameter-chains
```
"""
        (OUT / name).write_text(body)
        index.append((number, name, site, len(models)))

    by_kind = collections.Counter(s["kind"] for s in ordered)
    lines = [
        "# Static finding sites",
        "",
        f"**{len(ordered)} sites** from the full-corpus static run, one file each.",
        "",
        "Every one is a **candidate**. The oracle for these is execution, and",
        "they have not been through it. Confirmed occurrences live in",
        "[`INSTANCES.md`](../verified%20bugs/INSTANCES.md) under `BUG-` ids with",
        "a two-tool reproduction each.",
        "",
        "Reporting these as bugs is how 1247 sites would become \"1247 bugs\"",
        "when 26 have been proven. They are recorded because a site the analysis",
        "reached is worth keeping, not because reaching it settles anything.",
        "",
        "## By finding",
        "",
        "| Finding | Sites | What it means |",
        "|---|---|---|",
    ]
    for kind, count in by_kind.most_common():
        lines.append(f"| `{kind}` | {count} | {CLAIM.get(kind, ('?', ''))[0]} |")

    lines += ["", "## Sites, by how many models reach them", "",
              "| ID | Parameter | Declaration | Finding | Models |",
              "|---|---|---|---|---|"]
    for number, name, site, count in index:
        lines.append(f"| [SITE-{number:04d}]({name}) | `{site['parameter']}` | "
                     f"`{site['source']}` | `{site['kind']}` | {count} |")
    lines += ["", "## Regenerating", "",
              "```bash",
              "python3 tools/sweep/gen_site_reports.py docs/runs/data/STATIC_FINAL.jsonl",
              "```", ""]
    (OUT / "README.md").write_text("\n".join(lines))
    print(f"wrote {len(ordered)} site reports to {OUT}")
    for kind, count in by_kind.most_common():
        print(f"  {count:5}  {kind}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
