# FINDING-02852: `smpm.spacePhasorS.turnsRatio` in `SMPM_VoltageSource`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource |
| Target | `smpm.spacePhasorS.turnsRatio` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/SpacePhasors/Components/SpacePhasor.mo:26` |
| Original report | [FINDING-smpm-voltagesource-smpm-spacephasors-turnsratio-divzero.md](../../bugs/FINDING-smpm-voltagesource-smpm-spacephasors-turnsratio-divzero.md) |
| Original SHA-256 | `ac6349ee0c1b373a8e761cfee8b3a30bdb6fb3a3fbecb07c98dca53e1cb00c3d` |

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
model V2OMC_72b9ce8e63201baa
  extends Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource(smpm.spacePhasorS.turnsRatio=0);
end V2OMC_72b9ce8e63201baa;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_72b9ce8e63201baa",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo:93:67-93:79:writable] Error: Trying to override final element turnsRatio with modifier '= 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
