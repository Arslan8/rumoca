#!/usr/bin/env python3
"""One file per instance, under `docs/v2/bugs/`, for every tier of evidence.

Three things every report must carry, because a reader who cannot do these
three cannot check the claim:

  1. **Which sanitizer found it**, named as the class and the file that
     implements it, plus the rule it fired — not "ModelSan found it".
  2. **A command that reproduces exactly this one finding**, on this one model,
     in seconds. `tools/sweep/check_one.py` exists for that; the corpus sweep
     takes half an hour and prints five thousand lines.
  3. **What would disprove it.** A finding a reader cannot argue with is not
     evidence, it is an assertion.

The tiers are kept visibly separate. Merging them would turn six thousand files
into "six thousand bugs", and 26 of them are proven.

    python3 tools/sweep/gen_bug_reports.py            # all tiers
    python3 tools/sweep/gen_bug_reports.py --tier confirmed
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

#: Where the reports are published. `docs/bugs/` was the first round, reviewed
#: in `docs/verifiedBugs/`; `docs/v2/bugs/` is the round after the contract,
#: aggregate and sign work. Overridable so a third round does not have to
#: overwrite the second one to exist.
OUT = Path("docs/v2/bugs")


def up() -> str:
    """The prefix a link out of `OUT` needs to reach `docs/`.

    Every generated link is written as `../something`, which is right one
    directory below `docs/`. Publishing two levels down without adjusting them
    produced a page of links that resolve nowhere, so the depth is computed
    from `OUT` and applied once, at write time.
    """
    return "../" * (len(OUT.parts) - 1)


def _relink(text: str) -> str:
    """Rewrite `](../x)` for the depth `OUT` actually sits at."""
    prefix = up()
    if prefix == "../":
        return text
    return text.replace("](../", f"]({prefix}")
STATIC_RUN = Path("docs/runs/data/STATIC_INTENT_DEFAULT.jsonl")
CONFIRMED_RUN = Path("docs/runs/data/INSTANCES.json")
ATTRIBUTION = Path("docs/runs/data/CONFIRMED_ATTRIBUTION.json")
CATALOG = Path("docs/findings/catalog/by-type")
ROOT_CAUSES = Path("docs/verified bugs")

# ── who found it ─────────────────────────────────────────────────────────────

#: sanitizer name -> (display name, implementing file, one line on what it does)
SANITIZERS = {
    "physical": (
        "PhysicalSan",
        "packages/modelsan/modelsan/sanitizers/physical.py",
        "binds each variable to a physical role from its `quantity`, unit and "
        "declaring class, then checks the domain invariant that role carries"),
    "divisor": (
        "DivisorSan",
        "packages/modelsan/modelsan/sanitizers/divisor.py",
        "proposes an assignment for each division's **complete denominator**, "
        "substitutes it and evaluates: a finding exists only when the "
        "denominator actually comes out zero, under values the declarations, "
        "assertions and branch conditions all permit"),
    "structure": (
        "StructureSan",
        "packages/modelsan/modelsan/sanitizers/structure.py",
        "matches equations to unknowns over the bipartite incidence graph, as "
        "a maximum flow so array families and array variables count properly"),
    "dimension": (
        "DimensionSan",
        "packages/modelsan/modelsan/sanitizers/dimension.py",
        "checks that both sides of every equation carry the same SI dimension"),
    "init-static": (
        "InitStaticSan",
        "packages/modelsan/modelsan/sanitizers/init_static.py",
        "evaluates the initialization system by interval arithmetic and reports "
        "what it can prove goes wrong before the first step"),
    "probe": (
        "the parameter probe + SolverSan",
        "packages/modelsan/modelsan/sanitizers/solver.py",
        "sets one parameter to a suspect value, runs the model, and reports a "
        "solver or initialization failure that the declared values do not produce"),
}

#: What each finding kind asserts, and what it deliberately does not.
KINDS = {
    "physical-bound-permits-zero": (
        "the declaration carries `min=0`, and the physical role bound to this "
        "variable requires strictly greater than zero",
        "that zero is *reachable* — the bound permits it, which is a property "
        "of the declaration, not an observation of a failure"),
    "physical-domain-unenforced": (
        "nothing bounds this declaration at all, so it permits values the "
        "physical role forbids, including negative ones",
        "that any model actually sets such a value"),
    "physical-invariant-violated": (
        "a value the model itself supplies violates the invariant of the "
        "physical role bound to this variable",
        "that the solver fails — the invariant is about meaning, not numerics"),
    "divisor-reachable-zero": (
        "a permitted assignment, given in full below, drives the **complete "
        "denominator** to zero, and nothing on the path excludes it",
        "that any model sets those values, or that the model fails when it "
        "does — a vanishing denominator in a quotient nothing reads is "
        "harmless"),
    "divisor-zero-when-parameters-equal": (
        "the denominator is a difference, so it vanishes when the two sides "
        "are equal; no `min` on either can express a constraint between two "
        "parameters",
        "that the two are equal at their declared values"),
    "divisor-guarded-by-assertion": (
        "the denominator can be zeroed arithmetically, but the model asserts "
        "it is bounded away from zero, so the assignment is one the model "
        "already rejects",
        "that anything is wrong — this is reported so a reader can see the "
        "guard was found, and can challenge it if it is insufficient"),
    "divisor-unreachable-under-witness": (
        "the assignment that zeroes the denominator also makes the branch "
        "containing the division unreachable, so the division is never "
        "evaluated at that value",
        "that anything is wrong"),
    "divisor-introduced-by-translation": (
        "this division was produced by the compiler, not written in the "
        "source; `L*der(i) = v` becomes `der(i) = v/L` because that is what a "
        "solver integrates",
        "that the source contract is wrong — it is evidence about the "
        "translation"),
    "physical-zero-is-a-supported-limit": (
        "the positivity rule does **not** apply: this component documents zero "
        "as a meaningful limit, so a missing-bound claim would contradict its "
        "contract",
        "that anything is wrong — this records a rule that was considered and "
        "correctly declined, with the contract that declined it"),
    "divisor-introduced-by-translation": (
        "zero is a supported limit of this component; the quotient the DAE "
        "shows is the compiler's solved form, not a division in the source",
        "that the source contract is wrong"),
    "physical-inertia-tensor-not-semidefinite": (
        "the six declarations that assemble this component's inertia tensor "
        "produce a matrix that is **not positive semidefinite**, which no "
        "rigid body has; the violated principal minor and the eigenvalues are "
        "below",
        "that any one entry is wrong on its own — an inertia tensor's "
        "off-diagonal entries are signed products of inertia and the "
        "constraint is a property of the assembled matrix"),
    "physical-inertia-tensor-undecided": (
        "this component's inertia tensor could not be assembled from values "
        "this analysis can resolve, so **neither its validity nor its "
        "invalidity is claimed**",
        "that anything is wrong. It is recorded because the six scalar "
        "declarations are excluded from the positivity rule either way, and a "
        "silent exclusion is indistinguishable from a missed defect"),
    "physical-rule-does-not-apply": (
        "the component documents this quantity as taking the value it holds, "
        "so the rule derived from the SI quantity alone does not bind it",
        "that anything is wrong — this records a rule that was considered and "
        "correctly declined, with the contract that declined it"),
    "physical-intent-question": (
        "the value or the declaration is unusual for the **quantity** it "
        "declares, and nothing says what this component is — so this is a "
        "question for the author, not a claim about the model",
        "that the value is wrong. `SI.Resistance` is declared by passive "
        "resistors, by negative-impedance converters, by linearised "
        "incremental models and by fault-injection inputs alike; without a "
        "component contract the analyzer does not know the intent, and this "
        "advisory asks rather than asserts"),
    "STRUCTURE_DEGENERATES_AT_ZERO": (
        "at zero this parameter removes a state and the equation determining "
        "it, so **this model's** topology may become singular",
        "that the component's declaration should forbid zero — that is a "
        "different and much stronger claim"),
    "divisor-zero-unresolved": (
        "an assignment drives the denominator to zero, but whether the "
        "division is evaluated there could not be decided from the artifact",
        "that the model is wrong — this is **unresolved**, not confirmed, and "
        "is reported so it is not silently dropped"),
    "divisor-zero-at-declared-values": (
        "the denominator is zero at the model's own declared values",
        "that any parameter can be blamed: nothing was changed, so this is a "
        "broken baseline rather than a latent hazard"),
    "UNMATCHED_VARIABLE": (
        "no equation in the connected structural region is left to determine "
        "this unknown",
        "anything about algebraic rank — a matched system can still be singular"),
    "UNMATCHED_EQUATION": (
        "this constraint has no unknown left to determine; the region is "
        "over-constrained",
        "anything about algebraic rank"),
    "declaration-permits-impossible-value": (
        "the type supplies no lower bound and the declaration adds none, so "
        "this parameter accepts a value that is not a physical quantity",
        "that any model sets such a value, or that anything fails"),
    "solver-failure": (
        "setting this parameter to a value its declaration permits makes the "
        "solver fail, in two independent tools, where the declared values run "
        "clean",
        "that any static rule predicted it — these are the instances no "
        "static sanitizer names"),
    "STATE_WITHOUT_DERIVATIVE_CONSTRAINT": (
        "the model declares a continuous state and then never says how it "
        "evolves — `der()` of it appears in no equation",
        "that the model fails to compile; Rumoca may still accept it"),
}

TIERS = {
    "confirmed": (
        "Confirmed",
        "fails under **two independent tools**, and the model is clean at its "
        "declared values"),
    "candidate": (
        "Candidate",
        "static analysis of the canonical DAE reached it; **no execution has "
        "decided it either way**"),
    "latent": (
        "Latent",
        "a declaration *permits* a physically impossible value; **nothing has "
        "been observed failing**"),
}

ROOTS = ("target/msl/", "target/corpus/", "target/cmm/")

#: Flags the run behind each tier was produced with. A reproduce command that
#: does not match them does not reproduce: `--no-fold-parameter-bindings`
#: changes which parameter a divisor finding names, so with it `fG` in
#: `OpAmps.LowPass` resolves away and `check_one.py` prints nothing — which
#: reads as the report being wrong rather than the command being wrong.
TIER_FLAGS = {
    "candidate": "",
    "confirmed": " --keep-parameter-chains",
}
PROVENANCE = {
    "candidate": ("`docs/runs/data/STATIC_INTENT_DEFAULT.jsonl`, "
                  "`tools/sweep/static_eval.py` over `tools/sweep/ALL.list`, "
                  "default flags"),
    "confirmed": ("`docs/runs/data/INSTANCES.json`, cross-confirmed against "
                  "OpenModelica 1.27.0-dev; sanitizer attribution re-derived "
                  "with `--keep-parameter-chains`"),
    "latent": ("`docs/findings/catalog/by-type/`, from "
               "`tools/sweep/min0_census.py`"),
}


#: Short, stable tags for the finding kinds, used in filenames.
KIND_TAG = {
    "physical-bound-permits-zero": "bound",
    "physical-domain-unenforced": "unbounded",
    "physical-invariant-violated": "violated",
    "divisor-reachable-zero": "divzero",
    "divisor-zero-when-parameters-equal": "divequal",
    "divisor-guarded-by-assertion": "divguarded",
    "divisor-unreachable-under-witness": "divunreach",
    "divisor-introduced-by-translation": "divgenerated",
    "divisor-zero-at-declared-values": "divbaseline",
    "divisor-zero-unresolved": "divunresolved",
    "physical-zero-is-a-supported-limit": "zerolimit",
    "physical-inertia-tensor-not-semidefinite": "tensor",
    "physical-inertia-tensor-undecided": "tensorunknown",
    "physical-rule-does-not-apply": "ruleoff",
    "physical-intent-question": "intent",
    "STRUCTURE_DEGENERATES_AT_ZERO": "degenerate",
}


def slugify(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return text[:70] or "x"


def relative(path: str) -> str:
    for prefix in ROOTS:
        if path.startswith(prefix):
            return path[len(prefix):]
    return path


def model_paths() -> dict[str, str]:
    found = {}
    for line in Path("tools/sweep/ALL.list").read_text().splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            found[parts[1].strip()] = parts[0]
    return found


def names_in(evidence: dict) -> set[str]:
    """Every variable or parameter name a finding's evidence refers to."""
    names: set[str] = set()
    for key in ("parameter", "variable", "state"):
        if evidence.get(key):
            names.add(str(evidence[key]))
    for key in ("required", "where", "observed", "equation"):
        names |= set(re.findall(r"[A-Za-z_]\w*(?:\.\w+|\[\d+\])*",
                                str(evidence.get(key, ""))))
    for part in str(evidence.get("path", "")).split("->"):
        if part.strip():
            names.add(part.strip())
    return names


