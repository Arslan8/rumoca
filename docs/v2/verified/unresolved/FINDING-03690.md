# FINDING-03690: `pulse2.twoPulse.filter[1].fCut` in `ThyristorBridge2Pulse_DC_Drive`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive |
| Target | `pulse2.twoPulse.filter[1].fCut` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/PowerConverters/ACDC/Control/Filter.mo:9` |
| Original report | [FINDING-thyristorbridge2pulse-dc-drive-pulse2-twopulse-filter-1-fcut-divzero-2.md](../../bugs/FINDING-thyristorbridge2pulse-dc-drive-pulse2-twopulse-filter-1-fcut-divzero-2.md) |
| Original SHA-256 | `4b9c7cefee09a2a619bfec91d4f8ad5ce0d2fae8e37e949352f9f259ac04d792` |

## What remains unresolved

The static denominator witness remains arithmetically valid, but independent OpenModelica did not establish the claimed differential failure. The paired execution outcome was `not-attempted-array-element-modifier-needs-specialized-wrapper`; a clean short run is not enough to prove the path can never execute later.

## Evidence needed

Use the generated wrapper as a regression, extend execution to the model's relevant experiment horizon, and obtain a clean baseline plus an attributed numerical failure before calling this a true positive.

## Evidence basis

Source-resolved Rumoca witness plus a conservative, non-confirming OpenModelica paired result.

## OpenModelica paired execution

- Outcome: `not-attempted-array-element-modifier-needs-specialized-wrapper`
- Unmodified baseline: `unknown`
- Source-instantiated trigger: `unknown`

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
