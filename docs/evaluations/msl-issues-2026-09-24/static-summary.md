# Complete-corpus static results

[Overview](README.md) · [Per-model diagnostics](models.md)

5476 executable report instances across 255 models. Counts below are conservative **historical-operation matches**, not unique-root-cause recall.

| Historical verdict | Total | Ambiguous site match | Explicit non-defect | Intent advisory | No matching report | Static candidate | Unresolved analysis |
|---|---:|---:|---:|---:|---:|---:|---:|
| confirmed | 819 | 10 | 0 | 0 | 0 | 809 | 0 |
| false-positive | 3321 | 0 | 2986 | 6 | 1 | 328 | 0 |
| unresolved | 666 | 18 | 0 | 0 | 0 | 521 | 127 |
| advisory | 638 | 0 | 8 | 630 | 0 | 0 | 0 |
| candidate | 32 | 0 | 0 | 0 | 0 | 32 | 0 |

An ambiguous match usually means the old report lacks sufficient operation/witness identity, or the new witness differs. It is neither a demonstrated miss nor an exact hit.

## Current target-level output (weaker, not used as exact detection)

| Historical verdict | Current output | Reports |
|---|---|---:|
| advisory | Explicit non-defect | 8 |
| advisory | Intent advisory | 630 |
| candidate | Static candidate | 32 |
| confirmed | Static candidate | 819 |
| false-positive | Explicit non-defect | 2984 |
| false-positive | Intent advisory | 6 |
| false-positive | No matching report | 1 |
| false-positive | Static candidate | 330 |
| unresolved | Explicit non-defect | 6 |
| unresolved | Static candidate | 544 |
| unresolved | Unresolved analysis | 116 |

## Analyzer health

| Component | Failed operations |
|---|---:|
| No recorded analyzer errors | 0 |

These are not precision/recall estimates for all MSL defects. The ledger mostly originated from these same detector families; unresolved/advisory rows are not labeled positives. See the independent benchmark separately.
