# FINDING-04343: `g_mAirWork.A` in `SimpleSolenoid`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid |
| Target | `g_mAirWork.A` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Shapes/Force/HollowCylinderAxialFlux.mo:24` |
| Original report | [FINDING-simplesolenoid-g-mairwork-a-divzero.md](../../bugs/FINDING-simplesolenoid-g-mairwork-a-divzero.md) |
| Original SHA-256 | `7227908b5e384e7684e1c4c397604d09450fb8617af813664f4548654edbfa7a` |

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
model V2OMC_97bc6cb68b8ab15d
  extends Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid(g_mAirWork.A=0);
end V2OMC_97bc6cb68b8ab15d;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_97bc6cb68b8ab15d",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Shapes/Force/HollowCylinderAxialFlux.mo:16:3-17:59:writable] Error: Protected element 'A' may not be modified, got 'A = 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
