#!/usr/bin/env python3
"""Label every finding true positive, false positive, or unjudged.

A precision figure needs both numerators, and a sanitizer paper that reports
only its true positives is reporting half a result. So the false positives are
first-class here: each has a named class, a reason, and the evidence that
settled it.

Three verdicts, and the third is the honest majority:

    true-positive   reproduced in two independent tools
    false-positive  a named class with evidence that the claim does not hold
    unjudged        nobody has decided; counted, never silently dropped

Precision is reported over the *judged* subset with the judged fraction stated
next to it, because `TP / (TP + FP)` computed while ignoring 90% unjudged is a
number that means nothing.
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

#: False-positive classes, each established during this project with evidence.
#: The predicate decides membership from the finding alone, so the label is
#: reproducible rather than a remembered judgement.
FALSE_POSITIVE_CLASSES = [
    (
        "runtime-invariant-on-a-state",
        "The invariant is a runtime property of a variable no user can set — "
        "`HeatPort.T` is a connector variable. True, and not a declaration "
        "defect.",
        lambda f: f["kind"] == "physical-runtime-invariant-unobserved",
    ),
    (
        "documented-sign-latitude",
        "MSL documents the component as permitting this sign: "
        "\"The Resistance R is allowed to be positive, zero, or negative.\" "
        "Asserting R > 0 contradicts the component. See "
        "docs/findings/documented-sign-latitude.md.",
        lambda f: f["evidence"].get("rule") in
                  ("elec.resistance.positive", "elec.conductance.positive")
                  and _declared_in(f, ("Resistor.mo", "Conductor.mo")),
    ),
    (
        "sentinel-encoded-parameter",
        "Spice3 encodes an unset parameter as -1e40 and tests against it "
        "before use (Spice3.mo:157). The negative value is deliberate. See "
        "docs/findings/sentinel-parameters.md.",
        lambda f: "Spice3" in str(f.get("source", "")),
    ),
    (
        "bound-the-author-chose",
        "The declaration states `final min=0`, which is the author allowing "
        "zero rather than overlooking it — `IdealCommutingSwitch.Goff` is an "
        "off-state conductance whose ideal value is zero.",
        lambda f: f["kind"] == "physical-bound-permits-zero"
                  and _declared_in(f, ("Ideal", "Switch", "Diode", "Thyristor")),
    ),
]


def _declared_in(finding: dict, markers: tuple[str, ...]) -> bool:
    source = str(finding.get("source", ""))
    return any(marker in source for marker in markers)


def confirmed_keys(path: Path) -> set[tuple[str, str]]:
    """(model, parameter) pairs proven in two tools."""
    if not path.exists():
        return set()
    found = set()
    for entry in json.loads(path.read_text()):
        target = entry["trigger"].split("=")[0]
        found.add((entry["model"], target))
    return found


def adjudicate(finding: dict, model: str, confirmed: set) -> tuple[str, str, str]:
    evidence = finding["evidence"]
    predicate = evidence.get("required", "") or ""
    target = predicate.split()[0] if predicate else evidence.get("parameter", "?")
    if (model, target) in confirmed:
        return ("true-positive", "execution-confirmed",
                "reproduced in Rumoca and OpenModelica; the model is clean at "
                "its declared values and fails at this one")
    for name, reason, predicate_fn in FALSE_POSITIVE_CLASSES:
        try:
            if predicate_fn(finding):
                return ("false-positive", name, reason)
        except Exception:
            continue
    return ("unjudged", "no-oracle-run",
            "static analysis reached it; no execution has decided it either way")


def main() -> int:
    rows = [json.loads(l) for l in Path(sys.argv[1]).read_text().splitlines() if l.strip()]
    confirmed = confirmed_keys(Path("docs/runs/data/INSTANCES.json"))

    verdicts = collections.Counter()
    classes = collections.Counter()
    labelled = []
    for row in rows:
        for finding in row["findings"]:
            verdict, cls, reason = adjudicate(finding, row["model"], confirmed)
            verdicts[verdict] += 1
            classes[(verdict, cls)] += 1
            labelled.append({"model": row["model"], "verdict": verdict,
                             "class": cls, "reason": reason, "kind": finding["kind"],
                             "source": finding.get("source", "?")})

    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("docs/runs/data/ADJUDICATED.json")
    out.write_text(json.dumps(labelled, indent=0))

    total = sum(verdicts.values())
    tp, fp = verdicts["true-positive"], verdicts["false-positive"]
    judged = tp + fp
    print(f"{total} findings")
    for verdict, count in verdicts.most_common():
        print(f"  {count:6}  {verdict}  ({100 * count / total:.1f}%)")
    if judged:
        print(f"\nprecision over the judged subset: {tp}/{judged} = "
              f"{100 * tp / judged:.1f}%   (judged: {100 * judged / total:.1f}% of all)")
    print("\nby class:")
    for (verdict, cls), count in classes.most_common():
        print(f"  {count:6}  {verdict:15} {cls}")
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
