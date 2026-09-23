# False positives and explicit non-defects: `disabled-core-loss`

**1 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

GcRef is final and explicitly equals zero when PRef<=0; the default PRef is zero. Both DC and induction-machine Core consumers handle this branch by setting core-loss currents to zero. The reported default-value invariant violation is intended lossless behavior, not a failure.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0061](../false-positives/DECL-0061.md) | — | `GcRef` | Source/semantic review | [DECL-coreparameters-gcref-18.md](../../bugs/DECL-coreparameters-gcref-18.md) |