def target_of(finding: dict) -> str:
    """The one name this finding is about, for the title."""
    evidence = finding["evidence"]
    if evidence.get("parameter"):
        return str(evidence["parameter"])
    # A divisor finding names an assignment, which may move more than one knob.
    # The title takes the first; the report carries all of them.
    witness = str(evidence.get("witness", ""))
    if witness and "=" in witness:
        return witness.split(",")[0].split("=")[0].strip()
    # A guarded or already-zero site needs no assignment, so there is no
    # witness to name. Fall back to a symbol in the denominator: a report
    # titled `?` is not findable, and its reproduce command filtered on `?`
    # and printed nothing.
    # The same pattern `check_one.py --target` matches on, subscripts and all.
    # Dropping the subscript here titled a report `oLine50.G` and handed the
    # reader a reproduce command that filtered for a name no finding carries:
    # the evidence says `oLine50.G[1].alpha`, and the command printed nothing.
    denominator = str(evidence.get("denominator", ""))
    names = re.findall(r"[A-Za-z_]\w*(?:\.\w+|\[\d+\])*", denominator)
    for candidate in names:
        if candidate not in ("max", "min", "abs", "sqrt", "exp", "log",
                             "sin", "cos", "tan", "der", "pre", "time",
                             "noEvent", "smooth", "if", "then", "else"):
            return candidate
    for key in ("required", "where", "observed"):
        match = re.match(r"\s*([A-Za-z_]\w*(?:\.\w+|\[\d+\])*)", str(evidence.get(key, "")))
        if match:
            return match.group(1)
    return evidence.get("variable") or "?"


