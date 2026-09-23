# FINDING-00915: PI circuit has an unguarded design denominator

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | opamp-design-pi |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.PI |
| Target | k |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-pi-k-divzero-2.md](../../v2/bugs/FINDING-pi-k-divzero-2.md) — reviewed as `FINDING-00915-pi-k.md`, which a later run renamed |
| Original SHA-256 | debdbd60b57adf281e1af5355be74e0486235387fc082a4a97894576bba178cd |

## Verification and root cause

The source binding is C=T/k/R1. The reported parameter is an explicit divisor with no zero handling. At the zero witness the nominal design cannot produce finite capacitance. This declaration has a reproduced instance in the evidence; a declaration-only report is linked to that shared proof, not claimed to have its own executable model.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/PI.mo:5`. Role: `parameter`; binding: `1`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/PI.mo — source snapshot](../evidence/sources/cf132956ae22e33b-PI.mo)

```modelica
3:   extends PartialOpAmp(v2(start=0));
4:   import Modelica.Constants.pi;
5:   parameter Real k(final min=0)=1 "Desired amplification";
6:   parameter SI.Resistance R1=1000 "Resistance at negative input of OpAmp";
7:   parameter SI.Resistance R2=k*R1 "Calculated resistance to reach k";
8:   parameter SI.Time T "Time constant";
```

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/PI.mo — source snapshot](../evidence/sources/cf132956ae22e33b-PI.mo)

```modelica
4:   import Modelica.Constants.pi;
5:   parameter Real k(final min=0)=1 "Desired amplification";
6:   parameter SI.Resistance R1=1000 "Resistance at negative input of OpAmp";
7:   parameter SI.Resistance R2=k*R1 "Calculated resistance to reach k";
8:   parameter SI.Time T "Time constant";
9:   parameter SI.Capacitance C=T/k/R1 "Calculated capacitance to reach T";
10:   Basic.Resistor                            r1(R=R1)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/0777e46f4d751889.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Proposed fix

Validate the denominator parameters at OpAmpCircuits.PI, before evaluating C. Use positive domain constraints for the intended passive design and a guarded calculation plus clear assertions. If zero gain is supported, implement a dedicated zero-gain branch instead of dividing by it.

## Fix validation

Add a nominal regression and the exact boundary witness below. Require a clear domain diagnostic (or a documented finite limiting model), never NaN/Inf or an unrelated solver error. Re-run both engines.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/opamp-design-pi.md) · [Index](../README.md)
