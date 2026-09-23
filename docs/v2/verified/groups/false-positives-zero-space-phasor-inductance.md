# False positives and explicit non-defects: `zero-space-phasor-inductance`

**1 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

Both axis equations are v_[j]=L[j]*der(i_[j]); L is a multiplier and is never divided. A zero entry sets the corresponding voltage drop to zero. The report applies a strictly-positive heuristic where the component equations support an ideal zero-leakage limit.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0130](../false-positives/DECL-0130.md) | — | `L` | Source/semantic review | [DECL-inductor-l-3.md](../../bugs/DECL-inductor-l-3.md) |
