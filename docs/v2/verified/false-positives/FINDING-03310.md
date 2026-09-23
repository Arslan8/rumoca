# FINDING-03310: `transformerData.I1ph` in `TransformerTestbench`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Machines.Examples.Transformers.TransformerTestbench |
| Target | `transformerData.I1ph` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/TransformerData.mo:37` |
| Original report | [FINDING-transformertestbench-transformerdata-i1ph-divzero-4.md](../../bugs/FINDING-transformertestbench-transformerdata-i1ph-divzero-4.md) |
| Original SHA-256 | `2297990307fe5e8271f2e4d5ef686fc7671f3ae11eb93209659502a71a9b0019` |

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
model V2OMC_042bbda0b103faff
  extends Modelica.Electrical.Machines.Examples.Transformers.TransformerTestbench(transformerData.I1ph=0);
end V2OMC_042bbda0b103faff;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_042bbda0b103faff",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/TransformerData.mo:29:3-30:34:writable] Error: Trying to override final element I1ph with modifier '= 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
