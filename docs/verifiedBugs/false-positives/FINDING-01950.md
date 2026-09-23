# FINDING-01950: Arc-switch resistance/conductance are multiplicative ideal limits

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | ideal-arc-switch-zero |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc |
| Target | switchYDwithArc.idealCloser.closerWithArc[1].Goff |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-ydarc-switchydwitharc-idealcloser-closerwitharc-1-goff-zerolimit.md](../../v2/bugs/FINDING-imc-ydarc-switchydwitharc-idealcloser-closerwitharc-1-goff-zerolimit.md) — reviewed as `FINDING-01950-imc-ydarc-switchydwitharc-idealcloser-closerwitharc-1-goff.md`, which a later run renamed |
| Original SHA-256 | 1fb4e4eadfa17ebe82b7eab2561624cada913382dc1232d1af4689d6f5ee1275 |

## Why this is a false positive

The quenched off-state is i=Goff*v and the closed state is v=Ron*i; neither parameter is divided. Ron=0 is the ideal closed switch and Goff=0 the ideal open switch, consistent with the base ideal-switch family. A particular connected circuit can still become structurally singular.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Interfaces/IdealSwitchWithArc.mo:5`. Role: `parameter`; binding: `switchYDwithArc.idealCloser.Goff[1]`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Interfaces/IdealSwitchWithArc.mo — source snapshot](../evidence/sources/bb6f6e3037a7aa8a-IdealSwitchWithArc.mo)

```modelica
3:   extends Modelica.Electrical.Analog.Interfaces.OnePort;
4:   parameter SI.Resistance Ron=1E-5 "Closed switch resistance";
5:   parameter SI.Conductance Goff=1E-5
6:     "Opened switch conductance";
7:   parameter SI.Voltage V0(start=30) "Initial arc voltage";
8:   parameter SI.VoltageSlope dVdt(start=10E3)
```

[Electrical/Analog/Interfaces/IdealSwitchWithArc.mo — source snapshot](../evidence/sources/bb6f6e3037a7aa8a-IdealSwitchWithArc.mo)

```modelica
2: partial model IdealSwitchWithArc "Ideal switch with simple arc model"
3:   extends Modelica.Electrical.Analog.Interfaces.OnePort;
4:   parameter SI.Resistance Ron=1E-5 "Closed switch resistance";
5:   parameter SI.Conductance Goff=1E-5
6:     "Opened switch conductance";
7:   parameter SI.Voltage V0(start=30) "Initial arc voltage";
8:   parameter SI.VoltageSlope dVdt(start=10E3)
9:     "Arc voltage slope";
10:   parameter SI.Voltage Vmax(start=60) "Max. arc voltage";
11:   extends Modelica.Electrical.Analog.Interfaces.ConditionalHeatPort(final T=293.15);
12:   Boolean off(start=true) "Indicates off-state (but maybe not quenched)";
13: protected
14:   Boolean quenched(start=true, fixed=true)
15:     "Indicating quenched arc (if switch is off)";
16:   discrete SI.Time tSwitch(start=-Modelica.Constants.inf, fixed=true)
17:     "Last switch off time instant";
18: equation
19:   when edge(off) then
20:     tSwitch = time;
21:   end when;
22:   quenched = off and (abs(i) <= abs(v)*Goff or pre(quenched));
23:   if off then
24:     if quenched then
25:       i = Goff*v;
26:     else
27:       v = min(Vmax, V0 + dVdt*(time - tSwitch))*sign(i);
28:     end if;
29:   else
30:     v = Ron*i;
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a03f73e52ba0cfd4.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/ideal-arc-switch-zero.md) · [Index](../README.md)
