# FINDING-04273: `g_ma.r_i` in `PermeanceActuator`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator |
| Target | `g_ma.r_i` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Shapes/Force/HollowCylinderRadialFlux.mo:21` |
| Original report | [FINDING-permeanceactuator-g-ma-r-i-divzero.md](../../bugs/FINDING-permeanceactuator-g-ma-r-i-divzero.md) |
| Original SHA-256 | `3572d3850593a7b7764bf651f30e8e1ecbf935b6a2af8ed1e61257ce9e85258f` |

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
model V2OMC_c4ec955b097234e1
  extends Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator(g_ma.r_i=0);
end V2OMC_c4ec955b097234e1;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_c4ec955b097234e1",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/PermeanceActuator.mo:83:11-83:21:writable] Error: Trying to override final element r_i with modifier '= 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
