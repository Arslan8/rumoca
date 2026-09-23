#!/usr/bin/env python3
"""What the connection graph looks like across the corpus.

Run separately from `static_eval.py` rather than folded into it: the published
reports are mid-review, and adding a sanitizer to the main sweep would move
every count in them for a reason unrelated to what is being reviewed.

    tools/sweep/network_census.py --list tools/sweep/ALL.list --out census.json
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "packages" / "rumoca-bitcode"),
                str(ROOT / "packages" / "modelsan")]

RUMOCA = ROOT / "target" / "debug" / "rumoca"
ROOTS = ["target/msl/ModelicaStandardLibrary-4.1.0",
         "target/corpus/ModelicaStandardLibrary-4.1.0",
         "target/cmm/CMM-a642c381"]


def one(entry: tuple[str, str]) -> dict:
    path, name = entry
    import rumoca_bitcode
    from modelsan.analysis.context import AnalysisContext
    from modelsan.network import build, component_power
    from modelsan.sanitizers import NetworkSan

    work = tempfile.mkdtemp()
    artifact = Path(work) / "m.rbc"
    command = [str(RUMOCA), "compile", path, "--model", name,
               "--emit-bitcode", str(artifact)]
    for root in ROOTS:
        command += ["--source-root", root]
    try:
        subprocess.run(command, capture_output=True, cwd=ROOT, timeout=180)
    except subprocess.TimeoutExpired:
        return {"model": name, "status": "timeout"}
    if not artifact.exists():
        return {"model": name, "status": "no-dae"}

    model = rumoca_bitcode.Model.load(artifact)
    network = build(model)
    if network.absent:
        return {"model": name, "status": "no-connections"}

    kinds = collections.Counter(node.kind.value for node in network.nodes)
    power = collections.Counter()
    for component in network.components:
        balance = component_power(network, component)
        if not balance.terms:
            continue
        power["complete" if balance.complete else "partial"] += 1
        for term in balance.terms:
            power[f"form:{term.form.value}"] += 1
    findings = NetworkSan().analyze(model, AnalysisContext(model))
    return {
        "model": name, "status": "analyzed",
        "nodes": len(network.nodes), "components": len(network.components),
        "ports": len(network.ports),
        "max_degree": max((node.degree for node in network.nodes), default=0),
        "by_kind": dict(kinds), "power": dict(power),
        "findings": collections.Counter(f.kind for f in findings),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--jobs", type=int, default=8)
    args = parser.parse_args()

    entries = []
    for line in Path(args.list).read_text().splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            entries.append((parts[0], parts[1].strip()))

    rows = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for index, row in enumerate(pool.map(one, entries), start=1):
            rows.append(row)
            if index % 100 == 0:
                print(f"  {index}/{len(entries)}", flush=True)

    Path(args.out).write_text(json.dumps(rows, indent=1) + "\n")
    status = collections.Counter(row["status"] for row in rows)
    analyzed = [row for row in rows if row["status"] == "analyzed"]
    kinds = collections.Counter()
    power = collections.Counter()
    findings = collections.Counter()
    for row in analyzed:
        kinds.update(row["by_kind"])
        power.update(row["power"])
        findings.update(row["findings"])
    print(json.dumps({
        "status": dict(status),
        "models_with_a_graph": len(analyzed),
        "nodes": sum(row["nodes"] for row in analyzed),
        "ports": sum(row["ports"] for row in analyzed),
        "node_kinds": dict(kinds),
        "component_power": dict(power),
        "findings": dict(findings),
    }, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
