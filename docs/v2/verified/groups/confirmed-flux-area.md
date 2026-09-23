# Execution-confirmed defects: `flux-area`

**1 report instances**

[Back to Execution-confirmed defects](../confirmed.md) · [Overview](../README.md)

## Common decision rule

A=area; G_m=mu_0*mu_r*A/l; the inherited equations use R_m=1/G_m and B=Phi/A. area=0 makes both reciprocals undefined. Runtime overrides report division by zero; final-evaluated translation is structurally singular. This is not merely dividing a storage equation while selecting a state.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [BUG-025](../confirmed/BUG-025.md) | ModelicaTest.Magnetic.FluxTubes.Sensors | `genericFluxTube.area` | Prior paired execution | [BUG-sensors-genericfluxtube-area.md](../../bugs/BUG-sensors-genericfluxtube-area.md) |
