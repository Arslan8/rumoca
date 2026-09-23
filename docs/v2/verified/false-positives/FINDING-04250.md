# FINDING-04250: `pmActuator.material.H_cB` in `ArmatureStroke`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke |
| Target | `pmActuator.material.H_cB` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Material/HardMagnetic/BaseData.mo:19` |
| Original report | [FINDING-armaturestroke-pmactuator-material-h-cb-divzero.md](../../bugs/FINDING-armaturestroke-pmactuator-material-h-cb-divzero.md) |
| Original SHA-256 | `78185d57b05d77a1300e7d5179dc708c68c97da8d348e2a329ce957aab40be34` |

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
model V2OMC_72b5ce105755c84a
  extends Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke(pmActuator.material.H_cB=0);
end V2OMC_72b5ce105755c84a;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_72b5ce105755c84a",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Material/HardMagnetic/BaseData.mo:17:3-18:59:writable] Error: Trying to override final element H_cB with modifier '= 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
