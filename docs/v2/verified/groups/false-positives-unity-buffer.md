# False positives and explicit non-defects: `unity-buffer`

**1 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

R2=(k-1)*R1 deliberately gives zero at the default k=1. R2 feeds a Basic.Resistor, whose documented domain includes zero, and there is no reciprocal R2 in this buffer. Rejecting the nominal unity-gain configuration is a false positive.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0627](../false-positives/DECL-0627.md) | — | `R2` | Source/semantic review | [DECL-buffer-r2-6.md](../../bugs/DECL-buffer-r2-6.md) |
