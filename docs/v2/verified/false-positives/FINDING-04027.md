# FINDING-04027: `adaptor.vLimConst.k` in `ChopperStepDown_RL`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperStepDown.ChopperStepDown_RL |
| Target | `adaptor.vLimConst.k` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/PowerConverters/DCDC/Control/Voltage2DutyCycle.mo:39` |
| Original report | [FINDING-chopperstepdown-rl-adaptor-vlimconst-k-divzero.md](../../bugs/FINDING-chopperstepdown-rl-adaptor-vlimconst-k-divzero.md) |
| Original SHA-256 | `cd1bede52835f75fba56fde6801d5de92db190fc67001e4c43353e4a34104d4c` |

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
model V2OMC_a1eca77bd09f091f
  extends Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperStepDown.ChopperStepDown_RL(adaptor.vLimConst.k=0);
end V2OMC_a1eca77bd09f091f;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_a1eca77bd09f091f",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/PowerConverters/DCDC/Control/Voltage2DutyCycle.mo:27:52-27:58:writable] Error: Trying to override final element k with modifier '= 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
