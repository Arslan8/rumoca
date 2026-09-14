#!/usr/bin/env python3
"""Confirm, by execution, which declared parameter domains a model cannot survive.

The static censuses propose candidates and run at roughly 23% precision, which
is not a reportable rate. This confirms them instead: for each parameter, set it
to a value its own declaration permits, and keep only the cases where the model
simulates cleanly at its declared values and fails at the permitted one.

Every row this prints is therefore a reproduced failure, not a suspicion.
"""
import json, subprocess, sys, tempfile
from pathlib import Path

sys.path[:0] = ["packages/rumoca-bitcode", "packages/modelsan"]
from rumoca_bitcode import Model
from modelsan.legacy.analysis import _literal_value
from modelsan.legacy.runner import export, run

RUMOCA = "./target/debug/rumoca"


def probes(model):
    """Values each parameter's own declaration permits, worth trying.

    Zero first: it is what `min=0` and an absent bound both admit, and it is the
    value that makes a coefficient vanish or a divisor blow up. The declared
    lower bound is tried too when it is not zero, because a bound the component
    cannot honour is the same defect wherever it sits.
    """
    out = []
    for variable in model.variables:
        if not variable.is_parameter:
            continue
        low = _literal_value(variable.minimum)
        high = _literal_value(variable.maximum)
        for value in (0.0, low):
            if value is None:
                continue
            if low is not None and value < low:
                continue
            if high is not None and value > high:
                continue
            if (variable.name, value) in {(v, x) for v, x in out}:
                continue
            out.append((variable.name, value))
    return out


def sweep(jobs, roots, t_end, timeout, per_model, out_path):
    stats = dict(total=0, compiled=0, no_params=0, fails_nominally=0,
                 searched=0, models_with_findings=0, findings=0, trials=0)
    rows = []
    with tempfile.TemporaryDirectory() as work:
        art = Path(work) / "m.rbc"
        for i, (path, name) in enumerate(jobs, 1):
            stats["total"] += 1
            if art.exists():
                art.unlink()
            try:
                export(RUMOCA, Path(path), name, art, roots)
            except Exception:
                continue
            stats["compiled"] += 1
            try:
                model = Model.load(art)
            except Exception:
                continue

            candidates = probes(model)[:per_model]
            if not candidates:
                stats["no_params"] += 1
                continue

            base = run(RUMOCA, art, {}, t_end=t_end, timeout=timeout)
            if not base.ok:
                stats["fails_nominally"] += 1
                continue
            stats["searched"] += 1

            hits = []
            for param, value in candidates:
                stats["trials"] += 1
                got = run(RUMOCA, art, {param: value}, t_end=t_end, timeout=timeout)
                if got.ok or got.kind == "tool-error":
                    continue
                hits.append({"parameter": param, "value": value,
                             "kind": got.kind, "detail": got.detail[:200]})
            if hits:
                stats["models_with_findings"] += 1
                stats["findings"] += len(hits)
                rows.append({"model": name, "hits": hits})
                print(f"### {name}: {len(hits)} confirmed", flush=True)
                for hit in hits[:3]:
                    print(f"      {hit['parameter']} = {hit['value']:g} -> {hit['detail'][:90]}",
                          flush=True)
            if i % 25 == 0:
                print(f"... {i}/{len(jobs)}  searched={stats['searched']}"
                      f"  findings={stats['findings']}", flush=True)

    Path(out_path).write_text(json.dumps({"stats": stats, "rows": rows}, indent=1))
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--list", required=True)
    p.add_argument("--root", action="append", default=[])
    p.add_argument("--t-end", type=float, default=0.5)
    p.add_argument("--timeout", type=float, default=25)
    p.add_argument("--per-model", type=int, default=40)
    p.add_argument("--limit", type=int, default=10**9)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    jobs = [l.split("\t") for l in Path(a.list).read_text().splitlines() if l.strip()]
    jobs = [(x[0], x[1]) for x in jobs][: a.limit]
    sweep(jobs, a.root, a.t_end, a.timeout, a.per_model, a.out)