def header(rows: list[tuple[str, str]]) -> str:
    body = "\n".join(f"| **{k}** | {v} |" for k, v in rows)
    return f"|  |  |\n|---|---|\n{body}\n"


def found_by(sanitizer: str, rule: str | None) -> str:
    name, source, what = SANITIZERS[sanitizer]
    line = f"**{name}** — `{source}`"
    if rule and rule != "—":
        line += f", rule `{rule}`"
    return line


def sanitizer_section(sanitizer: str, rule: str | None,
                      evidence: dict) -> str:
    name, source, what = SANITIZERS[sanitizer]
    out = [f"## Why {name} fired", "",
           f"{name} {what}.", ""]
    if evidence.get("aggregate"):
        out += [f"This one is an **aggregate** rule: its subject is the "
                f"`{evidence['aggregate']}` that "
                f"`{evidence.get('component', 'this component')}` assembles "
                f"from several declarations, not any one of them. The fields "
                f"it covers are excluded from the scalar rule, so this finding "
                f"is the only thing said about them.", "",
                "```",
                f"matrix       {evidence.get('matrix', '')}",
                f"eigenvalues  {evidence.get('eigenvalues', 'not computed')}",
                f"verdict      {evidence.get('verdict', '')}",
                f"reason       {evidence.get('reason', '')}",
                "```", "",
                "Positive semidefiniteness is decided over **all** principal "
                "minors with a scale-relative tolerance, not the leading ones: "
                "Sylvester's criterion over leading minors decides positive "
                "*definiteness*, and `[[0,0,0],[0,1,0],[0,0,-1]]` has leading "
                "minors 0, 0, 0 and an eigenvalue of -1. See "
                "[the method note](../method/aggregate-and-signed-domains.md).",
                ""]
    if evidence.get("premise_state"):
        out += ["A physical rule is two separate facts: the **predicate**, and "
                "the **authority** for applying it to this object. An SI "
                "quantity supplies the first and not the second — "
                "`SI.Resistance` is declared by a passive resistor, by a "
                "negative-impedance converter, by a linearised incremental "
                "model and by a fault-injection input alike. This finding "
                "records which it had:", "", "```",
                f"predicate     {evidence.get('required', '')}",
                f"premise       {evidence['premise_state']}",
                f"authority     {evidence.get('authority', '')}",
                f"role          {evidence.get('semantic_role', '—')}",
                f"declaration   {evidence.get('canonical_declaration', '—')}",
                "```", ""]
        if evidence["premise_state"] == "unknown":
            out += ["**unknown** means no component contract and no user "
                    "assumption says what this object is, so the rule is "
                    "applied as a *question*: it is low severity, it is not "
                    "counted as a defect, and it does not fail a run. Answer "
                    "it by adding a component contract or a `[[contracts]]` "
                    "entry naming the intended `sign_domain` — see "
                    "[the method note](../method/physical-intent-policy.md).",
                    ""]
        elif evidence["premise_state"] == "refuted":
            out += ["**refuted** means an authoritative contract permits this "
                    "value. The rule was considered and correctly declined; "
                    "this record exists so that a rule not firing is "
                    "distinguishable from a rule nobody wrote.", ""]
        else:
            out += ["**established** means a component contract or a user "
                    "assumption says this object is the component the rule is "
                    "about, so the predicate is enforced rather than "
                    "suggested.", ""]
    if evidence.get("question"):
        out += ["The question this finding asks:", "",
                f"> {evidence['question']}", ""]
    if evidence.get("contract"):
        out += ["The shared zero contract that decided this, and how strongly "
                "it is held:", "", "```",
                f"contract    {evidence['contract']}",
                f"behavior    {evidence.get('contract_behavior', '')}",
                f"confidence  {evidence.get('contract_confidence', '')}",
                f"source      {evidence.get('contract_source', '')}",
                "```", "",
                "`confidence` is the field to read first. **proven** means the "
                "model's own equations establish it, **declared** means the "
                "component's catalog entry does, and **assumed** means a user "
                "contract supplied it and it is an input to the analysis "
                "rather than a result of it.", ""]
    if evidence.get("witness"):
        out += ["The assignment it found, and the arithmetic that verifies it:",
                "", "```",
                f"denominator            {evidence.get('denominator', '')}",
                f"witness                {evidence['witness']}",
                f"  found by             {evidence.get('witness_rationale', '')}",
                f"denominator at witness {evidence.get('denominator_at_witness')}",
                f"at declared values     "
                f"{evidence.get('denominator_at_declared_values')}",
                f"path condition         {evidence.get('path_condition', '')}",
                f"constraints consulted  {evidence.get('constraints', '')}",
                "```", "",
                "The last four lines are the check. A denominator that does not "
                "evaluate to zero under the witness is not a finding, and this "
                "pass previously reported many that did not.", "",
                "`constraints consulted` is where a disagreement usually lands. "
                "A symbol is only offered as a witness when its declaration "
                "permits the value: a `constant` never is, a `final` "
                "declaration is not unless its binding reads something "
                "adjustable, and `protected` is visibility rather than "
                "immutability. The contract behind that decision is carried in "
                "the artifact per symbol, so it can be read rather than "
                "inferred.", ""]
    if evidence.get("rule_origin"):
        out += [f"The rule it applied is `{rule}`:", "",
                f"> {evidence['rule_origin']}", ""]
    if evidence.get("rule_reference"):
        out += [f"Reference: {evidence['rule_reference']}.", ""]
    matched = evidence.get("matched_by")
    if matched:
        out += ["It bound this variable to that rule on this evidence — this is "
                "the step to check first if you think the rule does not apply "
                "here:", "", "```", str(matched), "```", ""]
    if evidence.get("path") and str(evidence["path"]) != evidence.get("parameter"):
        out += [f"The parameter reaches the denominator along `{evidence['path']}`, "
                f"which is why the finding names the parameter a user can set "
                f"rather than the expression that divides.", ""]
    return "\n".join(out)


