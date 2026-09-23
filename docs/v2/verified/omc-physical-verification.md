# OpenModelica physical-witness execution

Each case modifies the reported parameter in Modelica source before translation and compares it with the unmodified model. Zero tests a reported permissive lower bound; -1 tests a reported missing domain bound.

| Outcome | Reports |
|---|---:|
| `refuted-illegal-witness` | 90 |
| `unresolved-baseline-fails` | 5 |
| `witness-admitted-with-warning` | 10 |
| `witness-causes-omc-numerical-failure` | 2 |
| `witness-executes-cleanly` | 70 |

Unsupported cases: **0 reports**.

A clean negative/zero execution proves that the value is admitted, but does not by itself prove what the physical contract ought to be. A numerical failure is behavioral evidence only when the unmodified baseline is clean. Physical intent still requires the reviewed source contract recorded in the per-report audit.

[Raw JSON evidence](omc-physical-verification.json) · [v2 verification index](README.md)
