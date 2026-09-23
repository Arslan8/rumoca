# Per-instance reports

One file per confirmed occurrence. A fix-site report (BUG-002 … BUG-019)
says *which declaration to change*; these say *which instance was proven to
fail, in which model, at which line*. `Damper.mo` instantiates three masses
and all three were confirmed separately, so all three have their own file.

Every line reference below was checked against MSL 4.1.0 source.

| ID | Model | Instance | Parameter | Trigger | Reach | Root cause |
|---|---|---|---|---|---|---|
| [BUG-020](BUG-020-continuous-load-j.md) | `Continuous` | `load` | `J` | `load.J = 0` | 32 models | BUG-018 |
| [BUG-021](BUG-021-damper-mass3-m.md) | `Damper` | `mass3` | `m` | `mass3.m = 0` | 18 models | BUG-002 |
| [BUG-022](BUG-022-chuacircuit-c2-c.md) | `ChuaCircuit` | `C2` | `C` | `C2.C = 0` | 12 models | BUG-013 |
| [BUG-023](BUG-023-chuacircuit-l-l.md) | `ChuaCircuit` | `L` | `L` | `L.L = 0` | 8 models | BUG-010 |
| [BUG-024](BUG-024-damper-mass1-m.md) | `Damper` | `mass1` | `m` | `mass1.m = 0` | 6 models | BUG-002 |
| [BUG-025](BUG-025-damper-mass2-m.md) | `Damper` | `mass2` | `m` | `mass2.m = 0` | 5 models | BUG-002 |
| [BUG-026](BUG-026-parallelresonance-inductor1-l.md) | `ParallelResonance` | `inductor1` | `L` | `inductor1.L = 0` | 4 models | BUG-010 |
| [BUG-027](BUG-027-parallelresonance-inductor2-l.md) | `ParallelResonance` | `inductor2` | `L` | `inductor2.L = 0` | 4 models | BUG-010 |
| [BUG-028](BUG-028-invertingamp-f.md) | `InvertingAmp` | `(model parameter)` | `f` | `f = 0` | 3 models | BUG-019 |
| [BUG-029](BUG-029-sensors-genericfluxtube-area.md) | `Sensors` | `genericFluxTube` | `area` | `genericFluxTube.area = 0` | 3 models | BUG-017 |
| [BUG-030](BUG-030-sensors-genericfluxtube-l.md) | `Sensors` | `genericFluxTube` | `l` | `genericFluxTube.l = 0` | 3 models | BUG-014 |
| [BUG-031](BUG-031-parallelresonance-capacitor1-c.md) | `ParallelResonance` | `capacitor1` | `C` | `capacitor1.C = 0` | 2 models | BUG-013 |
| [BUG-032](BUG-032-parallelresonance-capacitor2-c.md) | `ParallelResonance` | `capacitor2` | `C` | `capacitor2.C = 0` | 2 models | BUG-013 |
| [BUG-033](BUG-033-sensors-genericfluxtube-material-b_mymax.md) | `Sensors` | `genericFluxTube.material` | `B_myMax` | `genericFluxTube.material.B_myMax = 0` | 2 models | BUG-011 |
| [BUG-034](BUG-034-chuacircuit-c1-c.md) | `ChuaCircuit` | `C1` | `C` | `C1.C = 0` | 1 model | BUG-013 |
| [BUG-035](BUG-035-lcoscillator-opamp-vps.md) | `LCOscillator` | `opAmp` | `Vps` | `opAmp.Vps = -15` | 1 model | BUG-016 |
| [BUG-036](BUG-036-elasticbearing-housing-j.md) | `ElasticBearing` | `housing` | `J` | `housing.J = 0` | 1 model | BUG-018 |
| [BUG-037](BUG-037-elasticbearing-idealgear-ratio.md) | `ElasticBearing` | `idealGear` | `ratio` | `idealGear.ratio = 0` | 1 model | BUG-015 |
| [BUG-038](BUG-038-elasticbearing-shaft-j.md) | `ElasticBearing` | `shaft` | `J` | `shaft.J = 0` | 1 model | BUG-018 |
| [BUG-039](BUG-039-whyarrows-inertia2-m.md) | `WhyArrows` | `inertia2` | `m` | `inertia2.m = 0` | 1 model | BUG-002 |
| [BUG-040](BUG-040-sources-genericfluxtube1-l.md) | `Sources` | `genericFluxTube1` | `l` | `genericFluxTube1.l = 0` | 1 model | BUG-014 |
| [BUG-041](BUG-041-sources-genericfluxtube1-material-b_mymax.md) | `Sources` | `genericFluxTube1.material` | `B_myMax` | `genericFluxTube1.material.B_myMax = 0` | 1 model | BUG-011 |
| [BUG-042](BUG-042-sources-genericfluxtube2-l.md) | `Sources` | `genericFluxTube2` | `l` | `genericFluxTube2.l = 0` | 1 model | BUG-014 |
| [BUG-043](BUG-043-sources-genericfluxtube2-material-b_mymax.md) | `Sources` | `genericFluxTube2.material` | `B_myMax` | `genericFluxTube2.material.B_myMax = 0` | 1 model | BUG-011 |
| [BUG-044](BUG-044-sources-genericfluxtube3-l.md) | `Sources` | `genericFluxTube3` | `l` | `genericFluxTube3.l = 0` | 1 model | BUG-014 |
| [BUG-045](BUG-045-sources-genericfluxtube3-material-b_mymax.md) | `Sources` | `genericFluxTube3.material` | `B_myMax` | `genericFluxTube3.material.B_myMax = 0` | 1 model | BUG-011 |