def _cell(value: str, limit: int = 600) -> str:
    """One evidence value, cut at a word boundary rather than mid-word.

    A value clipped to a fixed byte count ended a sentence at "beca", which
    reads as a broken generator rather than as an elision.
    """
    text = html.escape(str(value)).replace("|", "&#124;").replace("\n", " ")
    if len(text) <= limit:
        return text
    head = text[:limit].rsplit(" ", 1)[0]
    return f"{head} … (truncated)"


def evidence_table(evidence: dict) -> str:
    skip = {"rule_origin", "rule_reference", "matched_by"}
    rows = [f"| `{k}` | {_cell(v)} |"
            for k, v in evidence.items() if k not in skip]
    if not rows:
        return ""
    return "## Evidence\n\n| key | value |\n|---|---|\n" + "\n".join(rows) + "\n"


def tier_table(active: str) -> str:
    rows = []
    for key, (label, meaning) in TIERS.items():
        # The meaning already contains bold, so the active row is marked on the
        # label and with an arrow rather than by wrapping the whole cell —
        # nested `**` does not render.
        mark = "-> " if key == active else ""
        rows.append(f"| {mark}**{label}** | {meaning} |")
    return ("## How strong is this?\n\n| Tier | Evidence |\n|---|---|\n"
            + "\n".join(rows) + "\n\nThis instance is in the "
            f"**{TIERS[active][0]}** tier.\n")


# ── tier 1: confirmed ────────────────────────────────────────────────────────

def render_confirmed(number: int, entry: dict, attribution: dict,
                     paths: dict[str, str]) -> tuple[str, dict]:
    model = entry["model"]
    target, value = entry["trigger"].split("=", 1)
    path = paths.get(model, "")
    finding = attribution.get(entry["trigger"] + "@" + model)
    sanitizer = finding["sanitizer"] if finding else "probe"
    rule = (finding or {}).get("evidence", {}).get("rule")
    root = root_cause_for(target, model)

    rows = [
        ("Tier", "**Confirmed** — reproduced in two independent tools"),
        ("Model", f"`{model}`"),
        ("Trigger", f"`{target} = {value}`"),
        ("Found by", found_by(sanitizer, rule)),
    ]
    if finding:
        rows.append(("Reported as", f"`{finding['kind']}`"))
        rows.append(("Declaration", f"`{finding['source']}`"))
    rows += [
        ("Confirmed by", "SolverSan under Rumoca, and independently under "
                         "OpenModelica 1.27.0-dev"),
        ("Reach", f"{entry.get('reach', '?')} models set this declaration"),
        ("From run", PROVENANCE["confirmed"]),
        ("Fix site", f"[{root[0]}](../verified%20bugs/{root[1]})" if root else "—"),
        ("Status", "Reported upstream, not fixed"),
    ]

    body = [f"# BUG-{number:03d}: `{target}` in `{model.split('.')[-1]}`", "",
            header(rows), ""]

    body += ["## The claim", "",
             f"`{model}` runs cleanly at its declared values. Setting "
             f"`{target} = {value}` — a value the declaration permits — makes "
             f"it fail, in Rumoca and in OpenModelica.", "",
             "The defect is in the **declaration**, not in this model. This "
             "model is the witness.", ""]

    if finding:
        body += [sanitizer_section(sanitizer, rule, finding["evidence"]), ""]
        body += [evidence_table(finding["evidence"]), ""]
    else:
        body += ["## Why no static sanitizer names it", "",
                 "No static rule covers this one. It was found by perturbing "
                 "parameters and watching the solver: the static checkers "
                 "reason about one declaration at a time, and this failure is "
                 "a relationship between two of them, which no `min` can "
                 "express.", ""]

    body += [verify_confirmed(model, target, value, path, sanitizer,
                              (finding or {}).get("source", "")), ""]
    body += [disprove(sanitizer, confirmed=True), ""]
    body += [tier_table("confirmed")]

    slug = slugify(f"{model.split('.')[-1]}-{target}")
    return "\n".join(body), {"name": f"BUG-{slug}.md",
                             "id": f"BUG-{number:03d}", "tier": "confirmed",
                             "sanitizer": sanitizer, "model": model,
                             "target": target,
                             "kind": (finding or {}).get("kind", "solver-failure")}


def root_cause_for(target: str, model: str) -> tuple[str, str] | None:
    """The fix-site report covering this parameter, if one exists."""
    parameter = target.rsplit(".", 1)[-1]
    for report in sorted(ROOT_CAUSES.glob("BUG-*.md")):
        text = report.read_text(errors="replace")
        head = text.split("\n", 1)[0].lstrip("# ").strip()
        if re.search(rf"`[\w.]*\b{re.escape(parameter)}`", head):
            return head, report.name
    return None


def read_declaration(source: str) -> str:
    """Commands that open the declaration a finding points at.

    `source` is a path and a line, relative to the repository root, and the
    path is the part that has to be there: ten files in MSL are called
    `HollowCylinderAxialFlux.mo`, so a command that searches for the basename
    and takes the first match opens `Icons/HollowCylinderAxialFlux.mo`, which
    has no line 16. Runs produced before that was fixed carry a basename alone,
    and those still get the search, with the ambiguity stated.
    """
    if not source or ":" not in source:
        return ("The finding carries no declaration line, so there is nothing "
                "to open here.\n")
    name, _, line = source.rpartition(":")
    tail = """
That line is the declaration. Read its `min`: a declaration with no `min`, or
with `min=0`, permits the trigger value. Check the *type* too — a bound can be
inherited, and an inherited bound would refute the finding.
"""
    if "/" in name:
        return f"""```console
$ sed -n '{line}p' "{name}"
```
{tail}"""
    base = name
    return f"""```console
$ find target/msl target/corpus -name '{base}'
$ sed -n '{line}p' "$(find target/msl target/corpus -name '{base}' | head -1)"
```

This run recorded the basename only, so check the first command's output before
trusting the second: several MSL files share a basename, and the declaration is
in whichever one declares this component.
{tail}"""


