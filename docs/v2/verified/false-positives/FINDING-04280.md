# FINDING-04280: `material.H_cB` in `PermeanceActuator`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator |
| Target | `material.H_cB` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Material/HardMagnetic/BaseData.mo:19` |
| Original report | [FINDING-permeanceactuator-material-h-cb-divzero.md](../../bugs/FINDING-permeanceactuator-material-h-cb-divzero.md) |
| Original SHA-256 | `87c1efcb32bfa9e0e1c7846d2290ef93eb82a1a45696142467d03e88a6af00f1` |

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
model V2OMC_4994f6abcf7e48a5
  extends Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator(material.H_cB=0);
end V2OMC_4994f6abcf7e48a5;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_4994f6abcf7e48a5",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Material/HardMagnetic/BaseData.mo:17:3-18:59:writable] Error: Trying to override final element H_cB with modifier '= 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
