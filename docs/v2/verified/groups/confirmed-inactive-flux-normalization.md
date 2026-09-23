# Execution-confirmed defects: `inactive-flux-normalization`

**4 report instances**

[Back to Execution-confirmed defects](../confirmed.md) · [Overview](../README.md)

## Common decision rule

These instances set nonLinearPermeability=false, so B_myMax is documented as unused. Nevertheless FixedShape unconditionally defines B_N=abs(B/material.B_myMax). At B_myMax=0 this auxiliary equation is undefined. Rumoca and post-translation OpenModelica overrides fail; OpenModelica recompilation succeeds after removing the unused B_N equation. Therefore the original claim of a robust two-tool active-material failure is overstated, but the unconditional inactive-branch calculation is a source-verified defect.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [BUG-010](../confirmed/BUG-010.md) | ModelicaTest.Magnetic.FluxTubes.Sensors | `genericFluxTube.material.B_myMax` | Prior paired execution | [BUG-sensors-genericfluxtube-material-b-mymax.md](../../bugs/BUG-sensors-genericfluxtube-material-b-mymax.md) |
| [BUG-018](../confirmed/BUG-018.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube1.material.B_myMax` | Prior paired execution | [BUG-sources-genericfluxtube1-material-b-mymax.md](../../bugs/BUG-sources-genericfluxtube1-material-b-mymax.md) |
| [BUG-020](../confirmed/BUG-020.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube2.material.B_myMax` | Prior paired execution | [BUG-sources-genericfluxtube2-material-b-mymax.md](../../bugs/BUG-sources-genericfluxtube2-material-b-mymax.md) |
| [BUG-022](../confirmed/BUG-022.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube3.material.B_myMax` | Prior paired execution | [BUG-sources-genericfluxtube3-material-b-mymax.md](../../bugs/BUG-sources-genericfluxtube3-material-b-mymax.md) |
