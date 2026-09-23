# False positives and explicit non-defects: `ideal-dc-armature-la`

**1 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

La is passed to InductorDC, whose equation is v=L*der(i) outside quasi-static mode; zero removes the inductive voltage drop. The partial machine source has no unconditional reciprocal of this parameter. A particular initialization can still be topology-dependent.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0151](../false-positives/DECL-0151.md) | — | `La` | Source/semantic review | [DECL-partialbasicdcmachine-la-26.md](../../bugs/DECL-partialbasicdcmachine-la-26.md) |
