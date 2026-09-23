# False positives and explicit non-defects: `zero-machine-airgap-inductance`

**5 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

The air-gap model constructs an inductance matrix and computes psi=L*i. Neither the main inductance nor the protected matrix is divided. Zero removes the corresponding magnetic coupling; a useful machine normally needs coupling, but that engineering expectation is not an intrinsic arithmetic-domain failure.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0123](../false-positives/DECL-0123.md) | — | `Lmd` | Source/semantic review | [DECL-airgapr-lmd-3.md](../../bugs/DECL-airgapr-lmd-3.md) |
| [DECL-0124](../false-positives/DECL-0124.md) | — | `Lmq` | Source/semantic review | [DECL-airgapr-lmq-5.md](../../bugs/DECL-airgapr-lmq-5.md) |
| [DECL-0125](../false-positives/DECL-0125.md) | — | `L` | Source/semantic review | [DECL-airgapr-l-11.md](../../bugs/DECL-airgapr-l-11.md) |
| [DECL-0126](../false-positives/DECL-0126.md) | — | `Lm` | Source/semantic review | [DECL-airgaps-lm-3.md](../../bugs/DECL-airgaps-lm-3.md) |
| [DECL-0127](../false-positives/DECL-0127.md) | — | `L` | Source/semantic review | [DECL-airgaps-l-8.md](../../bugs/DECL-airgaps-l-8.md) |
