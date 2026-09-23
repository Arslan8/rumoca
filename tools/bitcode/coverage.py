#!/usr/bin/env python3
"""Which schema constructs the corpus actually exercises.

`roundtrip_audit.py` proves that whatever a model *does* produce survives a
round trip. It cannot say anything about a construct no model in the sample
happens to produce — and that is the failure this project keeps meeting: a
field written by the exporter and never read by the parser fails only when
somebody compiles the right model.

So this counts coverage. Every variant of the expression node set, every
optional table on `RbcModel`, and every optional field the exporter can emit
is tallied across a sample; anything at zero is reported, because an untested
construct and a broken one look identical until then.

    tools/bitcode/coverage.py --limit 120
    tools/bitcode/coverage.py --limit 120 --fail-on-gap
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "packages" / "rumoca-bitcode")]

RUMOCA = ROOT / "target" / "debug" / "rumoca"
SCHEMA = ROOT / "crates/rumoca-bitcode/src/schema.rs"
ROOTS = ["target/msl/ModelicaStandardLibrary-4.1.0",
         "target/corpus/ModelicaStandardLibrary-4.1.0",
         "target/cmm/CMM-a642c381"]

#: Tables on `RbcModel` that an artifact may legitimately omit. Each is a
#: construct whose export path is exercised only by a model that has one.
OPTIONAL_TABLES = (
    "domains", "functions", "equation_families", "initial_equation_families",
    "discrete_real_equations", "initial_discrete_values",
    "discrete_definitions", "connections", "connection_sets", "components",
    "trace_points", "relations", "conditions", "roots", "events",
    "time_events", "initial_equations",
)


#: Constructs no *compiled* model can produce, with what does cover them. The
#: exporter never writes a trace point --- `RbcTracePoint` exists for a later
#: pass to add --- so a corpus sample cannot reach that path and a permanent
#: entry in the gap list would train a reader to ignore the list.
NOT_EXPORTED = {
    "table:trace_points":
        "added by an instrumentation pass, never by export; covered by "
        "packages/modelsan/tests/test_network.py::"
        "test_instrumenting_an_artifact_is_idempotent_and_valid",
    "field:trace_point.connection_set":
        "same pass; covered by the same test",
}


def expression_kinds() -> list[str]:
    """Every `RbcExprNode` variant, as serde spells it on the wire."""
    source = SCHEMA.read_text()
    body = re.search(r"pub enum RbcExprNode \{(.*?)\n\}", source, re.S).group(1)
    found = []
    for line in body.splitlines():
        hit = re.match(r"\s{4}(\w+)\s*[{(,]", line)
        if hit:
            found.append(_snake(hit.group(1)))
    return found


def _snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def one(entry: tuple[str, str]) -> dict:
    import rumoca_bitcode as rb

    path, name = entry
    work = tempfile.mkdtemp()
    artifact = Path(work) / "m.rbc"
    command = [str(RUMOCA), "compile", path, "--model", name,
               "--emit-bitcode", str(artifact)]
    for root in ROOTS:
        command += ["--source-root", root]
    try:
        subprocess.run(command, capture_output=True, cwd=ROOT, timeout=180)
    except subprocess.TimeoutExpired:
        return {}
    if not artifact.exists():
        return {}

    model = rb.decode(artifact.read_bytes())["model"]
    seen: collections.Counter = collections.Counter()
    for expression in model.get("expressions", []):
        kind = expression.get("node", {}).get("kind")
        if kind:
            seen[f"expr:{kind}"] += 1
    for table in OPTIONAL_TABLES:
        if model.get(table):
            seen[f"table:{table}"] += 1
    # Optional fields whose absence is the common case, so their export path is
    # the one least likely to be exercised.
    for variable in model.get("variables", []):
        if variable.get("contract"):
            seen["field:variable.contract"] += 1
        if variable.get("connector"):
            seen["field:variable.connector"] += 1
        if variable.get("declaring_class"):
            seen["field:variable.declaring_class"] += 1
    for component in model.get("components", []):
        if component.get("class_name"):
            seen["field:component.class_name"] += 1
    for entry_set in model.get("connection_sets", []):
        if entry_set.get("balances"):
            seen["field:connection_set.balances"] += 1
        if entry_set.get("unconnected"):
            seen["field:connection_set.unconnected"] += 1
    for point in model.get("trace_points", []):
        if point.get("connection_set") is not None:
            seen["field:trace_point.connection_set"] += 1
    return dict(seen)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", default="tools/sweep/ALL.list")
    parser.add_argument("--limit", type=int, default=120)
    parser.add_argument("--jobs", type=int, default=8)
    parser.add_argument("--out", default="")
    parser.add_argument("--fail-on-gap", action="store_true")
    args = parser.parse_args()

    entries = []
    for line in (ROOT / args.list).read_text().splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            entries.append((parts[0], parts[1].strip()))
    # Spread the sample across the library rather than taking a prefix: the
    # first N entries of an alphabetical list are all one package, and a
    # coverage number from one package is not a coverage number.
    if args.limit and args.limit < len(entries):
        step = len(entries) / args.limit
        entries = [entries[int(index * step)] for index in range(args.limit)]

    total: collections.Counter = collections.Counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for seen in pool.map(one, entries):
            total.update(seen)

    expected = ([f"expr:{kind}" for kind in expression_kinds()]
                + [f"table:{name}" for name in OPTIONAL_TABLES]
                + ["field:variable.contract", "field:variable.connector",
                   "field:variable.declaring_class",
                   "field:component.class_name",
                   "field:connection_set.balances",
                   "field:connection_set.unconnected",
                   "field:trace_point.connection_set"])
    gaps = [name for name in expected
            if not total.get(name) and name not in NOT_EXPORTED]
    elsewhere = [name for name in expected
                 if not total.get(name) and name in NOT_EXPORTED]

    covered = len(expected) - len(gaps) - len(elsewhere)
    print(f"{len(entries)} models sampled, {covered}/{len(expected)} "
          f"constructs covered by the corpus, {len(elsewhere)} elsewhere\n")
    for name in expected:
        count = total.get(name, 0)
        if count:
            mark = "    "
        elif name in NOT_EXPORTED:
            mark = "[T] "
        else:
            mark = "GAP "
        print(f"  {mark}{name:<42} {count}")
    if elsewhere:
        print("\n[T] not producible by compiling a model; covered by a test:")
        for name in elsewhere:
            print(f"  {name}\n      {NOT_EXPORTED[name]}")
    if gaps:
        print(f"\n{len(gaps)} construct(s) no sampled model produces. An "
              f"untested export path and a broken one look identical:")
        for name in gaps:
            print(f"  {name}")
    if args.out:
        Path(args.out).write_text(json.dumps(
            {"sampled": len(entries), "counts": dict(total), "gaps": gaps},
            indent=1) + "\n")
    return 1 if (gaps and args.fail_on_gap) else 0


if __name__ == "__main__":
    raise SystemExit(main())