## Grouped by root cause

**BUG-002** — 4 instances: [BUG-021](BUG-021-damper-mass3-m.md), [BUG-024](BUG-024-damper-mass1-m.md), [BUG-025](BUG-025-damper-mass2-m.md), [BUG-039](BUG-039-whyarrows-inertia2-m.md)

**BUG-010** — 3 instances: [BUG-023](BUG-023-chuacircuit-l-l.md), [BUG-026](BUG-026-parallelresonance-inductor1-l.md), [BUG-027](BUG-027-parallelresonance-inductor2-l.md)

**BUG-011** — 4 instances: [BUG-033](BUG-033-sensors-genericfluxtube-material-b_mymax.md), [BUG-041](BUG-041-sources-genericfluxtube1-material-b_mymax.md), [BUG-043](BUG-043-sources-genericfluxtube2-material-b_mymax.md), [BUG-045](BUG-045-sources-genericfluxtube3-material-b_mymax.md)

**BUG-013** — 4 instances: [BUG-022](BUG-022-chuacircuit-c2-c.md), [BUG-031](BUG-031-parallelresonance-capacitor1-c.md), [BUG-032](BUG-032-parallelresonance-capacitor2-c.md), [BUG-034](BUG-034-chuacircuit-c1-c.md)

**BUG-014** — 4 instances: [BUG-030](BUG-030-sensors-genericfluxtube-l.md), [BUG-040](BUG-040-sources-genericfluxtube1-l.md), [BUG-042](BUG-042-sources-genericfluxtube2-l.md), [BUG-044](BUG-044-sources-genericfluxtube3-l.md)

**BUG-015** — 1 instance: [BUG-037](BUG-037-elasticbearing-idealgear-ratio.md)

**BUG-016** — 1 instance: [BUG-035](BUG-035-lcoscillator-opamp-vps.md)

**BUG-017** — 1 instance: [BUG-029](BUG-029-sensors-genericfluxtube-area.md)

**BUG-018** — 3 instances: [BUG-020](BUG-020-continuous-load-j.md), [BUG-036](BUG-036-elasticbearing-housing-j.md), [BUG-038](BUG-038-elasticbearing-shaft-j.md)

**BUG-019** — 1 instance: [BUG-028](BUG-028-invertingamp-f.md)

## Withdrawn

Five instances were execution-confirmed and are **not** reported, because
the trigger was a value the declaration already forbids:

| Model | Trigger | Declares |
|---|---|---|
| `Translational.Examples.ElastoGap` | `elastoGap1.s_ref = 0` | `min=Modelica.Constants.eps` |
| `Translational.Examples.ElastoGap` | `elastoGap2.s_ref = 0` | `min=Modelica.Constants.eps` |
| `FluxTubes...TranslatoryArmatureAndStopper` | `stopper_xMax.s_ref = 0` | `min=Modelica.Constants.eps` |
| `FluxTubes...TranslatoryArmatureAndStopper` | `stopper_xMin.s_ref = 0` | `min=Modelica.Constants.eps` |
| `Clocked...SimpleControlledDrive.Continuous` | `PI.T = 0` | `min=Modelica.Constants.small` |

Cause in [TOOLBUG-010](../toolbugs/TOOLBUG-010-divisorsan-misread-non-literal-min.md).

## Regenerating

```bash
python3 tools/sweep/gen_instance_reports.py INSTANCES.json 20
```