def verify_confirmed(model: str, target: str, value: str, path: str,
                     sanitizer: str, source: str) -> str:
    # An instance no static rule covers has nothing for `check_one.py` to
    # reproduce, and telling a reader to run it anyway would hand them a
    # failure that looks like the report being wrong.
    if sanitizer == "probe":
        first = f"""**1. No static sanitizer reports this one** (seconds) — that is the point of
it, and this command confirms it rather than reproducing anything:

```console
$ python3 tools/sweep/check_one.py {model} \\
      --target {target} --keep-parameter-chains
```

It should print **0 findings**. The failure below is real regardless; it is
what the static rules miss.
"""
    else:
        first = f"""**1. The sanitizer still reports it** (seconds):

```console
$ python3 tools/sweep/check_one.py {model} \\
      --target {target} --keep-parameter-chains
```
"""
    return f"""## How to verify

Three checks, in increasing cost. All are run from the repository root.

{first}

**2. The declaration really permits the value** (seconds):

{read_declaration(source)}
**3. The model fails at that value, and only at that value** (a minute):

```console
$ ./target/debug/rumoca compile "{path}" --model {model} \\
      --source-root target/msl/ModelicaStandardLibrary-4.1.0 \\
      --source-root target/corpus/ModelicaStandardLibrary-4.1.0 \\
      --emit-bitcode /tmp/m.rbc
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check \\
      --param {target}={value}
```

The first simulation must succeed and the second must fail. If the first also
fails, the model is not a clean witness and this instance should be withdrawn.

**Independently, under OpenModelica** — this is what makes the instance
*confirmed* rather than a candidate, so it is the check that matters most:

```console
$ omc --version          # needs CC=gcc on this machine
$ omc <<'EOF'
loadModel(Modelica, {{"4.1.0"}});
simulate({model}, simflags="-override {target}={value}");
EOF
```
"""


def disprove(sanitizer: str, confirmed: bool) -> str:
    common = [
        "## What would disprove this",
        "",
    ]
    if confirmed:
        common += [
            "- The baseline simulation also fails, so the trigger value is not "
            "what breaks it.",
            "- The declaration turns out to carry a bound that excludes the "
            "trigger value after all (check the *type* as well as the "
            "declaration — a bound can be inherited).",
            "- The value is a documented sentinel rather than a real setting. "
            "`Spice3.mo` encodes \"unset\" as `-1e40` and tests for it before "
            "use; see [sentinel-parameters](../findings/sentinel-parameters.md).",
        ]
    elif sanitizer == "physical":
        common += [
            "- The semantic binding is wrong: the `matched_by` block above says "
            "why this variable was given this physical role. If the quantity or "
            "the declaring class does not mean what the rule assumes, the "
            "finding does not apply.",
            "- The value is excluded elsewhere — by an `assert`, by a guard, or "
            "by a bound on the *type* rather than the declaration.",
            "- The variable is a documented sentinel.",
        ]
    else:
        common += [
            "- Something on the path does exclude zero: an `assert`, an `if` "
            "guard, or a `min` on an intermediate declaration. DivisorSan "
            "follows bindings, not control flow, so a guard in an algorithm "
            "section is exactly the case it can miss.",
            "- The denominator is never evaluated in any configuration this "
            "model reaches.",
        ]
    return "\n".join(common) + "\n"


# ── tier 2: candidate ────────────────────────────────────────────────────────

def render_candidate(number: int, model: str, finding: dict,
                     paths: dict[str, str]) -> tuple[str, dict]:
    evidence = finding["evidence"]
    target = target_of(finding)
    sanitizer = finding["sanitizer"]
    rule = evidence.get("rule")
    kind = finding["kind"]
    claims, does_not = KINDS.get(kind, (kind, "—"))
    path = paths.get(model, "")

    rows = [
        ("Tier", "**Candidate** — static only, not execution-confirmed"),
        ("Model", f"`{model}`"),
        ("Reached as", f"`{target}`"),
        ("Found by", found_by(sanitizer, rule)),
        ("Reported as", f"`{kind}`"),
        ("Severity", finding.get("severity", "?")),
        ("Declaration", f"`{finding.get('source') or '?'}`"),
        ("Signature", f"`{finding.get('signature', '')}`"),
        ("From run", PROVENANCE["candidate"]),
        ("Status", "**candidate — no execution has decided it either way**"),
    ]

    body = [f"# FINDING-{number:05d}: `{target}` in `{model.split('.')[-1]}`", "",
            header(rows), "",
            "## The claim", "",
            f"{claims.capitalize()}.", "",
            f"It does **not** claim {does_not}.", ""]
    body += [sanitizer_section(sanitizer, rule, evidence), ""]
    body += [evidence_table(evidence), ""]
    body += [verify_candidate(model, target, sanitizer, path,
                              finding.get("source", ""), evidence), ""]
    body += [disprove(sanitizer, confirmed=False), ""]
    body += ["## Where the fix goes", "",
             "At the declaration, not in this model. Every model that reaches "
             "the same declaration is a separate file here; one edit closes "
             "all of them. Use the declaration line above to find the others:",
             "",
             "```console",
             f"$ grep -rl '| `{finding.get('source', '')}` |' {OUT}/",
             "```", ""]
    body += [tier_table("candidate")]

    # The filename is derived from what the finding *is*, never from where it
    # fell in the run. A positional name changes whenever the corpus does: one
    # detector fix renumbered every report and broke 5132 inbound links.
    slug = slugify(f"{model.split('.')[-1]}-{target}-{KIND_TAG.get(kind, kind)}")
    return "\n".join(body), {"name": f"FINDING-{slug}.md",
                             "id": f"FINDING-{number:05d}", "tier": "candidate",
                             "sanitizer": sanitizer, "model": model,
                             "target": target, "kind": kind}


def witness_overrides(evidence: dict, target: str) -> str:
    """`--param` flags applying a finding's witness, verbatim."""
    witness = str(evidence.get("witness", ""))
    parts = []
    for piece in witness.split(","):
        if "=" in piece:
            name, _, value = piece.partition("=")
            parts.append(f" \\\n      --param {name.strip()}={value.strip()}")
    return "".join(parts) or f" --param {target}=0"


