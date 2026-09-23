# FINDING-00990: `opAmp.Vps` in `Derivative`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-zero-when-parameters-equal` |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Derivative |
| Target | `opAmp.Vps` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Ideal/IdealizedOpAmpLimited.mo:21` |
| Original report | [FINDING-derivative-opamp-vps-divequal.md](../../bugs/FINDING-derivative-opamp-vps-divequal.md) |
| Original SHA-256 | `7a78b482ab4cf7fb0c6707eccdb56f1678cb6eef0a059c2f5d5308528a48a342` |

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
model V2OMC_68fb5a5dee336cf4
  extends Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Derivative(opAmp.Vps=-15);
end V2OMC_68fb5a5dee336cf4;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_68fb5a5dee336cf4",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/OpAmpCircuits/PartialOpAmp.mo:11:11-11:18:writable] Error: Trying to override final element Vps with modifier '= -15'.
```

## Original claim

The denominator is a difference, so it vanishes when the two sides are equal; no `min` on either can express a constraint between two parameters. It does **not** claim that the two are equal at their declared values.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
