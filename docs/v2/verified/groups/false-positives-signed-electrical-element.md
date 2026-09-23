# False positives and explicit non-defects: `signed-electrical-element`

**2 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

The component documentation explicitly permits positive, zero and negative values. Its constitutive equation is v=R_actual*i or i=G_actual*v. A universal strictly-positive physical-domain rule contradicts this contract; a particular singular circuit would require its own topology-specific evidence.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0043](../false-positives/DECL-0043.md) | — | `G` | Source/semantic review | [DECL-conductor-g-3.md](../../bugs/DECL-conductor-g-3.md) |
| [DECL-0604](../false-positives/DECL-0604.md) | — | `R` | Source/semantic review | [DECL-resistor-r-3.md](../../bugs/DECL-resistor-r-3.md) |
