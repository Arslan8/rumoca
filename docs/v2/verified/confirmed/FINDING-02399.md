# FINDING-02399: `smeeData.xd` in `SMEE_DOL`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-zero-when-parameters-equal` |
| Original tier | Candidate |
| Sanitizer result | `divisor-zero-when-parameters-equal` |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL |
| Target | `smeeData.xd` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/SynchronousMachineData.mo:74` |
| Original report | [FINDING-smee-dol-smeedata-xd-divequal-2.md](../../bugs/FINDING-smee-dol-smeedata-xd-divequal-2.md) |
| Original SHA-256 | `121e47273250d54941dffcda7ffe860096ce5ce151b1b458b028b2d9cffd9f8e` |

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
model V2OMC_cf40a5a6c93721aa
  extends Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL(smeeData.xd=0.13750000000000001);
end V2OMC_cf40a5a6c93721aa;
```

Relevant OMC diagnostic:

```text
messages = "Simulation execution failed for model: V2OMC_cf40a5a6c93721aa
LOG_ASSERT        | debug   | division by zero at time 0, (a=0.00140625) / (b=0), where divisor b expression is: smeeData.xd - smeeData.xdTransient
LOG_ASSERT        | info    | simulation terminated by an assertion at initialization
```

## Original claim

The denominator is a difference, so it vanishes when the two sides are equal; no `min` on either can express a constraint between two parameters. It does **not** claim that the two are equal at their declared values.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
