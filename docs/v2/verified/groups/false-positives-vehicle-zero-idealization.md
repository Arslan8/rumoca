# False positives and explicit non-defects: `vehicle-zero-idealization`

**1 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

J is passed to Rotational.Inertia and used in torque balance. At zero it removes that inertia or aerodynamic term; the Vehicle source does not divide by it. A physical production vehicle has positive values, but this component also supports idealized/lumped configurations, so a blanket strictly-positive sanitizer finding is not a verified bug.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0367](../false-positives/DECL-0367.md) | — | `J` | Source/semantic review | [DECL-vehicle-j-5.md](../../bugs/DECL-vehicle-j-5.md) |
