# FINDING-04245: `pmActuator.g_mb.r_i` in `ArmatureStroke`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke |
| Target | `pmActuator.g_mb.r_i` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Shapes/Force/HollowCylinderRadialFlux.mo:23` |
| Original report | [FINDING-armaturestroke-pmactuator-g-mb-r-i-divzero-2.md](../../bugs/FINDING-armaturestroke-pmactuator-g-mb-r-i-divzero-2.md) |
| Original SHA-256 | `07e322d6e206803734468a7d29c225e64b62d8bacb2f344a2a1408f8ca1d2da2` |

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
model V2OMC_bc4243be77581e0c
  extends Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke(pmActuator.g_mb.r_i=0);
end V2OMC_bc4243be77581e0c;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_bc4243be77581e0c",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/PermeanceActuator.mo:91:11-91:21:writable] Error: Trying to override final element r_i with modifier '= 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
