#!/usr/bin/env python3
"""Collect, for each sampled finding, what is needed to decide it.

Execution cannot settle a physical claim: a negative mass that simulates
cleanly is still a negative mass. What settles it is three facts, and all three
are in the source:

  1. the declaration — does it carry a bound of its own?
  2. the SI type in `Units.mo` — does *it* carry one?
  3. what the component documents — MSL states "The Resistance R is allowed to
     be positive, zero, or negative", and a rule asserting otherwise is
     arguing with the library.

Fact 3 is the one this project got wrong by assuming, so it is gathered rather
than recalled.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MSL = Path("target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0")


def find_file(stem: str) -> Path | None:
    hits = list(MSL.rglob(stem))
    return hits[0] if hits else None


def type_bound(quantity: str) -> str:
    """What `Units.mo` says about this SI type."""
    try:
        text = (MSL / "Units.mo").read_text(errors="replace")
    except OSError:
        return "?"
    found = re.search(rf"\btype\s+{re.escape(quantity)}\s*=\s*[\w.]+\s*\(([^;]*?)\)\s*(?:\"|;)",
                      text, re.S)
    if not found:
        return "no such type"
    modifiers = " ".join(found.group(1).split())
    low = re.search(r"min\s*=\s*([^,)]+)", modifiers)
    return f"min={low.group(1).strip()}" if low else "NO min"


def component_latitude(path: Path | None, member: str) -> str:
    """Whether the component documents this value as permitted to be negative."""
    if path is None:
        return "?"
    text = path.read_text(errors="replace")
    found = re.search(r"allowed to be[^<.]*", text)
    return found.group(0) if found else "no statement"


def declaration(path: Path | None, line: int) -> str:
    if path is None:
        return "?"
    lines = path.read_text(errors="replace").splitlines()
    if 0 < line <= len(lines):
        return lines[line - 1].strip()
    return "?"


def main() -> int:
    sample = json.loads(Path(sys.argv[1]).read_text())
    wanted = sys.argv[2] if len(sys.argv) > 2 else None
    for position, entry in enumerate(sample):
        if entry.get("verdict"):
            continue
        if wanted and entry["kind"] != wanted:
            continue
        source = entry["source"]
        stem, _, line = source.partition(":")
        path = find_file(stem)
        evidence = entry["evidence"]
        matched = evidence.get("matched_by")
        if isinstance(matched, str):
            try:
                matched = eval(matched)  # the run stringified it
            except Exception:
                matched = {}
        quantity = (matched or {}).get("quantity", "")
        print(f"[{position}] {entry['kind']}")
        print(f"    target     {entry['target']}   in {entry['model'].split('.')[-1]}")
        print(f"    claim      {evidence.get('required','')}")
        print(f"    decl       {source}   {declaration(path, int(line or 0))[:100]}")
        print(f"    SI type    {quantity or '-'}: {type_bound(quantity) if quantity else '-'}")
        print(f"    documents  {component_latitude(path, entry['target'])[:90]}")
        role = evidence.get("variable_role", "-")
        print(f"    role       {role}   declared_min={evidence.get('declared_min','-')}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
