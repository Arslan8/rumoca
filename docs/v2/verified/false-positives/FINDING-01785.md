# FINDING-01785: `aimc.spacePhasorS.turnsRatio` in `IMC_DOL`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL |
| Target | `aimc.spacePhasorS.turnsRatio` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/SpacePhasors/Components/SpacePhasor.mo:26` |
| Original report | [FINDING-imc-dol-aimc-spacephasors-turnsratio-divzero.md](../../bugs/FINDING-imc-dol-aimc-spacephasors-turnsratio-divzero.md) |
| Original SHA-256 | `de7caa9420663d6ccdb27a3831dda2aab801ee371e8170eef77c5992a25a766d` |

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
model V2OMC_b3a1b570489a198b
  extends Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL(aimc.spacePhasorS.turnsRatio=0);
end V2OMC_b3a1b570489a198b;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_b3a1b570489a198b",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo:93:67-93:79:writable] Error: Trying to override final element turnsRatio with modifier '= 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
