# FINDING-03190: MultiStarResistance delegates to zero-capable resistor elements

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | ideal-multistar-resistance |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_R |
| Target | multiStarResistance.R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-thyristorbridge2mpulse-r-multistarresistance-r-ruleoff.md](../../v2/bugs/FINDING-thyristorbridge2mpulse-r-multistarresistance-r-ruleoff.md) — reviewed as `FINDING-03190-thyristorbridge2mpulse-r-multistarresistance-r.md`, which a later run renamed |
| Original SHA-256 | 767118bd895efd16248a14b48c814557d32d554ff83092be32614a6399b52d47 |

## Why this is a false positive

R is filled into Polyphase.Basic.Resistor, which delegates to scalar Basic.Resistor. That contract permits zero/signed resistance and uses v=R*i. Zero may create an ideal connection with topology consequences, but the parameter itself is not an unguarded divisor.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Polyphase/Basic/MultiStarResistance.mo:6`. Role: `parameter`; binding: `1000000.0`; effective min: `None`; effective max: `None`. 

[Electrical/Polyphase/Basic/MultiStarResistance.mo — source snapshot](../evidence/sources/ea92c0fc8fb6f8ed-MultiStarResistance.mo)

```modelica
4:   parameter Integer m(final min=2) = 3 "Number of phases" annotation(Evaluate=true);
5:   final parameter Integer mBasic=numberOfSymmetricBaseSystems(m) "Number of symmetric base systems";
6:   parameter SI.Resistance R=1e6 "Insulation resistance between base systems";
7:   Polyphase.Interfaces.PositivePlug plug(m=m)
8:     annotation (Placement(transformation(extent={{-110,-10},{-90,10}})));
9:   Polyphase.Basic.MultiStar multiStar(m=m) annotation (Placement(transformation(
```

[Electrical/Polyphase/Basic/MultiStarResistance.mo — source snapshot](../evidence/sources/ea92c0fc8fb6f8ed-MultiStarResistance.mo)

```modelica
2: model MultiStarResistance "Resistance connection of star points"
3:   import Modelica.Electrical.Polyphase.Functions.numberOfSymmetricBaseSystems;
4:   parameter Integer m(final min=2) = 3 "Number of phases" annotation(Evaluate=true);
5:   final parameter Integer mBasic=numberOfSymmetricBaseSystems(m) "Number of symmetric base systems";
6:   parameter SI.Resistance R=1e6 "Insulation resistance between base systems";
7:   Polyphase.Interfaces.PositivePlug plug(m=m)
8:     annotation (Placement(transformation(extent={{-110,-10},{-90,10}})));
9:   Polyphase.Basic.MultiStar multiStar(m=m) annotation (Placement(transformation(
10:           extent={{-10,-10},{10,10}}, origin={-50,0})));
11:   Polyphase.Basic.Resistor resistor(m=mBasic, R=fill(R, mBasic))
12:     annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
13:   Polyphase.Basic.Star star(m=mBasic) annotation (Placement(transformation(
14:           extent={{-10,-10},{10,10}}, origin={50,0})));
15:   Modelica.Electrical.Analog.Interfaces.NegativePin pin annotation (
16:       Placement(transformation(
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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/79dbe87f648dd167.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/ideal-multistar-resistance.md) · [Index](../README.md)
