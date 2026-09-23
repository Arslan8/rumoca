# FINDING-00019: normalized=false selects a safe explicit branch

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | critical-damping-boolean |
| Model | Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.MixingUnitWithContinuousControl |
| Target | filter.normalized |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-00019-mixingunitwithcontinuouscontrol-filter-normalized.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 6fa7d39a73656dc0983e6c2d02bc9091892bf3bf8312f5b6b3ee65d6d8f4c93a |

## Why this is a false positive

normalized is Boolean, not a numeric divisor. The binding is alpha=if normalized then sqrt(2^(1/n)-1) else 1.0. Setting it false makes alpha exactly one, so the later division by alpha remains safe. The detector confused branch control with denominator data.

## Source evidence

Compiler/source-resolved declaration: `Blocks/Continuous.mo:1506`. Role: `parameter`; binding: `False`; effective min: `None`; effective max: `None`. 

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
1504:     parameter Integer n=2 "Order of filter";
1505:     parameter SI.Frequency f(start=1) "Cut-off frequency";
1506:     parameter Boolean normalized = true
1507:       "= true, if amplitude at f_cut is 3 dB, otherwise unmodified filter";
1508:     parameter Modelica.Blocks.Types.Init initType=Modelica.Blocks.Types.Init.NoInit
1509:       "Type of initialization (1: no init, 2: steady state, 3: initial state, 4: initial output)"
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


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4a214d5a5475e994.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/critical-damping-boolean.md) · [Index](../README.md)
