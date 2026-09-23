#!/usr/bin/env python3
"""One file per finding — every occurrence, not every fix site.

Three granularities now exist and they answer different questions:

    declaration-sites/  a declaration that permits an impossible value   911
    site-reports/       a fix site: one declaration, one claim          1075
    findings/instances/ one occurrence: this model, this instance      10942

A site says "`Inductor.mo:4` declares `L` unbounded". A finding says
"`ChuaCircuit` reaches it through `L.L`". The site is what you edit; the
finding is what you reproduce, and 608 of the 1075 sites are reached by exactly
one model, so most of the tail really is distinct work.

Every file states its tier. None of these is execution-confirmed: that is
`docs/verified bugs/`, which has 26.
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

OUT = Path("docs/findings/instances")

CLAIM = {
    "physical-domain-unenforced": "nothing bounds this declaration at all",
    "physical-bound-permits-zero": "the declaration explicitly permits zero (`min=0`)",
    "divisor-reachable-zero": "a settable parameter reaches a denominator, nothing excludes zero",
    "physical-invariant-violated": "the declared value is outside the physical domain",
    "divisor-zero-when-parameters-equal": "a divisor vanishes when two parameters are equal",
}

#: The kind that marks a finding as a known false positive.
#:
#: This replaced a hand-written list of four declarations, which was wrong about
#: two of them: `ConditionalHeatPort.T` and `Resistor.T_ref` are *parameters* a
#: user sets, and a negative absolute temperature there is a real defect. Only
#: `T_heatPort` and `HeatPort.T` are states, and the sanitizer now says so
#: itself rather than being told by a list someone has to keep correct.
KNOWN_FALSE_POSITIVE = "physical-runtime-invariant-unobserved"

def slug(text: str, limit: int = 40) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:limit]


def site_key(finding: dict) -> tuple:
    evidence = finding["evidence"]
    predicate = evidence.get("required", "") or ""
    target = predicate.split()[0] if predicate else evidence.get("parameter", "?")
    return (finding.get("source", "?"), target.rsplit(".", 1)[-1], finding["kind"])


def main() -> int:
    rows = [json.loads(l) for l in Path(sys.argv[1]).read_text().splitlines() if l.strip()]

    # Reproduce the site numbering so each finding can point at its fix site.
    sites: dict[tuple, dict] = {}
    for row in rows:
        for finding in row["findings"]:
            site = sites.setdefault(site_key(finding), {"models": set()})
            site["models"].add(row["model"])
    ordered = sorted(sites.items(), key=lambda kv: (-len(kv[1]["models"]), kv[0][2], kv[0][0]))
    # The site generator's own naming, reproduced so each finding links to the
    # file rather than to the index. Keeping the two in step is the price of
    # two generators over one dataset; the link check catches it if they drift.
    site_file = {
        key: f"SITE-{index:04d}-{slug(key[1] + '-' + key[2], 60)}.md"
        for index, (key, _) in enumerate(ordered, 1)
    }
    site_number = {key: index for index, (key, _) in enumerate(ordered, 1)}

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "by-model").mkdir(exist_ok=True)
    for stale in OUT.glob("FINDING-*.md"):
        stale.unlink()
    for stale in (OUT / "by-model").glob("*.md"):
        stale.unlink()

    # Deterministic order: model, then declaration, then parameter.
    flat = sorted(
        ((row["model"], finding) for row in rows for finding in row["findings"]),
        key=lambda pair: (pair[0], pair[1].get("source", ""), str(pair[1]["evidence"])),
    )

    per_model: dict[str, list] = collections.defaultdict(list)
    kinds = collections.Counter()
    noisy = 0

    for number, (model, finding) in enumerate(flat, 1):
        evidence = finding["evidence"]
        predicate = evidence.get("required", "") or ""
        target = predicate.split()[0] if predicate else evidence.get("parameter", "?")
        parameter = target.rsplit(".", 1)[-1]
        source = finding.get("source", "?")
        key = site_key(finding)
        number_of_site = site_number.get(key, 0)
        is_noise = finding["kind"] == KNOWN_FALSE_POSITIVE
        noisy += is_noise
        kinds[finding["kind"]] += 1

        name = f"FINDING-{number:05d}-{slug(model.split('.')[-1])}-{slug(parameter, 20)}.md"
        detail = "\n".join(
            f"| `{k}` | {v} |" for k, v in evidence.items() if k != "matched_by")
        matched = evidence.get("matched_by")
        caveat = ""
        if is_noise:
            caveat = (
                "\n> **Known false positive.** The invariant is a runtime "
                "property of a variable no user can set — a connector or\n"
                "> algebraic. True, and not a declaration defect. Kept because a "
                "precision figure needs its false positives\n"
                "> counted, not deleted.\n")

        (OUT / name).write_text(f"""# FINDING-{number:05d}: `{target}` in `{model.split('.')[-1]}`

