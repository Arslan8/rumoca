# False positives and explicit non-defects: `ideal-multistar-resistance`

**1 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

R is filled into Polyphase.Basic.Resistor, which delegates to scalar Basic.Resistor. That contract permits zero/signed resistance and uses v=R*i. Zero may create an ideal connection with topology consequences, but the parameter itself is not an unguarded divisor.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0733](../false-positives/DECL-0733.md) | — | `R` | Source/semantic review | [DECL-multistarresistance-r-6.md](../../bugs/DECL-multistarresistance-r-6.md) |
