# FINDING-00955: `R2` in `Multivibrator`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `physical-domain-unenforced` |
| Original tier | Candidate |
| Sanitizer result | `physical-domain-unenforced` |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator |
| Target | `R2` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/Multivibrator.mo:8` |
| Original report | [FINDING-multivibrator-r2-unbounded.md](../../bugs/FINDING-multivibrator-r2-unbounded.md) |
| Original SHA-256 | `168f35366970850b1bbd276c1c25de66d76bf3171e2cafc9023a6d6c94630620` |

## Verification and root cause

The reviewed component-specific physical contract excludes the reported value. With the exact zero or negative witness encoded before translation, the unmodified model ran cleanly and OpenModelica reproduced a numerical failure.

## Proposed fix

Tighten the declaration or its component-scoped type to the reviewed domain, retain any supported ideal limit explicitly, and add this generated witness as a boundary regression.

## Fix validation

Retest nominal values, the exact reported witness, nearby valid boundaries, and any relational equality or conditional branch involved. Preserve the intended ideal/algebraic behavior of delegated components.

## Evidence basis

Source-semantic contract review plus independent OpenModelica paired execution.

## OpenModelica paired execution

- Outcome: `witness-causes-omc-numerical-failure`
- Unmodified baseline: `clean`
- Source-instantiated trigger: `failed`

Generated test program:

```modelica
model V2OMC_b1af837395b7ee56
  extends Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator(R2=-1);
end V2OMC_b1af837395b7ee56;
```

Relevant OMC diagnostic:

```text
messages = "Simulation execution failed for model: V2OMC_b1af837395b7ee56
LOG_ASSERT        | warning | The following assertion has been violated at time 0.000000
LOG_ASSERT        | debug   | Model error: Argument of log(1.0 + 2.0 * R1 / R2) was -1999 should be > 0
LOG_ASSERT        | info    | simulation terminated by an assertion at initialization
```

## Original claim

Nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones. It does **not** claim that any model actually sets such a value.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
