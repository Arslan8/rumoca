# False positives and explicit non-defects: `zero-dc-machine-inductance`

**1 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

InductorDC uses v=if quasiStatic then 0 else L*der(i); it never divides by L. At L=0 the dynamic branch also imposes v=0. A missing positive bound is therefore not an intrinsic source defect, although a surrounding machine configuration may have incompatible state selections or constraints.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0131](../false-positives/DECL-0131.md) | — | `L` | Source/semantic review | [DECL-inductordc-l-5.md](../../bugs/DECL-inductordc-l-5.md) |
