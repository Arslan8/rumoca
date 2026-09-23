# Verified bugs

This folder is the single index of confirmed issues reported so far. It keeps
target-model findings and Rumoca/bitcode defects together while retaining their
origin in the table below. Limitations, coverage notes, and unfiled upstream
drafts are intentionally excluded.

Verification levels:

| Level | Meaning |
|---|---|
| Current reproducer | Reproduced against the current checkout on 2026-09-14. |
| Cross-confirmed report | The report includes a clean baseline and failing trigger in Rumoca and OpenModelica; the cited source was also inspected. |
| Source-proven | The cited MSL declaration and singular equation path were inspected; the report's isolated model reproduces the path, but the full component is not independently simulatable. |
| Fixed regression | The historical bug is confirmed by its report and the current end-to-end reproducer now passes. |

## Direct divide-by-zero defects

These are not merely structural-singularity reports: each has a reachable zero
denominator and was reproduced in the current Rumoca checkout on 2026-09-14.

| ID | Zero denominator | Current result |
|---|---|---|
| [BUG-003](BUG-003-switchedrlc-zero-resistance.md) | `V/R`, with `R = 0` | `i_R = NaN` |
| [BUG-011](BUG-011-fluxtubes-b-mymax-unguarded-divisor.md) | `B/B_myMax`, with `B_myMax = 0` | `genericFluxTube.B = -inf` |
| [BUG-014](BUG-014-genericfluxtube-l-unbounded-divisor.md) | `mu_0*mu_r*A/l`, with `l = 0` | `mu_r = -inf` |
| [BUG-017](BUG-017-genericfluxtube-area-chain-divisor.md) | `area = 0` then `1/G_m`, two classes away | `Phi = NaN` |
| [BUG-016](BUG-016-relational-invariant-between-two-parameters.md) | `p_s/(Vps - Vns)`, with `Vps = Vns` | `opAmp.i_s = -inf` |

## Complete verified-bug index

| ID | Origin | Fault class | Trigger / defect | Verification | Current status |
|---|---|---|---|---|---|
| [BUG-001](BUG-001-comprehension-in-for-equation-panic.md) | Rumoca | Compiler panic | Array comprehension in an algorithm, `when`, `assert`, or `for` context panics. | Current reproducer | Open |
| [BUG-002](BUG-002-msl-zero-mass-within-declared-bound.md) | MSL | Singular coefficient | `Mass.m = 0` or `Inertia.J = 0` is admitted but makes the model singular. | Current reproducer; report cross-confirmed | Open upstream |
| [BUG-003](BUG-003-switchedrlc-zero-resistance.md) | Repo example | **Direct divide by zero** | `R = 0` makes `i_R = V/R` non-finite. | Current reproducer | Open |
| [BUG-004](BUG-004-record-array-destructured-without-subscript.md) | Rumoca | Invalid Flat reference | Vectorised record-function call emits an unresolved whole-array field. | Current reproducer | Open |
| [BUG-005](BUG-005-multibody-rotor1d-zero-inertia.md) | MSL | Singular coefficient | `Rotor1D.J = 0` leaves acceleration undetermined. | Source-proven | Open upstream |
| [BUG-006](BUG-006-bound-propagated-into-a-different-component.md) | MSL | Propagated singular coefficient | `Der.k = 0` propagates to a zero capacitance coefficient. | Source-proven | Open upstream |
| [BUG-007](BUG-007-dae-drops-predefined-enum-in-assert.md) | Rumoca | DAE type handling | `AssertionLevel` in `assert` was rejected by DAE lowering. | Fixed regression | Fixed |
| [BUG-008](BUG-008-bitcode-enumeration-round-trip.md) | Bitcode | Wire-format type loss | Enumeration literals were exported as integers. | Fixed regression | Fixed |
| [BUG-009](BUG-009-bitcode-omits-discrete-definitions.md) | Bitcode | Wire-format topology loss | Discrete B.1c definitions were omitted from bitcode. | Fixed regression | Fixed |
| [BUG-010](BUG-010-inductor-documents-zero-it-cannot-honour.md) | MSL | Degenerate differential equation | `Inductor.L = 0` contradicts the component documentation and fails. | Cross-confirmed report | Open upstream |
| [BUG-011](BUG-011-fluxtubes-b-mymax-unguarded-divisor.md) | MSL | **Direct divide by zero** | `B_myMax = 0` divides by zero. | Current reproducer; report cross-confirmed | Open upstream |
| [BUG-012](BUG-012-variablepermeance-unbounded-input.md) | MSL | Singular coefficient | Permeance input at or below zero leaves voltage undetermined. | Cross-confirmed report | Open upstream |
| [BUG-013](BUG-013-capacitor-zero-capacitance-topology-dependent.md) | MSL | Topology-dependent degeneration | `Capacitor.C = 0` is unsafe in some admitted circuit topologies. | Cross-confirmed report | Open upstream |
| [BUG-014](BUG-014-genericfluxtube-l-unbounded-divisor.md) | MSL | **Direct divide by zero** | `l = 0` is the divisor in `G_m = mu_0*mu_r*A/l`. | Current reproducer; report cross-confirmed | Open upstream |
| [BUG-017](BUG-017-genericfluxtube-area-chain-divisor.md) | MSL | **Propagated divide by zero** | `area = 0` reaches `1/G_m` in the base class. | Current reproducer; report cross-confirmed | Open upstream |
| [BUG-018](BUG-018-rotational-inertia-zero-within-declared-bound.md) | MSL | **Vanishing coefficient** | `J = 0` degenerates `J*a = tau`. | Current reproducer; report cross-confirmed | Open upstream |
| [BUG-019](BUG-019-invertingamp-frequency-unbounded-divisor.md) | MSL | **Direct divide by zero** | `f = 0` makes four trapezoid timings infinite. | Current reproducer; report cross-confirmed | Open upstream |
| [BUG-015](BUG-015-idealgear-zero-ratio.md) | MSL | Degenerate constraint | `ratio = 0` decouples the gear. | Cross-confirmed report | Open upstream |
| [BUG-016](BUG-016-relational-invariant-between-two-parameters.md) | MSL | **Direct divide by zero** | `Vps = Vns` divides supply power by zero. | Current reproducer; report cross-confirmed | Open upstream |

The source-proven entries are included because their reports distinguish that
level clearly; they should not be represented as whole-model, two-tool runs
until such a reproducer exists.
