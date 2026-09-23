# False positives and explicit non-defects: `zero-thermal-conductance`

**1 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

The complete constitutive equation is Q_flow=G*dT. G is only a multiplier; at zero the component transports no heat. There is no source reciprocal and the component represents a lumped effective conductance, so a blanket strictly-positive claim rejects the ordinary insulation/open-thermal-path limit. A larger network may still need another equation for each isolated temperature.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0894](../false-positives/DECL-0894.md) | — | `G` | Source/semantic review | [DECL-thermalconductor-g-5.md](../../bugs/DECL-thermalconductor-g-5.md) |
