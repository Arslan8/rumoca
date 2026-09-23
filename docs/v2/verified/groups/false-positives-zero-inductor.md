# False positives and explicit non-defects: `zero-inductor`

**1 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

The library documentation explicitly says L may be positive or zero, and the constitutive equation is L*der(i)=v rather than an unconditional division by L. At L=0 the element becomes the algebraic ideal-short constraint v=0. A translator or post-translation state representation that divides by L cannot be used to prove the source declaration wrong; connected topologies and fixed starts may still be inconsistent.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0096](../false-positives/DECL-0096.md) | — | `L` | Source/semantic review | [DECL-inductor-l-4.md](../../bugs/DECL-inductor-l-4.md) |
