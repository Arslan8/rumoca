# False positives and explicit non-defects: `zero-machine-data-inertia`

**2 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

These record fields are forwarded as Jr/Js to machine inertias. The consumer component uses J as a multiplier in torque balance, so zero is a massless algebraic limit. A report needs a specific incompatible drive-train topology or initialization; absence of a strictly-positive record bound alone is not a verified defect.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0320](../false-positives/DECL-0320.md) | — | `Jr` | Source/semantic review | [DECL-inductionmachinedata-jr-6.md](../../bugs/DECL-inductionmachinedata-jr-6.md) |
| [DECL-0321](../false-positives/DECL-0321.md) | — | `Js` | Source/semantic review | [DECL-inductionmachinedata-js-7.md](../../bugs/DECL-inductionmachinedata-js-7.md) |
