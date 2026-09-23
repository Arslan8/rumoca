# OpenModelica source-instantiated verification

Rumoca generated the candidates; OpenModelica is the independent verifier. Every attempted trigger is encoded in a generated subclass before translation, and is compared with the unmodified model.

| Outcome | Unique model/witness cases | v2 report instances |
|---|---:|---:|
| `confirmed-by-omc` | 320 | 817 |
| `not-reproduced-by-omc` | 86 | 224 |
| `refuted-illegal-witness` | 122 | 284 |
| `unresolved-baseline-fails` | 32 | 73 |
| `unresolved-trigger-failed-other` | 22 | 25 |

Array/scope cases not attempted: **86 report instances**.

Only `confirmed-by-omc` is positive execution evidence. `not-reproduced-by-omc` must not remain labelled a true positive without stronger path evidence. Baseline failures, timeouts and harness gaps are unresolved.

[Raw JSON evidence](omc-source-verification.json) · [v2 verification index](README.md)
