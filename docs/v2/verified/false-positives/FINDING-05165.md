# FINDING-05165: `criticalDamping.alpha` in `Continuous`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | ModelicaTest.Blocks.Continuous |
| Target | `criticalDamping.alpha` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Blocks/Continuous.mo:1523` |
| Original report | [FINDING-continuous-criticaldamping-alpha-divzero.md](../../bugs/FINDING-continuous-criticaldamping-alpha-divzero.md) |
| Original SHA-256 | `1b198fc9d956e75e7c90d84a279117ab28f30a2f9d951f9a1a22b61e3dc76568` |

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
model V2OMC_c2f84d2ee1774f9c
  extends ModelicaTest.Blocks.Continuous(criticalDamping.alpha=0);
end V2OMC_c2f84d2ee1774f9c;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_c2f84d2ee1774f9c",
[/data/mrumoca/rumoca/target/corpus/ModelicaStandardLibrary-4.1.0/Modelica/Blocks/Continuous.mo:1521:5-1522:58:writable] Error: Protected element 'alpha' may not be modified, got 'alpha = 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
