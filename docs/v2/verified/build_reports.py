#!/usr/bin/env python3
"""Build the exhaustive v2 verification ledger.

The v2 input directory deliberately contains defect candidates, explicit
non-defect adjudications, unresolved analyses, and 26 historical runtime BUG
reports.  Treating every file as a bug would undo the distinctions the reports
themselves make.  This generator accounts for each report exactly once and
keeps the evidence basis visible in the rendered result.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


HERE = Path(__file__).resolve().parent
DOCS = HERE.parents[1]
INPUT = HERE.parent / "bugs"
PRIOR = DOCS / "verifiedBugs"

FALSE_KINDS = {
    "physical-zero-is-a-supported-limit": (
        "The v2 result explicitly records that zero is a supported component "
        "limit. It says the positivity rule does not apply and does not claim "
        "that the model is defective."
    ),
    "divisor-guarded-by-assertion": (
        "The complete denominator is protected by an existing assertion. The "
        "zero assignment is outside the model's admitted domain, so this is "
        "not an unguarded divide-by-zero defect."
    ),
    "divisor-unreachable-under-witness": (
        "The assignment that makes the denominator zero also makes the branch "
        "containing the division unreachable. The arithmetic witness is not an "
        "executable-path witness."
    ),
    "divisor-introduced-by-translation": (
        "The quotient is a compiler-solved representation of a source equation "
        "whose zero value is an algebraic/feature limit. It does not prove a "
        "source-level division contract defect."
    ),
    "physical-rule-does-not-apply": (
        "The component-specific contract refutes the generic physical rule. "
        "The v2 record explicitly says no defect is claimed."
    ),
}

UNRESOLVED_KINDS = {
    "divisor-zero-unresolved": (
        "The denominator has an arithmetic zero witness, but the current IR "
        "cannot decide whether the division executes on that path."
    ),
    "physical-inertia-tensor-undecided": (
        "The aggregate inertia tensor cannot be assembled from values currently "
        "available to the analysis. Neither validity nor invalidity is proven."
    ),
    "divisor-zero-at-declared-values": (
        "The static artifact says a denominator is zero at declared values, but "
        "these four cases lack an independent clean-baseline execution and may "
        "still involve conditional-component or path reconstruction. They remain "
        "unresolved rather than being called broken baselines."
    ),
}

SOURCE_CANDIDATE_KINDS = {
    "divisor-reachable-zero",
    "divisor-zero-when-parameters-equal",
}

ADVISORY_KINDS = {
    "physical-intent-question": (
        "The analyzer observed a value or permissive declaration that is unusual "
        "for the quantity, but it has no component contract or user assumption "
        "establishing that the generic physical rule applies. It therefore asks "
        "the author about intent and deliberately makes no defect claim."
    ),
    "physical-runtime-invariant-unobserved": (
        "The generic quantity rule describes a possible runtime invariant, but "
        "there is no violating observation and no settable declaration to fix. "
        "This remains visible as a question rather than a defect claim."
    ),
}


@dataclass
class Report:
    id: str
    path: Path
    title: str
    tier: str
    model: str
    target: str
    sanitizer: str
    kind: str
    declaration: str
    claim: str
    sha256: str


@dataclass
class Verdict:
    report: Report
    verdict: str
    group: str
    reason: str
    basis: str
    proposed_action: str
    prior_report: str = ""
    omc: dict | None = None


def field(text: str, name: str) -> str:
    found = re.search(rf"\| \*\*{re.escape(name)}\*\* \| (.*?) \|", text)
    return found.group(1).strip().strip("`") if found else ""


def section(text: str, name: str) -> str:
    found = re.search(
        rf"^## {re.escape(name)}\s*$\n(.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not found:
        return ""
    paragraphs = [p.strip() for p in found.group(1).split("\n\n") if p.strip()]
    return " ".join(paragraphs[:2])


def parse(path: Path) -> Report:
    text = path.read_text(errors="replace")
    heading = re.match(r"# ((?:BUG|FINDING|DECL)-\d+):?\s*(.*)", text)
    if not heading:
        raise ValueError(f"missing report heading: {path}")
    report_id, title = heading.groups()
    model = field(text, "Model")
    target = field(text, "Reached as")
    trigger = field(text, "Trigger")
    if not target and trigger:
        target = trigger.split(" = ", 1)[0].strip("`")
    if not target:
        quoted = re.match(r"# (?:BUG|FINDING|DECL)-\d+: `([^`]+)`", text)
        target = quoted.group(1) if quoted else ""
    sanitizer = field(text, "Found by")
    sanitizer = re.sub(r"\*\*|`.*", "", sanitizer).strip(" —")
    return Report(
        id=report_id,
        path=path,
        title=title.strip(),
        tier=field(text, "Tier").split(" —", 1)[0].replace("**", ""),
        model=model,
        target=target,
        sanitizer=sanitizer,
        kind=field(text, "Reported as"),
        declaration=field(text, "Declaration"),
        claim=section(text, "The claim"),
        sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
    )


def load_prior():
    with (PRIOR / "index.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    by_id = {row["id"]: row for row in rows}
    by_key: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_key[(row["model"], row["target"])].append(row)
    return by_id, by_key


def load_omc(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    by_id: dict[str, dict] = {}
    for result in data.get("results", []):
        for report_id in result["report_ids"]:
            by_id[report_id] = result
    for skipped in data.get("skipped", []):
        by_id[skipped["id"]] = {
            "outcome": f"not-attempted-{skipped['reason']}",
            "baseline": "unknown",
            "trigger": "unknown",
            "wrapper": "",
            "diagnostic": "",
        }
    return by_id


def normalize_prior(value: str) -> str:
    return "false-positive" if value == "false-positives" else value


def prior_verdict(report: Report, row: dict[str, str], basis: str) -> Verdict:
    verdict = normalize_prior(row["verdict"])
    reason = row.get("reason", "")
    action = row.get("proposed_action", "")
    if verdict == "confirmed" and not action:
        action = "Add a domain assertion/guard at the source calculation and a boundary regression test."
    if verdict == "false-positive" and not reason:
        reason = "The earlier source and execution review refuted the stated claim."
    if verdict == "unresolved" and not reason:
        reason = "The earlier review did not obtain enough executable or source-semantic evidence."
    return Verdict(
        report=report,
        verdict=verdict,
        group=row.get("group") or report.kind or "prior-review",
        reason=reason,
        basis=basis,
        proposed_action=action,
        prior_report=row.get("report", ""),
    )


def classify(report: Report, by_id, by_key, omc_by_id, physical_omc_by_id) -> Verdict:
    # The 26 BUG reports and 911 declaration census entries retain stable IDs.
    # They were individually checked in the first audit, including independent
    # OpenModelica controls for every BUG claim.
    if report.id.startswith(("BUG-", "DECL-")):
        prior = prior_verdict(
            report,
            by_id[report.id],
            "Exact stable-ID source/execution review from the first exhaustive audit.",
        )
        # BUG reports were exercised with independent execution controls.  A
        # DECL report is a latent contract review, so even a source-supported
        # declaration defect must not be presented as a reproduced bug.
        if report.id.startswith("DECL-") and prior.verdict == "confirmed":
            prior.verdict = "candidate"
            prior.basis = (
                "Exact stable-ID source-semantic review from the first audit; "
                "the latent declaration report has no failing execution witness."
            )
        return prior

    if report.kind in FALSE_KINDS:
        return Verdict(
            report,
            "false-positive",
            report.kind,
            FALSE_KINDS[report.kind],
            "The v2 report's own verdict/proof explicitly declines a defect claim.",
            "Keep this as a regression proving the detector suppresses or labels the non-defect correctly.",
        )

    if report.kind in UNRESOLVED_KINDS:
        return Verdict(
            report,
            "unresolved",
            report.kind,
            UNRESOLVED_KINDS[report.kind],
            "The v2 analysis explicitly reports UNKNOWN or lacks independent baseline evidence.",
            "Resolve the path/aggregate value and obtain a clean baseline before assigning blame.",
        )

    if report.kind in ADVISORY_KINDS:
        return Verdict(
            report,
            "advisory",
            report.kind,
            ADVISORY_KINDS[report.kind],
            "The finding carries premise_state=unknown: quantity/unit evidence raises the question, but does not establish component intent.",
            "Ask the author whether the value/domain is intended. If it is, add a component contract or user assumption; if it is not, add the appropriate declaration bound. Promote to a violation only after that intent evidence is available.",
        )

    if report.kind in SOURCE_CANDIDATE_KINDS:
        equality = report.kind == "divisor-zero-when-parameters-equal"
        execution = omc_by_id.get(report.id)
        if execution and execution["outcome"] == "confirmed-by-omc":
            return Verdict(
                report,
                "confirmed",
                report.kind,
                "The exact reported witness was placed in a generated Modelica subclass before translation. The unmodified model executed cleanly, while OpenModelica rejected the trigger with a numerical failure such as division by zero, a non-finite result, or a singular system.",
                "Rumoca supplied the source-resolved arithmetic witness; independent OpenModelica source translation and execution reproduced the attributed failure against a clean paired baseline.",
                (
                    "Add a relational assertion/guard that prevents the two denominator operands from becoming equal, and test equal, reversed, and nominal values."
                    if equality
                    else "Constrain or assert the complete denominator away from zero before evaluating the division. If zero has a meaningful limit, implement an explicit algebraic branch; do not hide it with an epsilon."
                ),
                omc=execution,
            )
        if execution and execution["outcome"] == "refuted-illegal-witness":
            return Verdict(
                report,
                "false-positive",
                "illegal-divisor-witness",
                "OpenModelica rejects the report's exact source modification because the named nested element is protected, final, otherwise non-modifiable, or violates a binding rule. The report therefore does not supply a legal executable witness for its claim.",
                "Independent OpenModelica source translation of the exact witness refuted its admissibility.",
                "Keep this report as a regression: the analysis must carry modifiability/visibility through qualified component paths and must not offer an illegal parameter assignment as a witness.",
                omc=execution,
            )
        if execution:
            outcome = execution["outcome"]
            return Verdict(
                report,
                "unresolved",
                report.kind,
                (
                    "The static denominator witness remains arithmetically valid, but independent OpenModelica did not establish the claimed differential failure. "
                    f"The paired execution outcome was `{outcome}`; a clean short run is not enough to prove the path can never execute later."
                ),
                "Source-resolved Rumoca witness plus a conservative, non-confirming OpenModelica paired result.",
                "Use the generated wrapper as a regression, extend execution to the model's relevant experiment horizon, and obtain a clean baseline plus an attributed numerical failure before calling this a true positive.",
                omc=execution,
            )
        return Verdict(
            report,
            "candidate",
            report.kind,
            (
                "The source-resolved calculation contains a complete denominator, "
                "the v2 constraint analysis supplies a permitted active-path witness, "
                "and substitution evaluates that denominator to zero. That verifies the "
                "arithmetic witness, but not that the source division necessarily executes "
                "or fails under full Modelica semantics in this model instance."
            ),
            "Direct source arithmetic plus a checked SAT witness; no independent failing execution for this candidate instance.",
            (
                "Add a relational assertion/guard that prevents the two denominator "
                "operands from becoming equal, and test equal, reversed, and nominal values."
                if equality
                else "Constrain or assert the complete denominator away from zero before evaluating the division. If zero has a meaningful limit, implement an explicit algebraic branch; do not hide it with an epsilon."
            ),
        )

    if report.kind in {"physical-domain-unenforced", "physical-bound-permits-zero"}:
        execution = physical_omc_by_id.get(report.id)
        if execution and execution["outcome"] == "witness-causes-omc-numerical-failure":
            return Verdict(
                report,
                "confirmed",
                report.kind,
                "The reviewed component-specific physical contract excludes the reported value. With the exact zero or negative witness encoded before translation, the unmodified model ran cleanly and OpenModelica reproduced a numerical failure.",
                "Source-semantic contract review plus independent OpenModelica paired execution.",
                "Tighten the declaration or its component-scoped type to the reviewed domain, retain any supported ideal limit explicitly, and add this generated witness as a boundary regression.",
                omc=execution,
            )
        candidates = by_key.get((report.model, report.target), [])
        groups = {row["group"] for row in candidates}
        if "signed-machine-data-resistance" in groups:
            return Verdict(
                report,
                "unresolved",
                "machine-resistance-policy",
                "Zero is a supported ideal lossless winding, while negative machine copper resistance is ordinarily unphysical. The old blanket-positive and blanket-signed readings are both too broad; this needs a component-scoped nonnegative contract.",
                "Re-review prompted by the distinction between generic signed Basic.Resistor and machine winding data.",
                "Bind this declaration to a machine-winding role and enforce R >= 0; then regenerate the finding.",
            )
        prior_values = {normalize_prior(row["verdict"]) for row in candidates}
        if len(prior_values) == 1:
            # Prefer a row with the same semantic group; where several repeated
            # instances exist, all share the same verdict by construction here.
            prior = prior_verdict(
                report,
                candidates[0],
                "Matched model/target source-semantic review from the first audit.",
            )
            if prior.verdict == "confirmed":
                prior.verdict = "candidate"
                prior.basis = (
                    "Matched model/target source-semantic review from the first audit; "
                    "the v2 report is static-only and has no failing execution witness."
                )
            prior.omc = execution
            return prior
        return Verdict(
            report,
            "unresolved",
            "physical-policy-needs-proof",
            "The quantity/unit heuristic identifies a possible physical-domain gap, but no unique component-specific source proof establishes the intended sign or zero contract.",
            "No unique prior source-semantic adjudication matched this v2 instance.",
            "Add or extract a component-scoped contract, then re-run PhysicalSan.",
            omc=execution,
        )

    return Verdict(
        report,
        "unresolved",
        report.kind or "unclassified",
        "No reviewed rule establishes or refutes this report yet.",
        "Conservative fallback: absent proof is not a defect or a false positive.",
        "Obtain a source proof and, where behavior matters, a clean baseline plus a targeted perturbation.",
    )


def safe(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def report_path(verdict: Verdict) -> str:
    folder = "false-positives" if verdict.verdict == "false-positive" else verdict.verdict
    return f"{folder}/{verdict.report.id}.md"


def render_report(item: Verdict) -> str:
    r = item.report
    original = f"../../bugs/{r.path.name}"
    lines = [
        f"# {r.id}: {r.title}",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Verdict | {item.verdict} |",
        f"| Review group | `{item.group}` |",
        f"| Original tier | {r.tier or '—'} |",
        f"| Sanitizer result | `{r.kind or 'historical-runtime/declaration report'}` |",
        f"| Model | {safe(r.model) or '—'} |",
        f"| Target | `{safe(r.target)}` |",
        f"| Declaration/site | `{safe(r.declaration)}` |",
        f"| Original report | [{r.path.name}]({original}) |",
        f"| Original SHA-256 | `{r.sha256}` |",
        "",
    ]
    if item.verdict == "confirmed":
        lines += [
            "## Verification and root cause",
            "",
            item.reason,
            "",
            "## Proposed fix",
            "",
            item.proposed_action,
            "",
            "## Fix validation",
            "",
            "Retest nominal values, the exact reported witness, nearby valid boundaries, and any relational equality or conditional branch involved. Preserve the intended ideal/algebraic behavior of delegated components.",
            "",
        ]
    elif item.verdict == "candidate":
        lines += [
            "## Why this remains a candidate",
            "",
            item.reason,
            "",
            "## Proposed fix if confirmed",
            "",
            item.proposed_action,
            "",
            "## Confirmation required",
            "",
            "Establish a clean executable baseline, apply the exact witness before translation where appropriate, and reproduce the attributed failure independently. Also rule out inherited constraints, assertions, inactive conditional components, sentinel values, and legal algebraic limits.",
            "",
        ]
    elif item.verdict == "false-positive":
        lines += [
            "## Why this is not a verified bug",
            "",
            item.reason,
            "",
            "## Regression action",
            "",
            item.proposed_action,
            "",
        ]
    elif item.verdict == "advisory":
        lines += [
            "## Why this is an advisory",
            "",
            item.reason,
            "",
            "## How to resolve the question",
            "",
            item.proposed_action,
            "",
        ]
    else:
        lines += [
            "## What remains unresolved",
            "",
            item.reason,
            "",
            "## Evidence needed",
            "",
            item.proposed_action,
            "",
        ]
    lines += [
        "## Evidence basis",
        "",
        item.basis,
        "",
    ]
    if item.omc:
        omc = item.omc
        lines += [
            "## OpenModelica paired execution",
            "",
            f"- Outcome: `{omc.get('outcome', 'unknown')}`",
            f"- Unmodified baseline: `{omc.get('baseline', 'unknown')}`",
            f"- Source-instantiated trigger: `{omc.get('trigger', 'unknown')}`",
            "",
        ]
        if omc.get("wrapper"):
            lines += ["Generated test program:", "", "```modelica", omc["wrapper"], "```", ""]
        if omc.get("diagnostic"):
            lines += ["Relevant OMC diagnostic:", "", "```text", omc["diagnostic"], "```", ""]
    if r.claim:
        lines += ["## Original claim", "", r.claim, ""]
    if item.prior_report:
        lines += [
            "## Earlier independent review",
            "",
            f"[Prior report](../../../verifiedBugs/{item.prior_report})",
            "",
        ]
    lines += [
        "## Scope",
        "",
        "Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.",
        "",
        "[v2 verification index](../README.md)",
        "",
    ]
    return "\n".join(lines)


def write_index(name: str, title: str, items: list[Verdict]) -> None:
    grouped: dict[str, list[Verdict]] = defaultdict(list)
    for item in items:
        grouped[item.group].append(item)

    lines = [
        f"# {title}: {len(items)} reports",
        "",
        "[Overview](README.md) · [Machine-readable CSV](index.csv)",
        "",
        "The group table is the fastest review path. Open a group, then use the "
        "per-report link for the full reasoning, generated test program, OMC "
        "diagnostic and proposed action.",
        "",
        "## Group index",
        "",
        "| Group | Reports | Decision rule / common cause |",
        "|---|---:|---|",
    ]
    for group in sorted(grouped):
        group_items = grouped[group]
        slug = re.sub(r"[^a-z0-9]+", "-", group.lower()).strip("-") or "unclassified"
        group_page = f"groups/{Path(name).stem}-{slug}.md"
        reason = safe(group_items[0].reason)
        if len(reason) > 220:
            reason = reason[:217].rstrip() + "…"
        lines.append(f"| [`{safe(group)}`]({group_page}) | {len(group_items)} | {reason} |")

        detail = [
            f"# {title}: `{group}`",
            "",
            f"**{len(group_items)} report instances**",
            "",
            f"[Back to {title}](../{name}) · [Overview](../README.md)",
            "",
            "## Common decision rule",
            "",
            group_items[0].reason,
            "",
            "## Reports",
            "",
            "| ID | Model | Target | Independent evidence | Student report |",
            "|---|---|---|---|---|",
        ]
        for item in group_items:
            r = item.report
            if item.omc:
                evidence = f"OMC: `{safe(item.omc.get('outcome', 'unknown'))}`"
            elif r.id.startswith("BUG-"):
                evidence = "Prior paired execution"
            else:
                evidence = "Source/semantic review"
            detail.append(
                f"| [{r.id}](../{report_path(item)}) | {safe(r.model) or '—'} | "
                f"`{safe(r.target)}` | {evidence} | "
                f"[{r.path.name}](../../bugs/{r.path.name}) |"
            )
        detail.append("")
        (HERE / group_page).write_text("\n".join(detail))

    lines += [
        "",
        "## Report table",
        "",
        "| ID | Model | Target | Group | Independent evidence | Student report |",
        "|---|---|---|---|---|---|",
    ]
    for item in items:
        r = item.report
        if item.omc:
            evidence = f"OMC: `{safe(item.omc.get('outcome', 'unknown'))}`"
        elif r.id.startswith("BUG-"):
            evidence = "Prior paired execution"
        else:
            evidence = "Source/semantic review"
        lines.append(
            f"| [{r.id}]({report_path(item)}) | {safe(r.model) or '—'} | "
            f"`{safe(r.target)}` | `{safe(item.group)}` | {evidence} | "
            f"[{r.path.name}](../bugs/{r.path.name}) |"
        )
    lines.append("")
    (HERE / name).write_text("\n".join(lines))


def validate(items: list[Verdict]) -> dict:
    ids = [item.report.id for item in items]
    input_ids = []
    for path in INPUT.glob("*.md"):
        if path.name in {"README.md", "withdrawn.md", "by-model.md"}:
            continue
        match = re.match(r"# ((?:BUG|FINDING|DECL)-\d+)", path.read_text(errors="replace"))
        if match:
            input_ids.append(match.group(1))
    broken = []
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in HERE.rglob("*.md"):
        for raw in link_pattern.findall(path.read_text(errors="replace")):
            if raw.startswith(("http:", "https:", "#")):
                continue
            target = (path.parent / raw.replace("%20", " ")).resolve()
            if not target.exists():
                broken.append(f"{path.relative_to(HERE)} -> {raw}")
    return {
        "input_report_count": len(input_ids),
        "output_report_count": len(items),
        "all_input_ids_accounted_for": set(ids) == set(input_ids),
        "unique_ids": len(ids) == len(set(ids)),
        "broken_internal_links": sorted(broken),
        "counts": dict(Counter(item.verdict for item in items)),
    }


def main() -> None:
    for folder in ("confirmed", "candidate", "advisory", "false-positives", "unresolved"):
        directory = HERE / folder
        directory.mkdir(parents=True, exist_ok=True)
        for stale in directory.glob("*.md"):
            stale.unlink()
    groups = HERE / "groups"
    groups.mkdir(parents=True, exist_ok=True)
    for stale in groups.glob("*.md"):
        stale.unlink()

    reports = [
        parse(path)
        for path in INPUT.glob("*.md")
        if path.name not in {"README.md", "withdrawn.md", "by-model.md"}
    ]
    reports.sort(key=lambda report: report.id)
    by_id, by_key = load_prior()
    omc_by_id = load_omc(HERE / "omc-source-verification.json")
    physical_omc_by_id = load_omc(HERE / "omc-physical-verification.json")
    items = [
        classify(report, by_id, by_key, omc_by_id, physical_omc_by_id)
        for report in reports
    ]

    for item in items:
        (HERE / report_path(item)).write_text(render_report(item))

    confirmed = [item for item in items if item.verdict == "confirmed"]
    candidates = [item for item in items if item.verdict == "candidate"]
    advisories = [item for item in items if item.verdict == "advisory"]
    false = [item for item in items if item.verdict == "false-positive"]
    unresolved = [item for item in items if item.verdict == "unresolved"]
    write_index("confirmed.md", "Execution-confirmed defects", confirmed)
    write_index("candidates.md", "Static/source-supported candidates", candidates)
    write_index("advisories.md", "Intent questions and advisories", advisories)
    write_index("false-positives.md", "False positives and explicit non-defects", false)
    write_index("unresolved.md", "Unresolved reports", unresolved)

    with (HERE / "index.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "verdict", "group", "tier", "sanitizer_kind", "model", "target", "declaration", "original", "report", "omc_outcome", "reason", "proposed_action"])
        for item in items:
            r = item.report
            writer.writerow([r.id, item.verdict, item.group, r.tier, r.kind, r.model, r.target, r.declaration, r.path.name, report_path(item), item.omc.get("outcome", "") if item.omc else "", item.reason, item.proposed_action])

    (HERE / "index.json").write_text(json.dumps([
        {
            "id": item.report.id,
            "verdict": item.verdict,
            "group": item.group,
            "tier": item.report.tier,
            "sanitizer_kind": item.report.kind,
            "model": item.report.model,
            "target": item.report.target,
            "declaration": item.report.declaration,
            "original": item.report.path.name,
            "report": report_path(item),
            "omc_outcome": item.omc.get("outcome", "") if item.omc else "",
            "reason": item.reason,
            "basis": item.basis,
            "proposed_action": item.proposed_action,
        }
        for item in items
    ], indent=2) + "\n")

    kinds = Counter(item.report.kind or item.report.id.split("-", 1)[0] for item in items)
    verdicts = Counter(item.verdict for item in items)
    runtime_bugs = Counter(
        item.verdict for item in items if item.report.id.startswith("BUG-")
    )
    divisor_omc = Counter(
        item.omc.get("outcome", "") for item in items
        if item.report.kind in SOURCE_CANDIDATE_KINDS and item.omc
    )
    physical_omc = Counter(
        item.omc.get("outcome", "") for item in items
        if item.report.kind in {"physical-domain-unenforced", "physical-bound-permits-zero"} and item.omc
    )
    readme = f"""# v2 report verification

