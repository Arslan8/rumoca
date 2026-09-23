# False positives and explicit non-defects: `signed-inertia-tensor`

**3 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

Off-diagonal inertia tensor entries are signed (the declaration explicitly allows negative infinity as a lower bound); zero off-diagonal entries describe principal axes. The assembled tensor must satisfy matrix-level physical constraints, not elementwise strict positivity. This does not dismiss a separate invalid diagonal/eigenvalue report.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0356](../false-positives/DECL-0356.md) | — | `I` | Source/semantic review | [DECL-body-i-114.md](../../bugs/DECL-body-i-114.md) |
| [DECL-0357](../false-positives/DECL-0357.md) | — | `I` | Source/semantic review | [DECL-bodybox-i-111.md](../../bugs/DECL-bodybox-i-111.md) |
| [DECL-0359](../false-positives/DECL-0359.md) | — | `I` | Source/semantic review | [DECL-bodycylinder-i-114.md](../../bugs/DECL-bodycylinder-i-114.md) |