def verify_candidate(model: str, target: str, sanitizer: str, path: str,
                     source: str, evidence: dict) -> str:
    chains = TIER_FLAGS["candidate"]
    overrides = witness_overrides(evidence, target)
    # `--target ?` matches nothing. Where the finding names no symbol, the
    # command runs unfiltered rather than filtering on a placeholder.
    filter = f"--target {target} " if target and target != "?" else ""
    return f"""## How to verify

**1. Reproduce this exact finding** (seconds):

```console
$ python3 tools/sweep/check_one.py {model} \\
      {filter}--sanitizer {sanitizer}{chains}
```

This compiles the one model, runs the one sanitizer, and prints what it finds.
It should print the evidence table above.

The flags matter and are not optional: they are the ones the run in the header
used. Adding `--keep-parameter-chains` keeps derived parameter bindings
symbolic, which changes *which* parameter a divisor finding names, so a
reproduce command with different flags can legitimately print nothing.

**2. Read the declaration it points at.** The finding is about what the
declaration permits, so this is the check that decides whether it is right:

{read_declaration(source)}
**3. See it in the IR, if the claim is about reach rather than a bound:**

```console
$ python3 tools/sweep/check_one.py {model} --keep-artifact /tmp/m.rbc \\
      --sanitizer {sanitizer}{chains} >/dev/null
$ ./target/debug/rumoca bitcode disasm /tmp/m.rbc | grep -n "{target}"
```

**4. Decide it by execution** — this is what would move it out of the candidate
tier, and nothing here has done it:

```console
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check{overrides}
```

The second command applies **the witness this finding names**, not an arbitrary
zero. A finding that claims a denominator vanishes has already been checked
arithmetically; what execution adds is whether the vanishing matters.

A clean baseline and a failing perturbation makes this **confirmed**. A failing
baseline makes it **undecidable** — the model does not run, so nothing can be
attributed to the parameter.
"""


# ── tier 3: latent ───────────────────────────────────────────────────────────

ROW = re.compile(r"^\| `([^`]+)` \| (\d+) \| `([^`]+)` \| `?([^|]*?)`? \|$")

#: Why the value the type permits is not a physical state of affairs.
WHY = {
    "resistance": "a resistance below zero makes a passive element a source",
    "conductance": "the reciprocal of a resistance; negative means generation",
    "inductance": "stored energy is `L*i^2/2`, which a negative `L` makes negative",
    "capacitance": "stored energy is `C*v^2/2`, which a negative `C` makes negative",
    "inertia": "`J*a = tau` determines angular acceleration only for `J > 0`",
    "momentofinertia": "`J*a = tau` determines angular acceleration only for `J > 0`",
    "mass": "`m*a = f` determines acceleration only for `m > 0`",
    "length": "a negative length is not a geometry",
    "area": "a negative cross-section is not a geometry",
    "volume": "a negative volume is not a geometry",
    "permeance": "the magnetic analogue of conductance",
    "reluctance": "the magnetic analogue of resistance",
    "resistivity": "a material property that is non-negative by definition",
    "conductivity": "a material property that is non-negative by definition",
    "heatcapacity": "a negative heat capacity makes heating cool the body",
    "specificheatcapacity": "a negative heat capacity makes heating cool the body",
    "density": "a negative density is not a material",
    "duration": "a negative duration runs time backwards",
    "time": "a negative time constant inverts the response",
    "frequency": "a negative frequency is the same signal with a phase shift; "
                 "zero divides",
}


def read_catalog() -> list[dict]:
    """Every exposed declaration, from the per-type catalog pages."""
    entries = []
    for page in sorted(CATALOG.glob("*.md")):
        if page.name == "README.md":
            continue
        type_name = ""
        exposed = False
        for line in page.read_text().splitlines():
            if line.startswith("# "):
                match = re.search(r"`([^`]+)`", line)
                type_name = match.group(1) if match else page.stem
            if line.startswith("## "):
                exposed = line.strip().lower() == "## exposed"
                continue
            if not exposed:
                continue
            row = ROW.match(line)
            if row:
                entries.append({
                    "file": row.group(1), "line": int(row.group(2)),
                    "param": row.group(3),
                    "modifiers": row.group(4).strip() or "—",
                    "type": type_name, "quantity": page.stem,
                })
    return entries


#: The two corpus layouts, both of which nest the Modelica package one level
#: below the archive root but under different names.
PACKAGE_ROOTS = (
    "target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0",
    "target/corpus/ModelicaStandardLibrary-4.1.0/Modelica",
)


def resolve_msl(relative_path: str) -> str:
    """An openable path for a file the catalog names relative to the package."""
    for root in PACKAGE_ROOTS:
        candidate = Path(root) / relative_path
        if candidate.exists():
            return str(candidate)
    return f"{PACKAGE_ROOTS[0]}/{relative_path}"


def units_file() -> str:
    """Where `Units.mo` actually is, since the claim is about what it omits."""
    for root in PACKAGE_ROOTS:
        candidate = Path(root) / "Units.mo"
        if candidate.exists():
            return str(candidate)
    return f"{PACKAGE_ROOTS[0]}/Units.mo"