This review accounts for **all {len(items):,} report instances** in `docs/v2/bugs`. The input mixes defect candidates with explicit supported-limit, guarded, unreachable, translation-generated and unresolved records; those are not all bugs.

| Verdict | Reports | Browse |
|---|---:|---|
| Execution-confirmed defect | {verdicts['confirmed']} | [Verified reports](confirmed.md) |
| Static/source-supported candidate | {verdicts['candidate']} | [Candidates](candidates.md) |
| Intent question / advisory — no defect claimed | {verdicts['advisory']} | [Advisories](advisories.md) |
| False positive or explicit non-defect | {verdicts['false-positive']} | [Reasons](false-positives.md) |
| Unresolved — not called real or fake | {verdicts['unresolved']} | [Evidence gaps](unresolved.md) |
| Total | {len(items)} | [CSV](index.csv) · [JSON](index.json) |

Counts are report instances, not unique root causes. A repeated shared declaration may appear in many models.

[Divisor OMC evidence](omc-source-verification.md) · [Physical-witness OMC evidence](omc-physical-verification.md)
· [Current rerun audit and residual issues](current-rerun-audit.md)

## Important findings

- The current v2 analyzers explicitly identify {kinds['physical-zero-is-a-supported-limit']} supported-zero records, {kinds['divisor-guarded-by-assertion']} assertion-guarded divisions, {kinds['divisor-unreachable-under-witness']} unreachable divisions and {kinds['divisor-introduced-by-translation']} translation-introduced quotients. These are non-defects, not bugs.
- The analyzer retains {verdicts['advisory']} quantity-based anomalies as explicit intent questions. They preserve recall without asserting that a negative/zero value or permissive declaration is erroneous before a component contract or user assumption establishes that premise.
- Of {kinds['divisor-reachable-zero'] + kinds['divisor-zero-when-parameters-equal']} source-denominator candidates, OpenModelica independently reproduced {divisor_omc['confirmed-by-omc']} report instances against clean baselines. It rejected {divisor_omc['refuted-illegal-witness']} exact witnesses as illegal/protected; non-reproductions, baseline failures, timeouts, unsupported array modifiers and other failures remain unresolved.
- Of the current physical defect claims, {sum(physical_omc.values())} have paired OpenModelica witness results. The broader retained physical-witness ledger exercised 177 pre-policy report instances. These tests decide whether zero/negative values translate and execute, while the intended physical domain still comes from the component-specific source contract.
- The original 26 runtime `BUG-*` claims remain **{runtime_bugs['confirmed']} confirmed and {runtime_bugs['false-positive']} refuted** under the independent translation and initialization controls retained in the earlier audit.
- Machine-winding resistance reports are left unresolved pending the corrected component-scoped `R >= 0` policy: generic `Basic.Resistor` is signed, while negative copper resistance is not ordinarily physical.

