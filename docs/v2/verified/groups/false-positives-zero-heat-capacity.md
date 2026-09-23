# False positives and explicit non-defects: `zero-heat-capacity`

**1 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

The source equation is C*der(T)=port.Q_flow, not division by C. At C=0 it imposes zero stored heat flow and removes the temperature state. Thus the missing/zero-bound claim does not by itself prove a defect; fixed starts or isolated thermal topologies may still become inconsistent. The two divisor-reach reports for this declaration remain unresolved separately because they make a different compiler-IR claim.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0095](../false-positives/DECL-0095.md) | — | `C` | Source/semantic review | [DECL-heatcapacitor-c-3.md](../../bugs/DECL-heatcapacitor-c-3.md) |
