# FINDING-00788: `Vps` in `Comparator`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-zero-when-parameters-equal` |
| Original tier | Candidate |
| Sanitizer result | `divisor-zero-when-parameters-equal` |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.Comparator |
| Target | `Vps` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/Comparator.mo:9` |
| Original report | [FINDING-comparator-vps-divequal.md](../../bugs/FINDING-comparator-vps-divequal.md) |
| Original SHA-256 | `0d5f075843b77446698df686c8fdadc5f7e37af3002c3a361135efcede7971ac` |

## Verification and root cause

The exact reported witness was placed in a generated Modelica subclass before translation. The unmodified model executed cleanly, while OpenModelica rejected the trigger with a numerical failure such as division by zero, a non-finite result, or a singular system.

## Proposed fix

Add a relational assertion/guard that prevents the two denominator operands from becoming equal, and test equal, reversed, and nominal values.

## Fix validation

Retest nominal values, the exact reported witness, nearby valid boundaries, and any relational equality or conditional branch involved. Preserve the intended ideal/algebraic behavior of delegated components.

## Evidence basis

Rumoca supplied the source-resolved arithmetic witness; independent OpenModelica source translation and execution reproduced the attributed failure against a clean paired baseline.

## OpenModelica paired execution

- Outcome: `confirmed-by-omc`
- Unmodified baseline: `clean`
- Source-instantiated trigger: `failed`

Generated test program:

```modelica
model V2OMC_f6b0aa5b20abdd68
  extends Modelica.Electrical.Analog.Examples.OpAmps.Comparator(Vps=-15);
end V2OMC_f6b0aa5b20abdd68;
```

Relevant OMC diagnostic:

```text
messages = "Simulation execution failed for model: V2OMC_f6b0aa5b20abdd68
LOG_ASSERT        | debug   | division by zero at time 0, (a=15) / (b=0), where divisor b expression is: Vps - Vns
LOG_ASSERT        | info    | simulation terminated by an assertion at initialization
```

## Original claim

The denominator is a difference, so it vanishes when the two sides are equal; no `min` on either can express a constraint between two parameters. It does **not** claim that the two are equal at their declared values.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