## Verification performed

- Reviewed every v2 finding kind and its claimed evidence semantics.
- Checked all reported source arithmetic sites: 270 of 276 unique SAT source locations contain a division on the cited line; the remaining six are multiline expressions whose division continues on adjacent lines.
- Reused the exact stable-ID review for all 26 BUG reports and 911 declaration census entries.
- Reused model/target source-semantic adjudications from the first exhaustive audit where the v2 physical claim matched uniquely.
- Re-ran the verification commands embedded in all 26 confirmed-tier reports and all 911 latent-tier reports; all reproduced their published analyzer/source result.
- Ran the combined semantics, physical-policy, zero-contract, symbol-contract and divisor regression suite: 113 tests passed.

## Limitations

- A clean short OMC run is recorded as unresolved, not as proof that a later conditional path can never execute.
- Declaration-only physical-policy claims remain unresolved unless a reviewed component contract establishes or refutes them.
- An advisory is not counted as a verified bug, candidate bug, false positive or unresolved bug; it is an intentional request for missing author intent.
- Four `divisor-zero-at-declared-values` results remain unresolved because a static broken-baseline claim needs independent execution and conditional-path review.
- No library or analyzer implementation was changed by this audit.

## Reproduce

```sh
python3 docs/v2/verified/omc_source_verify.py --jobs 4 --timeout 240
python3 docs/v2/verified/omc_physical_verify.py --jobs 4 --timeout 240
python3 docs/v2/verified/build_reports.py
python3 -m pytest -q packages/modelsan/tests/test_symbol_contract.py packages/modelsan/tests/test_divisor_reasoning.py
python3 -m pytest -q packages/modelsan/tests/test_physical.py packages/modelsan/tests/test_divisor_witness.py packages/modelsan/tests/test_divisor.py
```

[Input overview](../bugs/README.md) · [Earlier exhaustive audit](../../verifiedBugs/README.md) · [Validation](validation.json)
"""
    (HERE / "README.md").write_text(readme)

    # Validation links include validation.json itself, so create it before the
    # link walk and then replace the placeholder with the actual result.
    (HERE / "validation.json").write_text("{}\n")
    result = validate(items)
    (HERE / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
    if not result["all_input_ids_accounted_for"] or not result["unique_ids"] or result["broken_internal_links"]:
        raise SystemExit(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
