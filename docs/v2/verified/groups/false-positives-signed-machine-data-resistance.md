# False positives and explicit non-defects: `signed-machine-data-resistance`

**1 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

Rs is a stator resistance data field passed to resistor components. The underlying Basic.Resistor contract explicitly permits positive, zero and negative resistance and uses v=R_actual*i. A real machine normally has positive copper resistance, but the ideal zero-loss limit is mathematically supported; a blanket missing-bound finding is not a bug.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0717](../false-positives/DECL-0717.md) | — | `Rs` | Source/semantic review | [DECL-inductionmachinedata-rs-10.md](../../bugs/DECL-inductionmachinedata-rs-10.md) |
