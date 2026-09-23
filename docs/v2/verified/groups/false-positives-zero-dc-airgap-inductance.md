# False positives and explicit non-defects: `zero-dc-airgap-inductance`

**1 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

The complete magnetic relation is psi_e=Le*ie. Le=0 produces zero excitation flux; this source does not divide by Le. Whether such an idealized machine remains useful is separate from the reported claim that the declaration necessarily causes an arithmetic failure.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0122](../false-positives/DECL-0122.md) | — | `Le` | Source/semantic review | [DECL-airgapdc-le-4.md](../../bugs/DECL-airgapdc-le-4.md) |
