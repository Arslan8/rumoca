# FINDING-05182: `transferFunction.a_end` in `Continuous_InitialState`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | ModelicaTest.Blocks.Continuous_InitialState |
| Target | `transferFunction.a_end` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Blocks/Continuous.mo:1167` |
| Original report | [FINDING-continuous-initialstate-transferfunction-a-end-divzero-2.md](../../bugs/FINDING-continuous-initialstate-transferfunction-a-end-divzero-2.md) |
| Original SHA-256 | `5555b076ce3ae22cdf482d069b3d782c9a7e6a313649ac574b11e02d944d70df` |

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
model V2OMC_9f573be6076bdf71
  extends ModelicaTest.Blocks.Continuous_InitialState(transferFunction.a_end=0);
end V2OMC_9f573be6076bdf71;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_9f573be6076bdf71",
[/data/mrumoca/rumoca/target/corpus/ModelicaStandardLibrary-4.1.0/Modelica/Blocks/Continuous.mo:1147:5-1147:97:writable] Error: Protected element 'a_end' may not be modified, got 'a_end = 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
