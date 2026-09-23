# FINDING-00018: CriticalDamping accepts zero order then divides by it

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | critical-damping-order |
| Model | Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.MixingUnitWithContinuousControl |
| Target | filter.n |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-mixingunitwithcontinuouscontrol-filter-n-divunresolved-2.md](../../v2/bugs/FINDING-mixingunitwithcontinuouscontrol-filter-n-divunresolved-2.md) — reviewed as `FINDING-00018-mixingunitwithcontinuouscontrol-filter-n.md`, which a later run renamed |
| Original SHA-256 | 6ef17c423adcc0984c3a3af5a5e5b9e9ce5ebf66bbf763f4e1fc42769fbd3fc7 |

## Verification and root cause

CriticalDamping declares Integer n=2 without min=1. It computes alpha=sqrt(2^(1/n)-1), allocates x[n], and indexes x[1] and x[n]. n=0 therefore causes division/index/domain failures. Filter order is structurally required to be at least one.

## Source evidence

Compiler/source-resolved declaration: `Blocks/Continuous.mo:1504`. Role: `parameter`; binding: `3`; effective min: `None`; effective max: `None`. 

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
1502:     extends Modelica.Blocks.Interfaces.SISO;
1503: 
1504:     parameter Integer n=2 "Order of filter";
1505:     parameter SI.Frequency f(start=1) "Cut-off frequency";
1506:     parameter Boolean normalized = true
1507:       "= true, if amplitude at f_cut is 3 dB, otherwise unmodified filter";
```

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
1498:   block CriticalDamping
1499:     "Output the input signal filtered with an n-th order filter with critical damping"
1500: 
1501:     import Modelica.Blocks.Types.Init;
1502:     extends Modelica.Blocks.Interfaces.SISO;
1503: 
1504:     parameter Integer n=2 "Order of filter";
1505:     parameter SI.Frequency f(start=1) "Cut-off frequency";
1506:     parameter Boolean normalized = true
1507:       "= true, if amplitude at f_cut is 3 dB, otherwise unmodified filter";
1508:     parameter Modelica.Blocks.Types.Init initType=Modelica.Blocks.Types.Init.NoInit
1509:       "Type of initialization (1: no init, 2: steady state, 3: initial state, 4: initial output)"
1510:                                                                                       annotation(Evaluate=true,
1511:         Dialog(group="Initialization"));
1512:     parameter Real x_start[n]=zeros(n) "Initial or guess values of states"
1513:       annotation (Dialog(group="Initialization"));
1514:     parameter Real y_start=0.0
1515:       "Initial value of output (remaining states are in steady state)"
1516:       annotation(Dialog(enable=initType == Init.InitialOutput, group=
1517:             "Initialization"));
1518: 
1519:     output Real x[n](start=x_start) "Filter states";
1520:   protected
1521:     parameter Real alpha=if normalized then sqrt(2^(1/n) - 1) else 1.0
1522:       "Frequency correction factor for normalized filter";
1523:     parameter Real w=2*Modelica.Constants.pi*f/alpha;
1524:   initial equation
```

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
1530:       y = y_start;
1531:       der(x[1:n-1]) = zeros(n-1);
1532:     end if;
1533:   equation
1534:     der(x[1]) = (u - x[1])*w;
1535:     for i in 2:n loop
1536:       der(x[i]) = (x[i - 1] - x[i])*w;
1537:     end for;
1538:     y = x[n];
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4a214d5a5475e994.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Proposed fix

Declare n(min=1)=2 and retain an explicit assertion for tools that do not enforce parameter bounds before structural evaluation. Ensure array dimensions and alpha are never evaluated for invalid n.

## Fix validation

Test n=1, n=2, larger orders, and n=0/negative with a deterministic order-domain diagnostic before array indexing or division.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/critical-damping-order.md) · [Index](../README.md)
