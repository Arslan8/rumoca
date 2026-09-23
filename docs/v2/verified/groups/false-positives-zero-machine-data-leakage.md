# False positives and explicit non-defects: `zero-machine-data-leakage`

**3 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

Lszero and Lssigma represent zero-sequence/stray inductance. They are forwarded to inductor equations that multiply derivatives by L; zero removes the leakage voltage drop. The Basic.Inductor contract explicitly permits zero. This does not excuse fsNominal=0 in the default formula, which is documented as a separate confirmed frequency bug.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0166](../false-positives/DECL-0166.md) | — | `Lszero` | Source/semantic review | [DECL-inductionmachinedata-lszero-20.md](../../bugs/DECL-inductionmachinedata-lszero-20.md) |
| [DECL-0167](../false-positives/DECL-0167.md) | — | `Lssigma` | Source/semantic review | [DECL-inductionmachinedata-lssigma-23.md](../../bugs/DECL-inductionmachinedata-lssigma-23.md) |
| [FINDING-02310](../false-positives/FINDING-02310.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aimsData.Lssigma` | Source/semantic review | [FINDING-ims-start-aimsdata-lssigma-unbounded.md](../../bugs/FINDING-ims-start-aimsdata-lssigma-unbounded.md) |
