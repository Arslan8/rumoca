# FINDING-02243: Equal machine reactances divide by zero

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | machine-reactance-equality |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator |
| Target | smeeData.xdTransient |
| Student classification | divisor-zero-when-parameters-equal |
| Original report | [FINDING-smee-generator-smeedata-xdtransient-divequal-2.md](../../v2/bugs/FINDING-smee-generator-smeedata-xdtransient-divequal-2.md) — reviewed as `FINDING-02243-smee-generator-smeedata-xdtransient.md`, which a later run renamed |
| Original SHA-256 | 1eb0a7180e59c32312f6557279f914329209b8193be04d10a977e857adf251be |

## Verification and root cause

The record defines xe=xmd^2/(xd-xdTransient), xrd with /(xdTransient-xdSubtransient), and xrq=xmq^2/(xq-xqSubtransient), without relational assertions. The equality in this report zeros the corresponding denominator. A minimal model using the actual library record tests the nominal data and all three equalities independently; the full reported machine cannot be simulated by the current Rumoca bitcode runtime. Verification is of the shared declaration, not a claim that the full machine was independently run.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/SynchronousMachineData.mo:29`. Role: `parameter`; binding: `0.1375`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/SynchronousMachineData.mo — source snapshot](../evidence/sources/16b4341f9d5ec816-SynchronousMachineData.mo)

```modelica
27:   parameter Real xq(start=1.6)
28:     "Synchronous reactance per phase, q-axis [pu]";
29:   parameter Real xdTransient(start=0.1375)
30:     "Transient reactance per phase, d-axis [pu]";
31:   parameter Real xdSubtransient(start=0.121428571)
32:     "Subtransient reactance per phase, d-axis [pu]";
```

[Electrical/Machines/Utilities/SynchronousMachineData.mo — source snapshot](../evidence/sources/16b4341f9d5ec816-SynchronousMachineData.mo)

```modelica
23:   parameter Real x0(start=0.1)
24:     "Stator stray inductance per phase (approximately zero impedance) [pu]";
25:   parameter Real xd(start=1.6)
26:     "Synchronous reactance per phase, d-axis [pu]";
27:   parameter Real xq(start=1.6)
28:     "Synchronous reactance per phase, q-axis [pu]";
29:   parameter Real xdTransient(start=0.1375)
30:     "Transient reactance per phase, d-axis [pu]";
31:   parameter Real xdSubtransient(start=0.121428571)
32:     "Subtransient reactance per phase, d-axis [pu]";
33:   parameter Real xqSubtransient(start=0.148387097)
34:     "Subtransient reactance per phase, q-axis [pu]";
```

[Electrical/Machines/Utilities/SynchronousMachineData.mo — source snapshot](../evidence/sources/16b4341f9d5ec816-SynchronousMachineData.mo)

```modelica
70:   final parameter Real xmd=xd - x0
71:     "Main field reactance per phase, d-axis [pu]";
72:   final parameter Real xmq=xq - x0
73:     "Main field reactance per phase, q-axis [pu]";
74:   final parameter Real xe=xmd^2/(xd - xdTransient)
75:     "Excitation reactance [pu]";
76:   final parameter Real xrd=xmd^2/(xdTransient - xdSubtransient)*(1 - (xmd/
77:       xe))^2 + xmd^2/xe "Damper reactance per phase, d-axis [pu]";
78:   final parameter Real xrq=xmq^2/(xq - xqSubtransient)
79:     "Damper reactance per phase, d-axis [pu]";
80:   final parameter Real rs=2/(1/xdSubtransient + 1/xqSubtransient)/(omega*Ta)
81:     "Stator resistance per phase at specification temperature [pu]";
82:   final parameter Real rrd=(xrd - xmd^2/xe)/(omega*Td0Subtransient)
83:     "Damper resistance per phase at specification temperature, d-axis [pu]";
84:   final parameter Real rrq=xrq/(omega*Tq0Subtransient)
85:     "Damper resistance per phase at specification temperature, q-axis [pu]";
86:   final parameter Real re=xe/(omega*Td0Transient)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4d376a5cb19be7de.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

[Independent controls and actual library-record projections](../evidence/control-initialization.json) include source wrappers, compiler options, and full results.

## Proposed fix

Validate xd>xdTransient>xdSubtransient and xq>xqSubtransient in the data-conversion layer (or explicitly define any supported degenerate machine representation). Guard parameter calculations and use a checked helper function with assertions, since record bindings may be evaluated before model initial equations.

## Fix validation

The nominal record projection must run; each equality must yield a clear relational-domain diagnostic rather than NaN/Inf. Also test reversed ordering and near-equal well-conditioned input.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/machine-reactance-equality.md) · [Index](../README.md)
