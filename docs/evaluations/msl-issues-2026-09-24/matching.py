"""Conservative report-to-finding matching for the 2026-09-24 audit.

``score(row, result)`` is a drop-in replacement for evaluate.score. An exact
match means the historical *reported operation* was rediscovered, not that its
ground-truth verdict was re-proven. ``summarize(rows)`` counts this distinction.
No stable identity is inferred from changed expression IDs, model basenames,
or a parameter name alone. Equivalent formatting is normalized syntactically;
algebraic equivalence, branch reachability, and new witnesses are not invented.
"""
from __future__ import annotations

import ast
from collections import Counter
from decimal import Decimal, InvalidOperation
from functools import lru_cache
import hashlib
import html
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "target/msl-issue-evaluation-20260924/corpus"
NONDEFECT = {"physical-zero-is-a-supported-limit", "physical-rule-does-not-apply",
             "divisor-guarded-by-assertion", "divisor-unreachable-under-witness",
             "divisor-introduced-by-translation"}
UNDECIDED = {"divisor-zero-unresolved", "physical-inertia-tensor-undecided"}
ADVISORY = {"physical-intent-question", "physical-runtime-invariant-unobserved"}
DEFECT = {"divisor-reachable-zero", "divisor-zero-at-declared-values",
          "divisor-zero-when-parameters-equal", "physical-bound-permits-zero",
          "physical-domain-unenforced", "physical-inertia-tensor-not-semidefinite",
          "physical-invariant-violated"}
NAME = r"[A-Za-z_]\w*(?:\.\w+|\[\d+\])*"


def _clean(value):
    return html.unescape(str(value)).strip().strip("`").replace("\\|", "|")


def _tree(node):
    """AST identity with decimal-valued literals, not evaluated arithmetic."""
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return ("number", str(Decimal(str(node.value)).normalize()))
    return (type(node).__name__, tuple((field, _tree(value) if isinstance(value, ast.AST)
            else tuple(_tree(v) if isinstance(v, ast.AST) else v for v in value)
            if isinstance(value, list) else value) for field, value in ast.iter_fields(node)))


def expression(value):
    """Ignore spaces/redundant parentheses, never reassociate/reorder operands."""
    text = _clean(value)
    try:
        # Modelica power and inequality have equivalent Python AST structure.
        return _tree(ast.parse(text.replace("^", "**").replace("<>", "!="), mode="eval"))
    except (SyntaxError, ValueError, RecursionError):
        return ("tokens", tuple(re.findall(r"\w+|[^\s]", text)))


def witness(value):
    """Compare the full assignment set, including array indices and values."""
    text = _clean(value)
    pieces = re.split(r",\s*(?=" + NAME + r"\s*=)", text)
    assignments = []
    for piece in pieces:
        match = re.fullmatch(r"(" + NAME + r")\s*=\s*(.+)", piece.strip())
        if not match:
            return ("unparsed", expression(text))
        try:
            number = Decimal(match[2]).normalize()
            if not number.is_finite():
                raise InvalidOperation
            assignments.append((match[1], "0" if number == 0 else str(number)))
        except InvalidOperation:
            assignments.append((match[1], expression(match[2])))
    return tuple(sorted(assignments, key=lambda pair: pair[0]))


