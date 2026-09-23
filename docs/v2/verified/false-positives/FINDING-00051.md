# FINDING-00051: `invMixingUnit.tau0` in `MixingUnitWithContinuousControl`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.MixingUnitWithContinuousControl |
| Target | `invMixingUnit.tau0` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Clocked/Examples/Systems/Utilities/ComponentsMixingUnit/MixingUnit.mo:28` |
| Original report | [FINDING-mixingunitwithcontinuouscontrol-invmixingunit-tau0-divzero-5.md](../../bugs/FINDING-mixingunitwithcontinuouscontrol-invmixingunit-tau0-divzero-5.md) |
| Original SHA-256 | `d3f6f14c5164d5df4c090408e98e958e3e9293b33447e37e3f70e40fcdaee960` |

## Why this is not a verified bug

OpenModelica rejects the report's exact source modification because the named nested element is protected, final, otherwise non-modifiable, or violates a binding rule. The report therefore does not supply a legal executable witness for its claim.

## Regression action

Keep this report as a regression: the analysis must carry modifiability/visibility through qualified component paths and must not offer an illegal parameter assignment as a witness.

## Evidence basis

Independent OpenModelica source translation of the exact witness refuted its admissibility.

## OpenModelica paired execution

- Outcome: `refuted-illegal-witness`
- Unmodified baseline: `clean`
- Source-instantiated trigger: `failed`

Generated test program:

```modelica
model V2OMC_9a2075b460dd4c5f
  extends Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.MixingUnitWithContinuousControl(invMixingUnit.tau0=0);
end V2OMC_9a2075b460dd4c5f;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_9a2075b460dd4c5f",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Clocked/Examples/Systems/Utilities/ComponentsMixingUnit/MixingUnit.mo:23:3-23:30:writable] Error: Protected element 'tau0' may not be modified, got 'tau0 = 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
