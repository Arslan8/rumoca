# FINDING-04321: `material.B_myMax` in `AdvancedSolenoid`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid |
| Target | `material.B_myMax` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/BaseClasses/FixedShape.mo:31` |
| Original report | [FINDING-advancedsolenoid-material-b-mymax-divzero-6.md](../../bugs/FINDING-advancedsolenoid-material-b-mymax-divzero-6.md) |
| Original SHA-256 | `94cba72871515105bd3a44de4452589b959f16771926a88bc75cd2253774233e` |

## What remains unresolved

The static denominator witness remains arithmetically valid, but independent OpenModelica did not establish the claimed differential failure. The paired execution outcome was `unresolved-baseline-fails`; a clean short run is not enough to prove the path can never execute later.

## Evidence needed

Use the generated wrapper as a regression, extend execution to the model's relevant experiment horizon, and obtain a clean baseline plus an attributed numerical failure before calling this a true positive.

## Evidence basis

Source-resolved Rumoca witness plus a conservative, non-confirming OpenModelica paired result.

## OpenModelica paired execution

- Outcome: `unresolved-baseline-fails`
- Unmodified baseline: `failed`
- Source-instantiated trigger: `failed`

Generated test program:

```modelica
model V2OMC_28a6fead2d9f2354
  extends Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid(material.B_myMax=0);
end V2OMC_28a6fead2d9f2354;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_28a6fead2d9f2354",
Error: Internal error IndexReduction.pantelidesIndexReduction failed! Found empty set of continuous equations. Use -d=bltdump to get more information.
Error: Internal error Transformation Module PFPlusExt index Reduction Method Pantelides failed!
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
