# FINDING-04844: FirstOrder divides by an unconstrained zero time constant

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | first-order-time-constant |
| Model | ModelicaTest.Blocks.LimPID |
| Target | firstOrder1.T |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-limpid-firstorder1-t-divzero.md](../../v2/bugs/FINDING-limpid-firstorder1-t-divzero.md) — reviewed as `FINDING-04844-limpid-firstorder1-t.md`, which a later run renamed |
| Original SHA-256 | 22e2b7caa13332fe03552b93fdb8b3aa39dde2263851e1fa3499a62bc13665fa |

## Verification and root cause

Blocks.Continuous.FirstOrder declares T without a positive bound and evaluates der(y)=(k*u-y)/T. T=0 is admitted by the declaration and makes that equation undefined, even though the transfer-function limit at T=0 is the algebraic gain y=k*u. The shared source defect is established independently of nominal models the current runtime cannot execute.

## Source evidence

Compiler/source-resolved declaration: `Blocks/Continuous.mo:354`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
352:     import Modelica.Blocks.Types.Init;
353:     parameter Real k=1 "Gain";
354:     parameter SI.Time T(start=1) "Time Constant";
355:     parameter Init initType=Init.NoInit
356:       "Type of initialization (1: no init, 2: steady state, 3/4: initial output)" annotation(Evaluate=true,
357:         Dialog(group="Initialization"));
```

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
348:       textString="k=%k")}));
349:   end Derivative;
350: 
351:   block FirstOrder "First order transfer function block (= 1 pole)"
352:     import Modelica.Blocks.Types.Init;
353:     parameter Real k=1 "Gain";
354:     parameter SI.Time T(start=1) "Time Constant";
355:     parameter Init initType=Init.NoInit
356:       "Type of initialization (1: no init, 2: steady state, 3/4: initial output)" annotation(Evaluate=true,
357:         Dialog(group="Initialization"));
358:     parameter Real y_start=0 "Initial or guess value of output (= state)"
359:       annotation (Dialog(group="Initialization"));
360: 
361:     extends Interfaces.SISO(y(start=y_start));
362: 
363:   initial equation
364:     if initType == Init.SteadyState then
365:       der(y) = 0;
366:     elseif initType == Init.InitialState or initType == Init.InitialOutput then
367:       y = y_start;
368:     end if;
369:   equation
370:     der(y) = (k*u - y)/T;
371:     annotation (
372:       Documentation(info="<html>
373: <p>
374: This blocks defines the transfer function between the input u
375: and the output y as <em>first order</em> system:
376: </p>
377: <blockquote><pre>
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/0340928397dc64cd.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Proposed fix

Choose and document the contract. To support the natural zero-time-constant limit, formulate T*der(y)=k*u-y and handle state/initialization selection structurally. Otherwise require T>0 with a meaningful lower bound and an assertion evaluated before division. Do not silently replace zero by epsilon.

## Fix validation

Test T>0 dynamics, T=0 algebraic feedthrough, fixed-output initialization, and parameter changes if tunability is supported. Invalid negative T should follow the documented policy.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/first-order-time-constant.md) · [Index](../README.md)
