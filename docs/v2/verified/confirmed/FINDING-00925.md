# FINDING-00925: `C` in `LCOscillator`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `physical-bound-permits-zero` |
| Original tier | Candidate |
| Sanitizer result | `physical-bound-permits-zero` |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator |
| Target | `C` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/LCOscillator.mo:9` |
| Original report | [FINDING-lcoscillator-c-bound.md](../../bugs/FINDING-lcoscillator-c-bound.md) |
| Original SHA-256 | `360383453ca299c63ba76e17176375f28f6b7edc2240b3152ff55e67d234aacf` |

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
model V2OMC_d3ecbbf0da84a9c1
  extends Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator(C=0);
end V2OMC_d3ecbbf0da84a9c1;
```

Relevant OMC diagnostic:

```text
messages = "Simulation execution failed for model: V2OMC_d3ecbbf0da84a9c1
LOG_ASSERT        | debug   | division by zero at time 0, (a=-0.0009999999999998899) / (b=0), where divisor b expression is: C * R
LOG_ASSERT        | info    | simulation terminated by an assertion at initialization
```

## Original claim

The declaration carries `min=0`, and the physical role bound to this variable requires strictly greater than zero. It does **not** claim that zero is *reachable* — the bound permits it, which is a property of the declaration, not an observation of a failure.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
