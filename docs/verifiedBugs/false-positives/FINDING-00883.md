# FINDING-00883: Zero feedback resistance is the unity-gain buffer

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | unity-buffer |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Buffer |
| Target | R2 |
| Student classification | physical-invariant-violated |
| Original report | [FINDING-buffer-r2-zerolimit.md](../../v2/bugs/FINDING-buffer-r2-zerolimit.md) — reviewed as `FINDING-00883-buffer-r2.md`, which a later run renamed |
| Original SHA-256 | 22e8435f392d6886c5b20e843f6782c5e1ae488790cbdfb5211abf5aaebf0db3 |

## Why this is a false positive

R2=(k-1)*R1 deliberately gives zero at the default k=1. R2 feeds a Basic.Resistor, whose documented domain includes zero, and there is no reciprocal R2 in this buffer. Rejecting the nominal unity-gain configuration is a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Buffer.mo:6`. Role: `parameter`; binding: `0`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Buffer.mo — source snapshot](../evidence/sources/88331c0e33cc6eb3-Buffer.mo)

```modelica
4:   parameter Real k(final min=0)=1 "Desired amplification";
5:   parameter SI.Resistance R1=1000 "Resistance at negative pin(s)";
6:   parameter SI.Resistance R2=(k - 1)*R1 "Calculated resistance to reach desired amplification k";
7:   Basic.Resistor                            r1(final R=R1)
8:     annotation (Placement(transformation(extent={{-10,-10},{10,10}},
9:         rotation=270,
```

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Buffer.mo — source snapshot](../evidence/sources/88331c0e33cc6eb3-Buffer.mo)

```modelica
4:   parameter Real k(final min=0)=1 "Desired amplification";
5:   parameter SI.Resistance R1=1000 "Resistance at negative pin(s)";
6:   parameter SI.Resistance R2=(k - 1)*R1 "Calculated resistance to reach desired amplification k";
7:   Basic.Resistor                            r1(final R=R1)
8:     annotation (Placement(transformation(extent={{-10,-10},{10,10}},
9:         rotation=270,
10:         origin={10,-70})));
11:   Basic.Resistor                            r2(final R=R2)
12:     annotation (Placement(transformation(extent={{10,-10},{-10,10}},
13:         rotation=90,
14:         origin={10,-30})));
```

[Electrical/Analog/Basic/Resistor.mo — source snapshot](../evidence/sources/f3257fcb99588782-Resistor.mo)

```modelica
14: equation
15:   assert((1 + alpha*(T_heatPort - T_ref)) >= Modelica.Constants.eps,
16:     "Temperature outside scope of model!");
17:   R_actual = R*(1 + alpha*(T_heatPort - T_ref));
18:   v = R_actual*i;
19:   LossPower = v*i;
20:   annotation (
21:     Documentation(info="<html>
22: <p>The linear resistor connects the branch voltage <em>v</em> with the branch current <em>i</em> by <em>i*R = v</em>. The Resistance <em>R</em> is allowed to be positive, zero, or negative.</p>
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/16ddacbc190cee1d.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/unity-buffer.md) · [Index](../README.md)
