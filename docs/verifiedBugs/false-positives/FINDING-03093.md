# FINDING-03093: Polyphase resistance/conductance delegates to signed scalar elements

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | signed-polyphase-element |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive |
| Target | earthing.resistor.R |
| Student classification | physical-domain-unenforced |
| Original report | `FINDING-03093-thyristorbridge2mpulse-dc-drive-earthing-resistor-r.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | b38b7d512c83d2819828f4c1617b55931c3d704e8e6b37a53847fda942a3f3f0 |

## Why this is a false positive

This component is an array wrapper that passes each R or G to Basic.Resistor/Conductor. The scalar contract explicitly allows positive, zero and negative values and uses a multiplicative constitutive equation. A universal strictly-positive rule is therefore wrong here; a particular singular network requires topology-specific evidence.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Polyphase/Basic/Resistor.mo:4`. Role: `parameter`; binding: `fill(earthing.R, earthing.mBasic)`; effective min: `None`; effective max: `None`. 

[Electrical/Polyphase/Basic/Resistor.mo — source snapshot](../evidence/sources/878881328edeca93-Resistor.mo)

```modelica
2: model Resistor "Ideal linear electrical resistors"
3:   extends Interfaces.TwoPlug;
4:   parameter SI.Resistance R[m](start=fill(1, m))
5:     "Resistances R_ref at temperatures T_ref";
6:   parameter SI.Temperature T_ref[m]=fill(300.15, m)
7:     "Reference temperatures";
```

[Electrical/Polyphase/Basic/Resistor.mo — source snapshot](../evidence/sources/878881328edeca93-Resistor.mo)

```modelica
2: model Resistor "Ideal linear electrical resistors"
3:   extends Interfaces.TwoPlug;
4:   parameter SI.Resistance R[m](start=fill(1, m))
5:     "Resistances R_ref at temperatures T_ref";
6:   parameter SI.Temperature T_ref[m]=fill(300.15, m)
7:     "Reference temperatures";
8:   parameter SI.LinearTemperatureCoefficient alpha[m]=zeros(m)
9:     "Temperature coefficients of resistances at reference temperatures";
10:   extends Polyphase.Interfaces.ConditionalHeatPort(final mh=m, T=T_ref);
11:   Modelica.Electrical.Analog.Basic.Resistor resistor[m](
12:     final R=R,
13:     final T_ref=T_ref,
14:     final alpha=alpha,
15:     each final useHeatPort=useHeatPort,
16:     final T=T) annotation (Placement(
17:         transformation(extent={{-10,-10},{10,10}})));
18: equation
```

[Electrical/Analog/Basic/Resistor.mo — source snapshot](../evidence/sources/f3257fcb99588782-Resistor.mo)

```modelica
13: 
14: equation
15:   assert((1 + alpha*(T_heatPort - T_ref)) >= Modelica.Constants.eps,
16:     "Temperature outside scope of model!");
17:   R_actual = R*(1 + alpha*(T_heatPort - T_ref));
18:   v = R_actual*i;
19:   LossPower = v*i;
20:   annotation (
21:     Documentation(info="<html>
22: <p>The linear resistor connects the branch voltage <em>v</em> with the branch current <em>i</em> by <em>i*R = v</em>. The Resistance <em>R</em> is allowed to be positive, zero, or negative.</p>
23: </html>",
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d8e62ee37d41ac80.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/signed-polyphase-element.md) · [Index](../README.md)
