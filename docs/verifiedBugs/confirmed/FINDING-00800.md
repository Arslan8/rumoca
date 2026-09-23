# FINDING-00800: Control-circuit time constants create zero divisions

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | control-design |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit |
| Target | T2 |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-00800-controlcircuit-t2.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 1a29013cde32a680cba597687d17894926fb45df647b587dcafab04ff0d8bb3b |

## Verification and root cause

kp=T2/(2*T1), Ti=T2 and PIA.C=Ti/kp/PIA.R1. T1=0 directly divides by zero; T2=0 sets both Ti and kp to zero and yields 0/0 in PIA.C. These are explicit design formulas, not just solver-selected state divisions. Both triggers fail after clean baselines.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/ControlCircuit.mo:5`. Role: `parameter`; binding: `0.01`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/ControlCircuit.mo — source snapshot](../evidence/sources/2006c2afcee8deb4-ControlCircuit.mo)

```modelica
3:   extends Modelica.Icons.Example;
4:   parameter SI.Time T1=0.01 "Small time constant";
5:   parameter SI.Time T2=0.01 "Large time constant";
6:   parameter SI.Time Ti=T2 "Integral time constant";
7:   parameter Real kp=T2/(2*T1) "Proportional gain";
8:   Modelica.Electrical.Analog.Basic.Ground ground
```

[Electrical/Analog/Examples/OpAmps/ControlCircuit.mo — source snapshot](../evidence/sources/2006c2afcee8deb4-ControlCircuit.mo)

```modelica
4:   parameter SI.Time T1=0.01 "Small time constant";
5:   parameter SI.Time T2=0.01 "Large time constant";
6:   parameter SI.Time Ti=T2 "Integral time constant";
7:   parameter Real kp=T2/(2*T1) "Proportional gain";
```

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/PI.mo — source snapshot](../evidence/sources/cf132956ae22e33b-PI.mo)

```modelica
5:   parameter Real k(final min=0)=1 "Desired amplification";
6:   parameter SI.Resistance R1=1000 "Resistance at negative input of OpAmp";
7:   parameter SI.Resistance R2=k*R1 "Calculated resistance to reach k";
8:   parameter SI.Time T "Time constant";
9:   parameter SI.Capacitance C=T/k/R1 "Calculated capacitance to reach T";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/38386543da2fe8c7.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `T2=0` | reported-failure |

Diagnostic: numeric evaluation produced a non-finite result

[Independent OpenModelica wrappers and complete output](../evidence/omc-extra-38386543da2fe8c7.json). Baseline: simulation succeeded.

- `T2=0` set before translation: LOG_ASSERT        | debug   | division by zero at time 0, (a=0) / (b=0), where divisor b expression is: PIA.R1 * PIA.k.
- Same value declared final, with final-parameter evaluation: LOG_ASSERT        | debug   | division by zero at time 0, (a=0) / (b=0), where divisor b expression is: 0.0.

## Proposed fix

Validate T1>0 and T2>0 at ControlCircuit; use guarded design formulas so invalid input reports the time-constant constraint before parameter evaluation produces NaN/Inf. Keep the analog/block comparison consistent.

## Fix validation

Add a nominal regression and the exact boundary witness below. Require a clear domain diagnostic (or a documented finite limiting model), never NaN/Inf or an unrelated solver error. Re-run both engines.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/control-design.md) · [Index](../README.md)