| | |
|---|---|
| **Model** | `{model}` |
| **Reached as** | `{target}` |
| **Declaration** | `{source}` |
| **Parameter** | `{parameter}` |
| **Claim** | {CLAIM.get(finding['kind'], finding['kind'])} |
| **Kind** | `{finding['kind']}` |
| **Severity** | {finding['severity']} |
| **Sanitizer** | `{finding['sanitizer']}` |
| **Fix site** | [SITE-{number_of_site:04d}](../../site-reports/{site_file.get(key, "README.md")}) |
| **Status** | **candidate — not execution-confirmed** |
{caveat}
## Evidence

| key | value |
|---|---|
{detail}
{f"| `matched_by` | {matched} |" if matched else ""}

## What this is

One occurrence. The declaration at `{source}` is reached by this model through
`{target}`, and the analysis reached it statically — no value has been observed
breaking anything here.

The fix is at the declaration, not in this model. Other models reaching the same
declaration are separate files; the fix site groups them.

| Tier | Evidence | Where |
|---|---|---|
| confirmed | fails in two independent tools | [`INSTANCES.md`](../../verified%20bugs/INSTANCES.md) |
| **candidate** | **static analysis reached it** | **here** |
| latent | a declaration permits it | [`declaration-sites/`](../../declaration-sites/README.md) |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \\
  --out results.jsonl --keep-parameter-chains
```
""")
        per_model[model].append((number, name, target, finding["kind"], is_noise))

    for model, items in per_model.items():
        lines = [f"# {model}", "", f"{len(items)} findings.", "",
                 "| ID | Reached as | Kind | |", "|---|---|---|---|"]
        for number, name, target, kind, is_noise in items:
            lines.append(f"| [FINDING-{number:05d}](../{name}) | `{target}` | "
                         f"`{kind}` | {'noise' if is_noise else ''} |")
        (OUT / "by-model" / f"{slug(model, 80)}.md").write_text("\n".join(lines) + "\n")

    index = [
        "# Findings — one file per occurrence",
        "",
        f"**{len(flat)} findings** over **{len(per_model)} models**, from the "
        f"full-corpus static run.",
        "",
        "Every one is a **candidate**: the analysis reached it, nothing was "
        "observed failing. Execution-confirmed defects are the 26 in",
        "[`verified bugs/INSTANCES.md`](../../verified%20bugs/INSTANCES.md).",
        "",
        "| Granularity | Answers | Count |",
        "|---|---|---|",
        f"| [declaration-sites](../../declaration-sites/README.md) | a declaration permits an impossible value | 911 |",
        f"| [site-reports](../../site-reports/README.md) | one declaration, one claim — **what you edit** | {len(sites)} |",
        f"| findings/instances (here) | one occurrence — **what you reproduce** | {len(flat)} |",
        "",
        "## By kind", "", "| Kind | Findings |", "|---|---|",
    ]
    for kind, count in kinds.most_common():
        index.append(f"| `{kind}` | {count} |")
    index += [
        "",
        f"## Known false positives: {noisy} findings "
        f"({100 * noisy // max(len(flat), 1)}%)",
        "",
        "Findings of kind `physical-runtime-invariant-unobserved`: the invariant "
        "is a runtime property of a variable no user can set, so it is true and",
        "is not a declaration defect. They are written rather than suppressed "
        "because a precision figure needs its false positives counted.",
        "Filter with `grep -L 'Known false positive'`.",
        "",
        "## By model", "", "| Model | Findings |", "|---|---|",
    ]
    for model, items in sorted(per_model.items(), key=lambda kv: -len(kv[1])):
        index.append(f"| [{model}](by-model/{slug(model, 80)}.md) | {len(items)} |")
    index += ["", "## Regenerating", "",
              "```bash",
              "python3 tools/sweep/gen_finding_reports.py docs/runs/data/STATIC_FINAL.jsonl",
              "```", ""]
    (OUT / "README.md").write_text("\n".join(index) + "\n")

    print(f"wrote {len(flat)} findings over {len(per_model)} models")
    for kind, count in kinds.most_common():
        print(f"  {count:6}  {kind}")
    print(f"  {noisy:6}  flagged as noise")
    return 0


if __name__ == "__main__":
    sys.exit(main())
