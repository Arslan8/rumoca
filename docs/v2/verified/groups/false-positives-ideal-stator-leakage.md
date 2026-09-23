# False positives and explicit non-defects: `ideal-stator-leakage`

**3 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

Lszero and Lssigma are passed to scalar/space-phasor inductors whose equations multiply current derivatives by L. Zero is the ideal no-leakage voltage-drop limit; there is no intrinsic reciprocal. The separate fsNominal-derived default formula can still require a positive nominal frequency.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0152](../false-positives/DECL-0152.md) | — | `Lszero` | Source/semantic review | [DECL-partialbasicinductionmachine-lszero-20.md](../../bugs/DECL-partialbasicinductionmachine-lszero-20.md) |
| [DECL-0153](../false-positives/DECL-0153.md) | — | `Lssigma` | Source/semantic review | [DECL-partialbasicinductionmachine-lssigma-23.md](../../bugs/DECL-partialbasicinductionmachine-lssigma-23.md) |
| [FINDING-02272](../false-positives/FINDING-02272.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.Lssigma` | Source/semantic review | [FINDING-ims-start-aims-lssigma-unbounded.md](../../bugs/FINDING-ims-start-aims-lssigma-unbounded.md) |
