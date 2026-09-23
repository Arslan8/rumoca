# FINDING-04341: `g_mFeArm.r_o` in `SimpleSolenoid`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid |
| Target | `g_mFeArm.r_o` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/BaseClasses/FixedShape.mo:37` |
| Original report | [FINDING-simplesolenoid-g-mfearm-r-o-divzero.md](../../bugs/FINDING-simplesolenoid-g-mfearm-r-o-divzero.md) |
| Original SHA-256 | `63fb36d5481faf71fa64a0e39823e871b915aaea88a4b6996d7c8196a1e8b2b3` |

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
model V2OMC_5bbc7cc5a9e8e08f
  extends Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid(g_mFeArm.r_o=0);
end V2OMC_5bbc7cc5a9e8e08f;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_5bbc7cc5a9e8e08f",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Examples/SolenoidActuator/Components/SimpleSolenoid.mo:80:11-80:20:writable] Error: Trying to override final element r_o with modifier '= 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
