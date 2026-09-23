# FINDING-00826: Derivative circuit has an unguarded design denominator

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | opamp-design-derivative |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.HighPass |
| Target | derivative.R1 |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-highpass-derivative-r1-divzero-2.md](../../v2/bugs/FINDING-highpass-derivative-r1-divzero-2.md) — reviewed as `FINDING-00826-highpass-derivative-r1.md`, which a later run renamed |
| Original SHA-256 | 9e854d2a165d28b35b00abfa5a314e8e13c2271964521eabbba2f15531e88665 |

## Verification and root cause

The source binding is C=T/R1. The reported parameter is an explicit divisor with no zero handling. At the zero witness the nominal design cannot produce finite capacitance. This declaration has a reproduced instance in the evidence; a declaration-only report is linked to that shared proof, not claimed to have its own executable model.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Derivative.mo:6`. Role: `parameter`; binding: `1000`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Derivative.mo — source snapshot](../evidence/sources/8eededa2a72767c5-Derivative.mo)

```modelica
4:   import Modelica.Constants.pi;
5:   parameter Real k(final min=0)=1 "Desired amplification";
6:   parameter SI.Resistance R1=1000 "Resistance at negative input of OpAmp";
7:   parameter SI.Resistance R2=k*R1 "Calculated resistance to reach k";
8:   parameter SI.Time T "Time constant";
9:   parameter SI.Capacitance C=T/R1 "Calculated capacitance to reach T";
```

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Derivative.mo — source snapshot](../evidence/sources/8eededa2a72767c5-Derivative.mo)

```modelica
4:   import Modelica.Constants.pi;
5:   parameter Real k(final min=0)=1 "Desired amplification";
6:   parameter SI.Resistance R1=1000 "Resistance at negative input of OpAmp";
7:   parameter SI.Resistance R2=k*R1 "Calculated resistance to reach k";
8:   parameter SI.Time T "Time constant";
9:   parameter SI.Capacitance C=T/R1 "Calculated capacitance to reach T";
10:   SI.Voltage v(start=0)=c.v "Capacitor voltage = state";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/c5eb5de89833fa1e.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `derivative.R1=0` | reported-failure |

Diagnostic: numeric evaluation produced a non-finite result

[Independent OpenModelica wrappers and complete output](../evidence/omc-extra-c5eb5de89833fa1e.json). Baseline: simulation succeeded.

- `derivative.R1=0` set before translation: LOG_ASSERT        | debug   | division by zero at time 0, (a=0.1591549430918953) / (b=0), where divisor b expression is: derivative.R1.
- Same value declared final, with final-parameter evaluation: LOG_ASSERT        | debug   | division by zero at time 0, (a=0.1591549430918953) / (b=0), where divisor b expression is: 0.0.

## Proposed fix

Validate the denominator parameters at OpAmpCircuits.Derivative, before evaluating C. Use positive domain constraints for the intended passive design and a guarded calculation plus clear assertions. If zero gain is supported, implement a dedicated zero-gain branch instead of dividing by it.

## Fix validation

Add a nominal regression and the exact boundary witness below. Require a clear domain diagnostic (or a documented finite limiting model), never NaN/Inf or an unrelated solver error. Re-run both engines.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/opamp-design-derivative.md) · [Index](../README.md)
