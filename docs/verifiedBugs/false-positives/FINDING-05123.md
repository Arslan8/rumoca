# FINDING-05123: MSL RLC wrapper delegates to zero/signed-capable primitive equations

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | msl-rlc-zero-component |
| Model | SwitchedRLC_MSL |
| Target | L |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-switchedrlc-msl-l-zerolimit.md](../../v2/bugs/FINDING-switchedrlc-msl-l-zerolimit.md) — reviewed as `FINDING-05123-switchedrlc-msl-l.md`, which a later run renamed |
| Original SHA-256 | 585d7452a05835dd883c3caaeb2ca7734762a3e2b5b6af01ce1406205aa01cc4 |

## Why this is a false positive

This local wrapper only passes L, R and C into Basic.Inductor, Basic.Resistor and Basic.Capacitor. Those source components use implicit/multiplicative equations; L and C explicitly document zero support, while R explicitly documents signed and zero support. A connected zero configuration may require retranslating states or different initialization, but the blanket physical-domain claim is not valid.

## Source evidence

Compiler/source-resolved declaration: `/data/mrumoca/rumoca/examples/models/SwitchedRLC_MSL.mo:6`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[/data/mrumoca/rumoca/examples/models/SwitchedRLC_MSL.mo — source snapshot](../evidence/sources/105ed4f74c69fe3d-SwitchedRLC_MSL.mo)

```modelica
4: 
5:   parameter Modelica.Units.SI.Voltage Vb = 24 "Battery voltage";
6:   parameter Modelica.Units.SI.Inductance L = 1;
7:   parameter Modelica.Units.SI.Resistance R = 100;
8:   parameter Modelica.Units.SI.Capacitance C = 1e-3;
9: 
```

[/data/mrumoca/rumoca/examples/models/SwitchedRLC_MSL.mo — source snapshot](../evidence/sources/105ed4f74c69fe3d-SwitchedRLC_MSL.mo)

```modelica
5:   parameter Modelica.Units.SI.Voltage Vb = 24 "Battery voltage";
6:   parameter Modelica.Units.SI.Inductance L = 1;
7:   parameter Modelica.Units.SI.Resistance R = 100;
8:   parameter Modelica.Units.SI.Capacitance C = 1e-3;
9: 
10:   Sources.StepVoltage source(
11:     V = Vb,
12:     startTime = 0.5) "Voltage steps from 0 to Vb at t=0.5 s";
13: 
14:   Basic.Inductor inductor(L = L);
15:   Basic.Resistor resistor(R = R);
16:   Basic.Capacitor capacitor(C = C);
17:   Basic.Ground ground;
18: equation
19:   connect(source.p, inductor.p);
20:   connect(inductor.n, resistor.p);
21:   connect(inductor.n, capacitor.p);
22:   connect(resistor.n, ground.p);
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/59f54dc4129c2dd4.json). Baseline: **clean**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/msl-rlc-zero-component.md) · [Index](../README.md)
