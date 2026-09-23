# FINDING-00814: Der circuit has an unguarded design denominator

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | opamp-design-der |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.Differentiator |
| Target | der_.R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-differentiator-der-r-unbounded.md](../../v2/bugs/FINDING-differentiator-der-r-unbounded.md) — reviewed as `FINDING-00814-differentiator-der-r.md`, which a later run renamed |
| Original SHA-256 | c5ade8bd3c9826dac2d84f02f05b03d5fb7569a432b2a7101beb5d40ff56f2e7 |

## Verification and root cause

The source binding is C=k/(2*pi*f*R). The reported parameter is an explicit divisor with no zero handling. At the zero witness the nominal design cannot produce finite capacitance. This declaration has a reproduced instance in the evidence; a declaration-only report is linked to that shared proof, not claimed to have its own executable model.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Der.mo:7`. Role: `parameter`; binding: `1000`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Der.mo — source snapshot](../evidence/sources/0db365a039713113-Der.mo)

```modelica
5:   parameter Real k(final min=0)=1 "Desired amplification at frequency f";
6:   parameter SI.Frequency f "Frequency";
7:   parameter SI.Resistance R=1000 "Resistance at output of OpAmp";
8:   parameter SI.Capacitance C=k/(2*pi*f*R) "Calculated capacitance to reach desired amplification k";
9:   SI.Voltage v(start=0)=c.v "Capacitor voltage = state";
10:   Basic.Capacitor                            c(final C=C)
```

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Der.mo — source snapshot](../evidence/sources/0db365a039713113-Der.mo)

```modelica
4:   import Modelica.Constants.pi;
5:   parameter Real k(final min=0)=1 "Desired amplification at frequency f";
6:   parameter SI.Frequency f "Frequency";
7:   parameter SI.Resistance R=1000 "Resistance at output of OpAmp";
8:   parameter SI.Capacitance C=k/(2*pi*f*R) "Calculated capacitance to reach desired amplification k";
9:   SI.Voltage v(start=0)=c.v "Capacitor voltage = state";
10:   Basic.Capacitor                            c(final C=C)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/9fb3c0f95a3c9b11.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `der_.R=0` | reported-failure |

Diagnostic: numeric evaluation produced a non-finite result

[Independent OpenModelica wrappers and complete output](../evidence/omc-extra-9fb3c0f95a3c9b11.json). Baseline: simulation succeeded.

- `der_.R=0` set before translation: LOG_ASSERT        | debug   | division by zero at time 0, (a=0.3183098861837907) / (b=0), where divisor b expression is: 0.0.
- Same value declared final, with final-parameter evaluation: LOG_ASSERT        | debug   | division by zero at time 0, (a=0.3183098861837907) / (b=0), where divisor b expression is: 0.0.

## Proposed fix

Validate the denominator parameters at OpAmpCircuits.Der, before evaluating C. Use positive domain constraints for the intended passive design and a guarded calculation plus clear assertions. If zero gain is supported, implement a dedicated zero-gain branch instead of dividing by it.

## Fix validation

Add a nominal regression and the exact boundary witness below. Require a clear domain diagnostic (or a documented finite limiting model), never NaN/Inf or an unrelated solver error. Re-run both engines.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/opamp-design-der.md) · [Index](../README.md)
