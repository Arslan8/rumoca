# False positives and explicit non-defects: `switched-capacitor-guard`

**1 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

The model explicitly represents positive or negative resistance. Its capacitance uses clock/max(eps*oneOhm,abs(R)), where protected constant oneOhm=1. Thus R=0 does not zero the denominator, negative R is handled by abs, and oneOhm is a fixed unit-conversion constant in this model rather than a reported adjustable parameter.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0656](../false-positives/DECL-0656.md) | — | `R` | Source/semantic review | [DECL-switchedcapacitor-r-5.md](../../bugs/DECL-switchedcapacitor-r-5.md) |
