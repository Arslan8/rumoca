# FINDING-00554: `line3.Z0` in `CompareLosslessLines`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `guarded-transmission-line` |
| Original tier | Candidate |
| Sanitizer result | `physical-domain-unenforced` |
| Model | Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines |
| Target | `line3.Z0` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Lines/TLine.mo:5` |
| Original report | [FINDING-comparelosslesslines-line3-z0-unbounded.md](../../bugs/FINDING-comparelosslesslines-line3-z0-unbounded.md) |
| Original SHA-256 | `a642bc60ac51c1b848794cc580f67051277c6e462795b83cbff914c1e2b03aae` |

## Why this is not a verified bug

TLine explicitly asserts Z0>0 before its port equations divide by Z0. The declaration lacks a min modifier, but the claimed missing domain enforcement is false because an executable assertion supplies it.

## Regression action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Evidence basis

Matched model/target source-semantic review from the first audit.

## Original claim

Nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones. It does **not** claim that any model actually sets such a value.

## Earlier independent review

[Prior report](../../../verifiedBugs/false-positives/FINDING-00503.md)

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
