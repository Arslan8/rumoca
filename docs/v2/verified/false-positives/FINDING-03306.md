# FINDING-03306: `transformerData.V2ph` in `TransformerTestbench`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Machines.Examples.Transformers.TransformerTestbench |
| Target | `transformerData.V2ph` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/TransformerData.mo:33` |
| Original report | [FINDING-transformertestbench-transformerdata-v2ph-divzero-2.md](../../bugs/FINDING-transformertestbench-transformerdata-v2ph-divzero-2.md) |
| Original SHA-256 | `e63427623ea212b07af369d4875c369c8e2b7d60532fd77316b30f848754648f` |

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
model V2OMC_835dd1bd36b7332f
  extends Modelica.Electrical.Machines.Examples.Transformers.TransformerTestbench(transformerData.V2ph=0);
end V2OMC_835dd1bd36b7332f;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_835dd1bd36b7332f",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/TransformerData.mo:31:3-32:53:writable] Error: Trying to override final element V2ph with modifier '= 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
