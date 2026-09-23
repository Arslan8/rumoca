# FINDING-04312: `g_mFePoleBot.r_i` in `AdvancedSolenoid`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid |
| Target | `g_mFePoleBot.r_i` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Shapes/FixedShape/HollowCylinderRadialFlux.mo:21` |
| Original report | [FINDING-advancedsolenoid-g-mfepolebot-r-i-divzero.md](../../bugs/FINDING-advancedsolenoid-g-mfepolebot-r-i-divzero.md) |
| Original SHA-256 | `304cb062931e850b2c432266717b096eae1ac5f907963b41f987ef0da49caca8` |

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
model V2OMC_40a72a88a5df42fd
  extends Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid(g_mFePoleBot.r_i=0);
end V2OMC_40a72a88a5df42fd;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_40a72a88a5df42fd",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Examples/SolenoidActuator/Components/AdvancedSolenoid.mo:132:11-132:20:writable] Error: Trying to override final element r_i with modifier '= 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
