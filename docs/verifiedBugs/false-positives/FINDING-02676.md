# FINDING-02676: Polyphase inductance delegates to zero-capable scalar inductors

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-polyphase-inductance |
| Model | Modelica.Electrical.Machines.Examples.Transformers.AsymmetricalLoad |
| Target | transformer.l2sigma.L |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-asymmetricalload-transformer-l2sigma-l-zerolimit.md](../../v2/bugs/FINDING-asymmetricalload-transformer-l2sigma-l-zerolimit.md) — reviewed as `FINDING-02676-asymmetricalload-transformer-l2sigma-l.md`, which a later run renamed |
| Original SHA-256 | 8ff0bf2d759116a10bedf834422889912115fa97613c85d319d6509967c4feb6 |

## Why this is a false positive

The polyphase component passes each L element to Basic.Inductor. That scalar component explicitly documents positive or zero inductance and uses L*der(i)=v. A universal positive-only finding contradicts the delegated contract.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Polyphase/Basic/Inductor.mo:4`. Role: `parameter`; binding: `fill(transformer.L2sigma, transformer.m)`; effective min: `None`; effective max: `None`. 

[Electrical/Polyphase/Basic/Inductor.mo — source snapshot](../evidence/sources/d0226d76ada881f1-Inductor.mo)

```modelica
2: model Inductor "Ideal linear electrical inductors"
3:   extends Interfaces.TwoPlug;
4:   parameter SI.Inductance L[m](start=fill(1, m)) "Inductance";
5:   Modelica.Electrical.Analog.Basic.Inductor inductor[m](final L=L)
6:     annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
7: equation
```

[Electrical/Polyphase/Basic/Inductor.mo — source snapshot](../evidence/sources/d0226d76ada881f1-Inductor.mo)

```modelica
2: model Inductor "Ideal linear electrical inductors"
3:   extends Interfaces.TwoPlug;
4:   parameter SI.Inductance L[m](start=fill(1, m)) "Inductance";
5:   Modelica.Electrical.Analog.Basic.Inductor inductor[m](final L=L)
6:     annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
7: equation
8:   connect(inductor.p, plug_p.pin)
9:     annotation (Line(points={{-10,0},{-100,0}}, color={0,0,255}));
10:   connect(inductor.n, plug_n.pin)
11:     annotation (Line(points={{10,0},{100,0}}, color={0,0,255}));
```

[Electrical/Analog/Basic/Inductor.mo — source snapshot](../evidence/sources/fff3148b5c6bf96b-Inductor.mo)

```modelica
2: model Inductor "Ideal linear electrical inductor"
3:   extends Interfaces.OnePort(i(start=0));
4:   parameter SI.Inductance L(start=1) "Inductance";
5: 
6: equation
7:   L*der(i) = v;
8:   annotation (
9:     Documentation(info="<html>
10: <p>The linear inductor connects the branch voltage <em>v</em> with the branch current <em>i</em> by <em>v = L * di/dt</em>. The Inductance <em>L</em> is allowed to be positive, or zero.</p>
11: 
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/9b0b7f4a290b32fb.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-polyphase-inductance.md) · [Index](../README.md)
