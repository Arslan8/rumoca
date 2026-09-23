# FINDING-01051: `opAmp1.Vps` in `SignalGenerator`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-zero-when-parameters-equal` |
| Original tier | Candidate |
| Sanitizer result | `divisor-zero-when-parameters-equal` |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.SignalGenerator |
| Target | `opAmp1.Vps` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Ideal/IdealizedOpAmpLimited.mo:21` |
| Original report | [FINDING-signalgenerator-opamp1-vps-divequal.md](../../bugs/FINDING-signalgenerator-opamp1-vps-divequal.md) |
| Original SHA-256 | `591e67c2a4317da454ce616ea2c4cacc6655874bf41ea257d05119524ef43f37` |

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
model V2OMC_8c230bccfa9bc9ab
  extends Modelica.Electrical.Analog.Examples.OpAmps.SignalGenerator(opAmp1.Vps=-15);
end V2OMC_8c230bccfa9bc9ab;
```

Relevant OMC diagnostic:

```text
messages = "Simulation execution failed for model: V2OMC_8c230bccfa9bc9ab
LOG_ASSERT        | debug   | division by zero at time 0, (a=0.3149999999999999) / (b=0), where divisor b expression is: opAmp1.Vps - opAmp1.Vns
LOG_ASSERT        | error   | Failed to solve the initialization problem with global homotopy with equidistant step size.
LOG_ASSERT        | debug   | Unable to solve initialization problem.
LOG_ASSERT        | info    | simulation terminated by an assertion at initialization
```

## Original claim

The denominator is a difference, so it vanishes when the two sides are equal; no `min` on either can express a constraint between two parameters. It does **not** claim that the two are equal at their declared values.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