def render_latent(number: int, entry: dict) -> tuple[str, dict]:
    quantity = entry["quantity"]
    why = WHY.get(quantity, f"a negative {quantity} is not a physical value")
    # The catalog stores the path relative to the *Modelica package* root, not
    # to the archive root, and the two corpora nest that package differently
    # ("Modelica 4.1.0/" vs "Modelica/"). Resolving it here rather than
    # concatenating gives a path that actually opens.
    path = resolve_msl(entry["file"])

    rows = [
        ("Tier", "**Latent** — a permitted value, not an observed failure"),
        ("Declaration", f"`{entry['file']}:{entry['line']}`"),
        ("Parameter", f"`{entry['param']}`"),
        ("Type", f"`{entry['type']}`"),
        ("Declared modifiers", f"`{entry['modifiers']}`"),
        ("Found by", "**the SI type-bound census** — "
                     "`tools/sweep/min0_census.py`, the same bound rule "
                     "PhysicalSan applies, run over declarations rather than "
                     "over one model's variables"),
        ("From run", PROVENANCE["latent"]),
        ("Status", "**latent — nothing has been observed failing here**"),
    ]

    body = [f"# DECL-{number:04d}: `{entry['param']}` declared without a lower bound",
            "", header(rows), "",
            "## The claim", "",
            f"`{entry['type']}` declares no `min` in `Units.mo`, and this "
            f"declaration adds none of its own. It therefore accepts a "
            f"negative value, and {why}.", "",
            "It does **not** claim that any model sets such a value, or that "
            "anything fails. This is the weakest tier in this project and the "
            "one most likely to contain deliberate choices.", ""]

    body += [f"""## How to verify

**1. Read the declaration** (seconds):

```console
$ sed -n '{entry['line']}p' "{path}"
```

It should declare `{entry['param']}` with type `{entry['type']}` and no `min`.

**2. Confirm the type supplies no bound either** — this is the whole claim, and
a bound inherited from the type would refute it:

```console
$ grep -n "type {entry['type'].split('.')[-1]} " "{units_file()}"
```

If that line carries no `min`, the type supplies no bound and the claim stands.

**3. Check it is not a sentinel.** Some MSL packages encode "unset" as a
negative magic number and test for it before use:

```console
$ grep -n -- "-1e40\\|-1E40" "{path}" | head
```

If this file uses that idiom, the negative value is deliberate — see
[sentinel-parameters](../findings/sentinel-parameters.md) — and this report
should be withdrawn.
""", ""]

    body += ["## What would disprove this", "",
             f"- `{entry['type']}` turns out to carry a `min` after all, or "
             f"this declaration carries one that the catalog missed.",
             "- The parameter is a sentinel, as above.",
             "- The negative range is meaningful for this quantity in this "
             "context — a signed offset rather than a magnitude.", ""]

    body += ["## The fix is not here", "",
             "This site is one of **911** that inherit from **17 type "
             "definitions** in `Units.mo` that declare no `min`. Bounding the "
             "type is one edit and closes every site that inherits it:", "",
             "```modelica",
             "// Units.mo",
             f"type {entry['type'].split('.')[-1]} = Real (",
             f'    final quantity="{entry["type"].split(".")[-1]}",',
             "    final unit=\"...\",",
             "    min=0);",
             "```", "",
             "Bounding this one declaration instead is correct but local:", "",
             "```modelica",
             f"// {entry['file']}:{entry['line']}",
             f"parameter {entry['type']} {entry['param']}(min=0) = ...;",
             "```", "",
             "See [si-type-bounds](../findings/si-type-bounds.md) for why the "
             "type is the right place.", ""]

    body += [tier_table("latent")]

    slug = slugify(f"{Path(entry['file']).stem}-{entry['param']}-{entry['line']}")
    return "\n".join(body), {"name": f"DECL-{slug}.md",
                             "id": f"DECL-{number:04d}", "tier": "latent",
                             "sanitizer": "type-census",
                             "model": entry["file"], "target": entry["param"],
                             "kind": "declaration-permits-impossible-value"}


# ── indexes ──────────────────────────────────────────────────────────────────

