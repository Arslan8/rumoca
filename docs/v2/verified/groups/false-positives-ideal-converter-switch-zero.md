# False positives and explicit non-defects: `ideal-converter-switch-zero`

**4 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

These values are forwarded to IdealGTOThyristor/IdealDiode, whose IdealSemiconductor equations multiply by Ron or Goff rather than divide. Zero is the exact closed/open ideal limit. Some bridge topologies can become structurally singular, but that requires circuit-specific evidence and does not justify a blanket source-parameter positivity claim.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0068](../false-positives/DECL-0068.md) | — | `GoffTransistor` | Source/semantic review | [DECL-singlephase2level-gofftransistor-6.md](../../bugs/DECL-singlephase2level-gofftransistor-6.md) |
| [DECL-0069](../false-positives/DECL-0069.md) | — | `GoffDiode` | Source/semantic review | [DECL-singlephase2level-goffdiode-12.md](../../bugs/DECL-singlephase2level-goffdiode-12.md) |
| [DECL-0748](../false-positives/DECL-0748.md) | — | `RonTransistor` | Source/semantic review | [DECL-singlephase2level-rontransistor-4.md](../../bugs/DECL-singlephase2level-rontransistor-4.md) |
| [DECL-0749](../false-positives/DECL-0749.md) | — | `RonDiode` | Source/semantic review | [DECL-singlephase2level-rondiode-10.md](../../bugs/DECL-singlephase2level-rondiode-10.md) |
