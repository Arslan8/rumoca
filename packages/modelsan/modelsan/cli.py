"""`modelsan model.mo` — find a parameter configuration that breaks the model."""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from rumoca_bitcode import Model

from .analysis import declared_ranges, find_domain_sites, incomplete, search_knobs
from .mutate import candidates, minimize
from .runner import export, find_rumoca, resolve_span, run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="modelsan", description=__doc__)
    parser.add_argument("model", help="a .mo file, or a .rbc artifact")
    parser.add_argument("--model-name", help="which model to compile")
    parser.add_argument("--source-root", action="append", default=[])
    parser.add_argument("--rumoca", help="path to the rumoca binary")
    parser.add_argument("--t-end", type=float, default=1.0)
    parser.add_argument("--max-trials", type=int, default=200)
    parser.add_argument("--all", action="store_true", help="keep searching after the first failure")
    parser.add_argument("--static-only", action="store_true", help="skip the parameter search")
    args = parser.parse_args(argv)

    rumoca = find_rumoca(args.rumoca)
    path = Path(args.model)

    with tempfile.TemporaryDirectory() as work:
        if path.suffix == ".rbc":
            artifact = path
        else:
            artifact = export(
                rumoca, path, args.model_name, Path(work) / "model.rbc", args.source_root
            )

        model = Model.load(artifact)
        print(f"[+] Parsed model {model.name}")
        print(
            f"    {len(model.equations)} equations, {len(model.variables)} variables, "
            f"{len(model.parameters)} parameters"
        )

        gaps = incomplete(model)
        if gaps:
            print(
                f"[!] {gaps} expression(s) could not be represented in bitcode v1;"
                " results below are based on a partial model"
            )

        sites = find_domain_sites(model)
        print(f"\n[+] {len(sites)} operation(s) with a mathematical domain condition")
        for site in sites:
            print(site)

        ranges = declared_ranges(model)
        if ranges:
            print(f"[+] {len(ranges)} variable(s) declare a min/max range to respect")

        if args.static_only or (not sites and not ranges):
            return 0

        knobs = search_knobs(model, sites)
        if not knobs:
            print("\n[+] no parameters gate those operations; nothing to search")
            return 0

        # Baseline first. A model that already fails with its declared values
        # has nothing to attribute to a parameter, and reporting the first
        # candidate as the "trigger" would be a false accusation.
        baseline = run(rumoca, artifact, {}, t_end=args.t_end)
        if not baseline.ok and baseline.kind != "tool-error":
            print("\n[!] Model already fails with its declared parameter values")
            print(f"\nType:\n    {baseline.kind}")
            print(f"\nDetail:\n    {baseline.detail}")
            location = resolve_span(model, baseline.detail)
            if location:
                print(f"\nSource:\n    {location}")
            print(
                "\nNo parameter search was run: there is nothing to attribute,"
                "\nbecause the failure does not depend on any override."
            )
            return 1

        print(f"\n[+] Baseline simulation is clean")
        print(f"[+] Exploring parameter space over {len(knobs)} parameter(s)...")
        trials = candidates(knobs)[: args.max_trials]

        failures = 0
        for index, candidate in enumerate(trials, start=1):
            outcome = run(rumoca, artifact, candidate.assignment, t_end=args.t_end)
            if outcome.ok:
                continue
            if outcome.kind == "tool-error":
                print(f"    trial {index}: tool error: {outcome.detail}")
                continue

            failures += 1
            print(f"\n[!] ModelSan found a failure  (trial {index} of {len(trials)})")
            print(f"\nType:\n    {outcome.kind}")
            print(f"\nDetail:\n    {outcome.detail}")
            location = resolve_span(model, outcome.detail)
            if location:
                print(f"\nSource:\n    {location}")
            print(f"\nTrigger:\n    {candidate}")

            minimal = minimize(
                candidate.assignment,
                lambda trial: not run(rumoca, artifact, trial, t_end=args.t_end).ok,
            )
            print("\nMinimal configuration:")
            for name, value in minimal.items():
                print(f"    {name} = {value:g}")

            related = [s for s in sites if any(p.name in minimal for p in s.parameters)]
            if related:
                print("\nImplicated operation(s):")
                for site in related:
                    print(f"    {site.expression}   requires {site.condition}")
                    print(f"        {site.source}")

            if not args.all:
                return 1

        if failures:
            return 1
        print(f"\n[+] No failure found in {len(trials)} configuration(s)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
