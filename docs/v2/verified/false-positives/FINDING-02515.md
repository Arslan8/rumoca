# FINDING-02515: `smeeData.omega` in `SMEE_Generator`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator |
| Target | `smeeData.omega` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/SynchronousMachineData.mo:104` |
| Original report | [FINDING-smee-generator-smeedata-omega-divzero-14.md](../../bugs/FINDING-smee-generator-smeedata-omega-divzero-14.md) |
| Original SHA-256 | `e3006fc15f87a1dfc983b42169bec81c7a4e4499b3b901cc4663082acd5a4a17` |

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
model V2OMC_e8e7b2b938da505f
  extends Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator(smeeData.omega=0);
end V2OMC_e8e7b2b938da505f;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_e8e7b2b938da505f",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/SynchronousMachineData.mo:16:3-17:32:writable] Error: Trying to override final element omega with modifier '= 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
