# FINDING-03222: `transformerData2.I2ph` in `Rectifier12pulse`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Machines.Examples.Transformers.Rectifier12pulse |
| Target | `transformerData2.I2ph` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/TransformerData.mo:45` |
| Original report | [FINDING-rectifier12pulse-transformerdata2-i2ph-divzero-3.md](../../bugs/FINDING-rectifier12pulse-transformerdata2-i2ph-divzero-3.md) |
| Original SHA-256 | `17efc0f04a2aeb0b1a3b4d96dbef33ce443ba0774d5f34317db873b130b05763` |

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
model V2OMC_78f4c4630e4f68ef
  extends Modelica.Electrical.Machines.Examples.Transformers.Rectifier12pulse(transformerData2.I2ph=0);
end V2OMC_78f4c4630e4f68ef;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_78f4c4630e4f68ef",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/TransformerData.mo:33:3-34:36:writable] Error: Trying to override final element I2ph with modifier '= 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
