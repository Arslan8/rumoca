# FINDING-00781: Equal op-amp supplies divide by zero

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | opamp-supply-span |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.Comparator |
| Target | Vps |
| Student classification | divisor-zero-when-parameters-equal |
| Original report | [FINDING-comparator-vps-divequal-2.md](../../v2/bugs/FINDING-comparator-vps-divequal-2.md) — reviewed as `FINDING-00781-comparator-vps.md`, which a later run renamed |
| Original SHA-256 | 68ed515882f6cfcd93efc2325c4894d81ce6c74237d57117cc0c239afe4382d0 |

## Verification and root cause

The source defines i_s = p_s/(vps-vns) with no nonzero-span assertion. In LCOscillator and Comparator, Vns=-15; setting Vps=-15 makes the denominator exactly zero. The correct equality witness is -15, not Vps=0. Both nominal examples pass; the actual equality fails in Rumoca and in ordinary and final-evaluated OpenModelica models.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/Comparator.mo:4`. Role: `parameter`; binding: `15`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/Comparator.mo — source snapshot](../evidence/sources/c3b4a9d44d7708f1-Comparator.mo)

```modelica
2: model Comparator "Comparator"
3:   extends Modelica.Icons.Example;
4:   parameter SI.Voltage Vps=+15 "Positive supply";
5:   parameter SI.Voltage Vns=-15 "Negative supply";
6:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
7:   parameter SI.Frequency f=10 "Frequency of input voltage";
```

[Electrical/Analog/Ideal/IdealizedOpAmpLimited.mo — source snapshot](../evidence/sources/82553ac7b2285238-IdealizedOpAmpLimited.mo)

```modelica
21:   SI.Current i_s=p_s/(vps - vns) "Supply current";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/7def794e383a0da2.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `Vps=-15` | reported-failure |

Diagnostic: numeric evaluation produced a non-finite result

[Independent OpenModelica wrappers and complete output](../evidence/omc-extra-7def794e383a0da2.json). Baseline: simulation succeeded.

- `Vps=-15` set before translation: LOG_ASSERT        | debug   | division by zero at time 0, (a=15) / (b=0), where divisor b expression is: 0.0.
- Same value declared final, with final-parameter evaluation: LOG_ASSERT        | debug   | division by zero at time 0, (a=15) / (b=0), where divisor b expression is: 0.0.

## Proposed fix

In IdealizedOpAmpLimited validate vps > vns (including useSupply=true pins), and make the zero-span behavior explicit. Do not divide before validation; use a guarded expression plus a domain assertion. If collapsed supplies are to be supported, specify and implement their power/current behavior rather than substituting an epsilon.

## Fix validation

Test unequal nominal supplies, both equal-supply values, reversed rails, and dynamic supply pins crossing equality. Preserve normal clipping and power accounting.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/opamp-supply-span.md) · [Index](../README.md)