@lru_cache(maxsize=None)
def _original(filename):
    path = ROOT / "docs/v2/bugs" / filename
    if not filename or not path.is_file():
        return {"error": "original-report-unavailable", "evidence": {}}
    text = path.read_text()
    section = re.search(r"^## Evidence\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    evidence = {}
    if section:
        for match in re.finditer(r"^\| `([^`]+)` \| (.*) \|$", section[1], re.M):
            evidence[match[1]] = _clean(match[2])
    # Older BUG files put semantic ownership in a printed dictionary, not the
    # table. literal_eval only decodes a literal; it never executes report text.
    for block in re.findall(r"```\n(\{[^\n]+\})\n```", text):
        try:
            data = ast.literal_eval(block)
            if isinstance(data, dict) and "declaring_class" in data:
                evidence.setdefault("canonical_declaration", ".".join(
                    str(data[k]) for k in ("declaring_class", "member") if data.get(k)))
        except (ValueError, SyntaxError):
            pass
    signature = re.search(r"^\| \*\*Signature\*\* \| `([^`]+)`", text, re.M)
    return {"evidence": evidence, "sha256": hashlib.sha256(text.encode()).hexdigest(),
            "signature": signature[1] if signature else None}


def _source(path):
    text = str(path).replace("\\", "/").strip("`")
    match = re.search(r"(?:^|/)(Modelica(?:Test)?)(?: [0-9][^/]*)?/(.+)$", text)
    return match[1] + "/" + match[2] if match else text


def _location(value):
    match = re.fullmatch(r"(.+?):(\d+)(?::\d+)?", str(value))
    return (_source(match[1]), int(match[2])) if match else (_source(value), None)


def _declaration(evidence):
    nested = evidence.get("matched_by", {})
    return evidence.get("canonical_declaration") or (
        nested.get("canonical_declaration") if isinstance(nested, dict) else None)


def _source_comparison(row, old, finding):
    historical, line = _location(row.get("declaration", ""))
    locations = [(_source(loc.get("file", "")), loc.get("line"))
                 for loc in finding.get("source_locations", [])]
    if not historical or line is None or not locations:
        return "unavailable"
    if "/" in historical:
        return "exact-path-line" if (historical, line) in locations else "different"
    candidates = [path for path, current_line in locations
                  if Path(path).name == historical and current_line == line]
    if not candidates:
        return "different"
    # Resolve old basename-only sites only with independently recorded semantic
    # ownership, or when the named top-level model is itself the source owner.
    old_decl = _declaration(old)
    new_decl = _declaration(finding.get("evidence", {}))
    if old_decl and old_decl == new_decl:
        return "canonical-declaration-line"
    owner_path = row.get("model", "").replace(".", "/") + ".mo"
    if owner_path in candidates:
        return "model-owner-path-line"
    return "basename-line-only"


def _equal(old, new, key, normalize=expression):
    if key not in old or key not in new or old[key] in (None, "") or new[key] in (None, ""):
        return "unavailable"
    return "same" if normalize(old[key]) == normalize(new[key]) else "different"


def _names(finding):
    evidence = finding.get("evidence", {})
    values = [str(evidence.get(k, "")) for k in
              ("parameter", "required", "where", "observed", "variable", "state",
               "equation", "denominator", "witness", "path")]
    names = set(re.findall(NAME, " ".join(values)))
    names.update(a.get("name") for a in finding.get("canonical_anchors", []) if a.get("name"))
    return names


def compare(row, old, finding):
    """Return explainable operation evidence without treating similarity as proof."""
    new = finding.get("evidence", {})
    comparison = {
        "source": _source_comparison(row, old, finding),
        "historical_source": row.get("declaration"),
        "current_sources": finding.get("source_locations", []),
        "historical_denominator": old.get("denominator"),
        "current_denominator": new.get("denominator"),
        "denominator": _equal(old, new, "denominator"),
        "historical_witness": old.get("witness"),
        "current_witness": new.get("witness"),
        "witness": _equal(old, new, "witness", witness),
        "path_condition": _equal(old, new, "path_condition"),
        "rule": _equal(old, new, "rule"),
        "required": _equal(old, new, "required"),
    }
    source_exact = comparison["source"] in {
        "exact-path-line", "canonical-declaration-line", "model-owner-path-line"}
    if row["sanitizer_kind"].startswith("divisor"):
        operation_exact = comparison["denominator"] == "same"
        witness_exact = comparison["witness"] == "same"
        path_compatible = comparison["path_condition"] != "different"
        exact = source_exact and operation_exact and witness_exact and path_compatible
    else:
        # Physical reports identify declaration + rule, not an arithmetic op.
        exact = source_exact and comparison["rule"] == "same" and comparison["required"] == "same"
    comparison["match"] = "exact" if exact else "ambiguous"
    comparison["current_expression_ids"] = [a.get("dae_id") for a in
        finding.get("canonical_anchors", []) if a.get("kind") == "expression"]
    return comparison


def _decision(findings):
    kinds = {finding["kind"] for finding in findings}
    if kinds & DEFECT:
        return "static-defect-candidate"
    if kinds & NONDEFECT:
        return "explicit-nondefect"
    if kinds & ADVISORY:
        return "intent-advisory"
    return "unresolved-analysis" if kinds else "not-reported"


def score(row, result):
    """Keep target-level detection compatible and expose strict_detection separately."""
    output = dict(row)
    key = hashlib.sha256(row["model"].encode()).hexdigest()[:16]
    output.update(model_evidence=str((OUT / key / "static.json").relative_to(ROOT)),
                  analysis_status=result["status"], matched_findings=[], ambiguous_findings=[],
                  exact_kind_present=False, matching="unavailable", operation_match="unavailable",
                  exact_candidate=False, target_hints=[])
    if result["status"] != "analyzed":
        output["detection"] = "blocked-before-analysis"
        output["strict_detection"] = "blocked-before-analysis"
        return output
    original = _original(row.get("original", ""))
    old = original["evidence"]
    output["historical_operation"] = {"source": row.get("declaration"),
        "evidence": old, "original_sha256": original.get("sha256"),
        "historical_signature": original.get("signature"), "error": original.get("error")}
    target = row["target"]
    wanted = "divisor" if row["sanitizer_kind"].startswith("divisor") else "physical"
    matching = [f for f in result.get("findings", [])
                if f.get("sanitizer") == wanted and target in _names(f)]
    for finding in matching:
        item = {key: finding.get(key) for key in
                ("kind", "severity", "source_locations", "evidence", "canonical_anchors")}
        item["operation_comparison"] = compare(row, old, finding)
        field = "matched_findings" if item["operation_comparison"]["match"] == "exact" else "ambiguous_findings"
        output[field].append(item)
    exact = output["matched_findings"]
    output["exact_kind_present"] = any(f["kind"] == row["sanitizer_kind"] for f in exact)
    output["target_kind_present"] = any(f["kind"] == row["sanitizer_kind"] for f in matching)
    output["target_detection"] = _decision(matching)
    if exact:
        output.update(matching="exact", strict_detection=_decision(exact))
    elif matching:
        output.update(matching="ambiguous", strict_detection="ambiguous-site-match")
    elif any(v["status"] != "ok" for k, v in result.get("analyses", {}).items()
             if k.startswith(wanted + ".")):
        output.update(matching="none", strict_detection="analyzer-error")
    else:
        output.update(matching="none", strict_detection="not-reported")
    output["operation_match"] = output["matching"]
    output["detection"] = output["target_detection"] if matching else output["strict_detection"]
    output["exact_candidate"] = output["strict_detection"] == "static-defect-candidate"
    output["target_hints"] = [h for h in result.get("hints", []) if h.get("target") == target]
    output["other_sanitizer_target_findings"] = [
        {key: f.get(key) for key in ("sanitizer", "kind", "severity", "evidence", "source_locations")}
        for f in result.get("findings", []) if f.get("sanitizer") != wanted and target in _names(f)]
    return output


def summarize(rows):
    """Report report-instance counts; deliberately do not claim unique recall."""
    return {
        "reports": len(rows),
        "detection": dict(sorted(Counter(r.get("detection", "unscored") for r in rows).items())),
        "strict_detection": dict(sorted(Counter(r.get("strict_detection", "unscored") for r in rows).items())),
        "matching": dict(sorted(Counter(r.get("matching", "not-applicable") for r in rows).items())),
        "by_verdict": {verdict: dict(sorted(Counter(r.get("detection", "unscored")
            for r in rows if r["verdict"] == verdict).items())) for verdict in sorted({r["verdict"] for r in rows})},
        "strict_by_verdict": {verdict: dict(sorted(Counter(r.get("strict_detection", "unscored")
            for r in rows if r["verdict"] == verdict).items())) for verdict in sorted({r["verdict"] for r in rows})},
        "interpretation": "Exact matches identify historical report operations, not newly verified defects. "
            "Ambiguous target-only matches are not strict detections; separate blocked models and unadjudicated reports.",
    }