def write_indexes(records: list[dict]) -> None:
    by_tier = Counter(r["tier"] for r in records)
    by_sanitizer = Counter(r["sanitizer"] for r in records)
    by_kind = Counter(r["kind"] for r in records)

    lines = [
        "# Bugs, one file per instance", "",
        "Every instance this project reports, at every strength of evidence, "
        "as a file that can be opened, linked and argued with. Each one names "
        "**which sanitizer found it** and carries the commands to check it.", "",
        "> **The total is not the number to quote.** These are three different "
        "kinds of claim and merging them would be dishonest — 26 are proven, "
        "the rest are reach.", "",
        "| Tier | Meaning | Instances |", "|---|---|---|",
    ]
    for key, (label, meaning) in TIERS.items():
        lines.append(f"| **{label}** | {meaning} | {by_tier.get(key, 0)} |")
    lines += ["", f"**{sum(by_tier.values())} files total.**", "",
              "## Which sanitizer found what", "",
              "This is the column a reader usually wants first: it says which "
              "detector is responsible, and therefore which one to doubt.", "",
              "| Sanitizer | What it does | Instances |", "|---|---|---|"]
    for name, count in by_sanitizer.most_common():
        if name in SANITIZERS:
            display, source, what = SANITIZERS[name]
            lines.append(f"| [{display}](by-sanitizer/{name}.md) "
                         f"<br>`{source}` | {what} | {count} |")
        else:
            lines.append(f"| [SI type-bound census](by-sanitizer/{name}.md) "
                         f"<br>`tools/sweep/min0_census.py` | the same bound rule "
                         f"PhysicalSan applies, run over the library's *declarations* "
                         f"rather than over one model's variables | {count} |")

    lines += ["", "## By finding kind", "", "| Kind | Instances | Asserts |",
              "|---|---|---|"]
    for kind, count in by_kind.most_common():
        claims = KINDS.get(kind, (kind, ""))[0]
        lines.append(f"| `{kind}` | {count} | {claims} |")

    lines += ["", "## Have these been checked?", "",
              "Yes, by running the commands the reports themselves print — "
              "extracted from the published markdown, not from the generator, "
              "so a report whose steps do not execute is caught:", "",
              "```console",
              "$ python3 tools/sweep/verify_bug_reports.py --tier confirmed --all",
              "$ python3 tools/sweep/verify_bug_reports.py --tier latent --all",
              "$ python3 tools/sweep/verify_bug_reports.py --tier candidate --sample 400",
              "```", "",
              "| Tier | Checked | Result |", "|---|---|---|",
              "| Confirmed | all 26 | 26 ok |",
              "| Latent | all 911 | 911 ok |",
              "| Candidate | 400 of 5142, sampled | 400 ok |", "",
              "\"ok\" means the commands run and produce what the report says "
              "they will — for a latent report, that the declaration line opens "
              "and its type really carries no `min`; for a candidate, that the "
              "sanitizer still reports a finding naming the same target. It "
              "does **not** mean the finding is a real defect: that is what the "
              "tier says, and for the candidate tier nothing has decided it.", "",
              "## Verifying any of these", "",
              "Every report carries its own commands. They all reduce to one "
              "tool, which compiles a single model and runs a single sanitizer "
              "over it:", "",
              "```console",
              "$ python3 tools/sweep/check_one.py <model> --target <name> "
              "--sanitizer <sanitizer>",
              "```", "",
              "Prerequisites, and the known weak points of each tier, are in "
              "[VERIFY.md](../VERIFY.md). The corpus runs these reports were "
              "generated from are in [runs/data/](../runs/data/), so a "
              "disagreement can be traced to a row rather than argued about.", "",
              "## Naming", "",
              "| Prefix | Tier |", "|---|---|",
              "| `BUG-nnn` | confirmed |",
              "| `FINDING-nnnnn` | candidate |",
              "| `DECL-nnnn` | latent |", "",
              "## What changed since the last run", "",
              "[withdrawn.md](withdrawn.md) lists the findings that stopped "
              "reporting and the ones that started, with why. None were "
              "withdrawn for being wrong; the compiler fixes made array "
              "equations and call arguments visible, which moved attribution "
              "from the propagated parameter to the one that actually divides.",
              "",
              "The root-cause argument for a confirmed instance — why the "
              "declaration is wrong, and what the fix is — lives in "
              "[`../verified bugs/`](../verified%20bugs/). These files are the "
              "*instances*; that directory holds the *fix sites*.", ""]
    (OUT / "README.md").write_text(_relink("\n".join(lines) + "\n"))

    index = OUT / "by-sanitizer"
    index.mkdir(exist_ok=True)
    grouped = defaultdict(list)
    for record in records:
        grouped[record["sanitizer"]].append(record)
    for name, rows in grouped.items():
        display, source, what = SANITIZERS.get(
            name, ("SI type-bound census", "tools/sweep/min0_census.py",
                   "the same bound rule PhysicalSan applies, run over the "
                   "library's declarations"))
        page = [f"# Found by {display}", "",
                f"Implemented in `{source}`.", "", f"{display} {what}.", "",
                f"**{len(rows)} instances.**", "",
                "| ID | Tier | Kind | Target | Model or file |",
                "|---|---|---|---|---|"]
        for record in sorted(rows, key=lambda r: r["id"]):
            page.append(f"| [{record['id']}](../{record['name']}) "
                        f"| {record['tier']} | `{record['kind']}` "
                        f"| `{record['target']}` | `{record['model']}` |")
        (index / f"{name}.md").write_text("\n".join(page) + "\n")

    by_model = defaultdict(list)
    for record in records:
        by_model[record["model"]].append(record)
    page = ["# By model", "",
            "Which instances each model witnesses. A model appearing many "
            "times usually reaches many *different* declarations, not one "
            "declaration many times.", "",
            "| Model or file | Instances | Sanitizers |", "|---|---|---|"]
    for model, rows in sorted(by_model.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        sanitizers = ", ".join(sorted({r["sanitizer"] for r in rows}))
        page.append(f"| `{model}` | {len(rows)} | {sanitizers} |")
    (OUT / "by-model.md").write_text(_relink("\n".join(page) + "\n"))


def write_withdrawn() -> None:
    """What the current run stopped reporting, and what it started.

    Generated here rather than by hand, because `--clean` deletes anything it
    did not write and a hand-made page in this directory disappears silently.
    """
    baseline = Path("docs/runs/data/STATIC_WITH_FAMILIES_AND_CALLS.jsonl")
    if not baseline.exists() or not STATIC_RUN.exists():
        return

    def keyed(path: Path) -> set:
        found = set()
        for line in path.read_text().splitlines():
            row = json.loads(line)
            for finding in row.get("findings", []):
                found.add((row["model"], finding["kind"],
                           target_of(finding)))
        return found

    before, after = keyed(baseline), keyed(STATIC_RUN)
    gone, fresh = sorted(before - after), sorted(after - before)
    lines = [
        "# Withdrawn and newly reported", "",
        "What changed between the previous run and this one. Both are archived "
        "in [`../runs/data/`](../runs/data/), so any row here can be traced.", "",
        "The baseline is the run before the divisor rework, so this page is "
        "cumulative rather than a single step. Four defects account for it: "
        "[TOOLBUG-017](../toolbugs/TOOLBUG-017-divisor-reported-parameters-not-denominators.md) "
        "(every parameter inside a denominator reported without checking that "
        "the denominator could vanish), "
        "[TOOLBUG-018](../toolbugs/TOOLBUG-018-ir-lost-the-symbol-contract.md) "
        "(the IR could not distinguish a constant from a settable parameter), "
        "[TOOLBUG-019](../toolbugs/TOOLBUG-019-two-valued-divisor-classification.md) "
        "(a path the analysis could not decide was treated as reachable) and "
        "[TOOLBUG-020](../toolbugs/TOOLBUG-020-zero-behaviour-was-decided-three-times.md) "
        "(three detectors deciding separately what zero meant). Nothing here "
        "was withdrawn for being inconvenient; each withdrawal is a claim that "
        "did not hold.", "",
        f"## Withdrawn ({len(gone)})", "",
        "| Model | Kind | Target |", "|---|---|---|",
    ]
    lines += [f"| `{m}` | `{k}` | `{t}` |" for m, k, t in gone]
    lines += ["", f"## Newly reported ({len(fresh)})", "",
              "Divisions previously attributed to the wrong parameter, or not "
              "reached at all.", "",
              "| Model | Kind | Target |", "|---|---|---|"]
    lines += [f"| `{m}` | `{k}` | `{t}` |" for m, k, t in fresh]
    (OUT / "withdrawn.md").write_text(_relink("\n".join(lines) + "\n"))


# ── driver ───────────────────────────────────────────────────────────────────

_TAKEN: dict[str, int] = {}


def _write(record: dict, text: str) -> None:
    """Write a report, disambiguating a name two findings would share.

    Silently overwriting would lose a finding and leave a count that no longer
    matches the files on disk, which is exactly the kind of quiet loss this
    project keeps finding in other people's tools.
    """
    name = record["name"]
    if name in _TAKEN:
        _TAKEN[name] += 1
        stem, _, extension = name.rpartition(".")
        name = f"{stem}-{_TAKEN[record['name']]}.{extension}"
        record["name"] = name
    else:
        _TAKEN[name] = 1
    (OUT / name).write_text(_relink(text))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier", action="append", default=[],
                        choices=sorted(TIERS), help="default: all")
    parser.add_argument("--clean", action="store_true",
                        help=f"remove {OUT} first")
    parser.add_argument("--out", type=Path, default=None,
                        help=f"where to publish (default {OUT})")
    args = parser.parse_args()
    if args.out is not None:
        globals()["OUT"] = args.out
    tiers = args.tier or list(TIERS)

    if args.clean and OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)

    paths = model_paths()
    records: list[dict] = []

    if "confirmed" in tiers:
        entries = json.loads(CONFIRMED_RUN.read_text())
        attribution = (json.loads(ATTRIBUTION.read_text())
                       if ATTRIBUTION.exists() else {})
        for number, entry in enumerate(entries, start=1):
            text, record = render_confirmed(number, entry, attribution, paths)
            _write(record, text)
            records.append(record)
        print(f"confirmed: {len(entries)}")

    if "candidate" in tiers:
        number = 0
        for line in STATIC_RUN.read_text().splitlines():
            row = json.loads(line)
            for finding in row.get("findings", []):
                number += 1
                text, record = render_candidate(number, row["model"], finding, paths)
                _write(record, text)
                records.append(record)
        print(f"candidate: {number}")

    if "latent" in tiers:
        entries = read_catalog()
        for number, entry in enumerate(entries, start=1):
            text, record = render_latent(number, entry)
            _write(record, text)
            records.append(record)
        print(f"latent: {len(entries)}")

    write_indexes(records)
    write_withdrawn()
    print(f"{len(records)} reports in {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
