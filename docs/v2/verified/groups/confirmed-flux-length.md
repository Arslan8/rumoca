# Execution-confirmed defects: `flux-length`

**4 report instances**

[Back to Execution-confirmed defects](../confirmed.md) · [Overview](../README.md)

## Common decision rule

G_m = mu_0*mu_r*A/l is evaluated with l=0. The numerator is nonzero for the nominal positive area/permeability. Baseline passes; the l=0 source-modified and final-evaluated models explicitly report division by zero.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [BUG-011](../confirmed/BUG-011.md) | ModelicaTest.Magnetic.FluxTubes.Sensors | `genericFluxTube.l` | Prior paired execution | [BUG-sensors-genericfluxtube-l.md](../../bugs/BUG-sensors-genericfluxtube-l.md) |
| [BUG-019](../confirmed/BUG-019.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube1.l` | Prior paired execution | [BUG-sources-genericfluxtube1-l.md](../../bugs/BUG-sources-genericfluxtube1-l.md) |
| [BUG-021](../confirmed/BUG-021.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube2.l` | Prior paired execution | [BUG-sources-genericfluxtube2-l.md](../../bugs/BUG-sources-genericfluxtube2-l.md) |
| [BUG-023](../confirmed/BUG-023.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube3.l` | Prior paired execution | [BUG-sources-genericfluxtube3-l.md](../../bugs/BUG-sources-genericfluxtube3-l.md) |
