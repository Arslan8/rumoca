# FINDING-04893: Zero core-loss conductance deliberately disables losses

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | disabled-core-loss |
| Model | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses |
| Target | smpmData.statorCoreParameters.GcRef |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-voltagesourcewithlosses-smpmdata-statorcoreparameters-gcref-zerol.md](../../v2/bugs/FINDING-smpm-voltagesourcewithlosses-smpmdata-statorcoreparameters-gcref-zerol.md) — reviewed as `FINDING-04893-smpm-voltagesourcewithlosses-smpmdata-statorcoreparameters-gcref.md`, which a later run renamed |
| Original SHA-256 | cb8af42422f0725849361da707db67e15cfd75e03f2d5253e9434fc53cf43a31 |

## Why this is a false positive

GcRef is final and explicitly equals zero when PRef<=0; the default PRef is zero. Both DC and induction-machine Core consumers handle this branch by setting core-loss currents to zero. The reported default-value invariant violation is intended lossless behavior, not a failure.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Losses/CoreParameters.mo:18`. Role: `parameter`; binding: `(if (smpmData.statorCoreParameters.PRef <= 0) then 0 else ((smpmData.statorCoreParameters.PRef / (smpmData.statorCoreParameters.VRef ^ 2)) / smpmData.statorCoreParameters.m))`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Losses/CoreParameters.mo — source snapshot](../evidence/sources/4e22ebe6537d7ba8-CoreParameters.mo)

```modelica
16:     start=0.775) = 0
17:     "Ratio of hysteresis losses with respect to the total core losses at VRef and fRef";
18:   final parameter SI.Conductance GcRef=if (PRef <= 0) then 0
19:        else PRef/VRef^2/m
20:     "Reference conductance at reference frequency and voltage";
21:   final parameter SI.AngularVelocity wMin=1e-6*wRef "Angular velocity limit";
```

[Electrical/Machines/Losses/CoreParameters.mo — source snapshot](../evidence/sources/4e22ebe6537d7ba8-CoreParameters.mo)

```modelica
6:   parameter SI.Power PRef(min=0) = 0
7:     "Reference core losses at reference inner voltage VRef";
8:   parameter SI.Voltage VRef(min=Modelica.Constants.small)
9:     "Reference inner RMS voltage that reference core losses PRef refer to";
10:   parameter SI.AngularVelocity wRef(min=Modelica.Constants.small)
11:     "Reference angular velocity that reference core losses PRef refer to";
12:   // In the current implementation ratioHysterisis = 0 since hysteresis losses are not implemented yet
13:   final parameter Real ratioHysteresis(
14:     min=0,
15:     max=1,
16:     start=0.775) = 0
17:     "Ratio of hysteresis losses with respect to the total core losses at VRef and fRef";
18:   final parameter SI.Conductance GcRef=if (PRef <= 0) then 0
19:        else PRef/VRef^2/m
20:     "Reference conductance at reference frequency and voltage";
```

[Electrical/Machines/Losses/DCMachines/Core.mo — source snapshot](../evidence/sources/7a13299a0773d848-Core.mo)

```modelica
16:   if (coreParameters.PRef <= 0) then
17:     Gc = 0;
18:     i = 0;
19:   else
20:     Gc = coreParameters.GcRef;
21:     // * (coreParameters.wRef/wLimit*coreParameters.ratioHysteresis + 1 - coreParameters.ratioHysteresis);
22:     i = Gc*v;
23:   end if;
```

[Electrical/Machines/Losses/InductionMachines/Core.mo — source snapshot](../evidence/sources/f2069b6894c33128-Core.mo)

```modelica
23:     Gc = 0;
24:     spacePhasor.i_ = zeros(2);
25:   else
26:     Gc = coreParameters.GcRef;
27:     //  * (coreParameters.wRef/wLimit*coreParameters.ratioHysteresis + 1 - coreParameters.ratioHysteresis);
28:     spacePhasor.i_ = Gc*spacePhasor.v_;
29:   end if;
30:   lossPower = 3/2*(+spacePhasor.v_[1]*spacePhasor.i_[1] + spacePhasor.v_[2]*spacePhasor.i_[2]);
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f5cf46ada0ef7a80.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/disabled-core-loss.md) · [Index](../README.md)
