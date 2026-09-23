# FINDING-04277: `g_mLeak1.l_g` in `PermeanceActuator`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator |
| Target | `g_mLeak1.l_g` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Shapes/Leakage/CoaxCylindersEndFaces.mo:20` |
| Original report | [FINDING-permeanceactuator-g-mleak1-l-g-divzero.md](../../bugs/FINDING-permeanceactuator-g-mleak1-l-g-divzero.md) |
| Original SHA-256 | `22bbf8caa1c8e4cd30a59d248dc631bf3a8d7d44b4dd0dec68d1047b35756873` |

## Why this is not a verified bug

OpenModelica rejects the report's exact source modification because the named nested element is protected, final, otherwise non-modifiable, or violates a binding rule. The report therefore does not supply a legal executable witness for its claim.

## Regression action

Keep this report as a regression: the analysis must carry modifiability/visibility through qualified component paths and must not offer an illegal parameter assignment as a witness.

## Evidence basis

Independent OpenModelica source translation of the exact witness refuted its admissibility.

## OpenModelica paired execution

- Outcome: `refuted-illegal-witness`
- Unmodified baseline: `failed`
- Source-instantiated trigger: `failed`

Generated test program:

```modelica
model V2OMC_f393af262b5e0984
  extends Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator(g_mLeak1.l_g=0);
end V2OMC_f393af262b5e0984;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_f393af262b5e0984",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Shapes/Leakage/CoaxCylindersEndFaces.mo:13:3-14:47:writable] Error: Trying to override final element l_g with modifier '= 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
