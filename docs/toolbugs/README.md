# Tool defects

Bugs in the **instrument**, not in anything being measured: Rumoca (the
compiler ModelSan reads models through) and `rumoca-bitcode` (the interchange
format built for this project).

These are **not findings**. A crash in AddressSanitizer is not a result about
the program under test. They are recorded because each one caps how much of a
corpus the detectors can see, and because two of them were defects in code
written for this project and had to be fixed before any result was trustworthy.

ModelSan's actual results are in [`../findings/`](../findings/).

## In Rumoca

| ID | Severity | Component | Effect on coverage |
|---|---|---|---|
| [BUG-001](../verified%20bugs/BUG-001-comprehension-in-for-equation-panic.md) | High | `rumoca-phase-dae` | Process abort on a comprehension in an algorithm, `when`, `assert` or `for`. Root cause: `all_model_expressions` walks 3 of 9 expression-bearing fields; 4 of its 5 other callers each patch around that differently. |
| [BUG-004](../verified%20bugs/BUG-004-record-array-destructured-without-subscript.md) | Medium | `rumoca-phase-flatten` | Blocks all of `QuasiStatic.Polyphase`. |
| [BUG-007](../verified%20bugs/BUG-007-dae-drops-predefined-enum-in-assert.md) | Medium | `rumoca-phase-dae` | 3-argument `assert(..., AssertionLevel.x)` unusable; 27 uses across 7 MSL files. |
| [LIMITATION-001](LIMITATION-001-index-reduction-drops-fixed-start.md) | — | `rumoca-phase-structural` | Correct, deliberate refusal; costs 2 MSL examples. |
| [LIMITATION-002](LIMITATION-002-no-solver-tolerance-control.md) | — | `compile-bitcode --simulate` | No `--rtol`/`--atol`, so the trajectory-differential detector cannot use a tight threshold. |

## In this project's own code

Both found by running the sweep against real MSL rather than hand-written
fixtures, and both were the same shape — export and import disagreeing, which
no test of either side alone could see.

| ID | Severity | Status |
|---|---|---|
| [BUG-008](../verified%20bugs/BUG-008-bitcode-enumeration-round-trip.md) | High | **Fixed.** Enumerations were exported as integers, so import rejected its own output. |
| [BUG-009](../verified%20bugs/BUG-009-bitcode-omits-discrete-definitions.md) | High | **Fixed.** No field existed for MLS Appendix B.1c definitions, so any discrete-valued variable broke round-trip. Affected every Boolean produced by a comparison. |

Bitcode tests: 29 passing, was 23. Round-trip audit over 60+ construct probes:
0 export-but-cannot-import, down from 9 models.

| [TOOLBUG-015](TOOLBUG-015-function-bodies-not-carried.md) | High | **Partly fixed.** Function declarations, call nodes and parameter coordinates are now carried; bodies are not. Measured over all 491 MSL models: calls appear in 156 of them. |

| [TOOLBUG-016](TOOLBUG-016-incidence-edges-lost-and-invented.md) | High | **Fixed.** Four separate ways the equation–variable incidence was wrong, each producing structural findings against models the compiler had proved balanced. Corpus findings 1324 → 63. |

| [TOOLBUG-017](TOOLBUG-017-divisor-reported-parameters-not-denominators.md) | High | **Fixed.** DivisorSan reported every parameter appearing inside a denominator without checking that the denominator could vanish. Found by independent review of the published reports. |

| [TOOLBUG-018](TOOLBUG-018-ir-lost-the-symbol-contract.md) | High | **Fixed.** The IR lowered every numeric declaration to an indistinguishable `Real`, so `constant`, `final` and `protected` were invisible and `pi` was a settable zero witness. `RbcSymbolContract` now carries variability, mutability, binding, dependencies and provenance. |

| [TOOLBUG-019](TOOLBUG-019-two-valued-divisor-classification.md) | Medium | **Fixed.** The divisor analysis could not say "I don't know": a path it could not decide was treated as reachable. Now three-valued, with 57% of all corpus divisions *proved* safe. |

| [TOOLBUG-020](TOOLBUG-020-zero-behaviour-was-decided-three-times.md) | High | **Fixed.** Three detectors each decided what zero meant for a parameter and disagreed; 1448 reports across ten component families followed. One shared contract now decides it, with provenance. The confirmed-defect count fell from 26 to 11 as a result. |

| [TOOLBUG-021](TOOLBUG-021-locations-named-a-basename.md) | Medium | **Fixed.** Locations were published as a basename, and four MSL files share `HollowCylinderAxialFlux.mo`; the documented verification command opened the wrong one. Locations now carry the path. |

| [TOOLBUG-022](TOOLBUG-022-a-violated-invariant-never-consulted-the-contract.md) | Medium | **Fixed.** The shared zero contract gated the "declaration permits zero" path and not the "declaration *is* zero" path, so a parameter the library ships at zero on purpose stayed in the 100%-precision stratum. |

| [TOOLBUG-023](TOOLBUG-023-a-tensor-checked-one-entry-at-a-time.md) | High | **Fixed.** An inertia tensor was checked one entry at a time against `> 0` (182 reports) and a resistance was judged by its SI quantity rather than its component (86 reports). The scalar tensor rule would also have passed a matrix with a negative eigenvalue. |

| [TOOLBUG-024](TOOLBUG-024-a-quantity-was-treated-as-an-intent.md) | High | **Fixed.** The declaration path asserted a physical intent from an SI quantity alone, on 638 declarations. Premise states are now carried end to end and an unestablished premise asks the author instead of accusing the model; nothing was suppressed, and source arithmetic outranks every declared intent. |

| [TOOLBUG-025](TOOLBUG-025-the-conserved-half-was-never-exported.md) | High | **Fixed.** Every exported connection carried the potential equality and never the flow balance, so no consumer could see what a node conserves. The artifact was self-consistent throughout. |

## Defects found while building the sanitizers

| ID | Component | Summary | Status |
|---|---|---|---|
| [TOOLBUG-010](TOOLBUG-010-divisorsan-misread-non-literal-min.md) | ModelSan | DivisorSan read `min=Modelica.Constants.eps` as no bound, manufacturing two confirmed findings against correct models | Fixed |
| [TOOLBUG-011](TOOLBUG-011-bitcode-cannot-encode-unary-plus.md) | Rumoca bitcode | unary plus had no v1 encoding, so an exported artifact failed its own import | Fixed |
| [TOOLBUG-012](TOOLBUG-012-connection-ids-not-dense.md) | Rumoca bitcode | connection ids were numbered before filtering, so 28 of 35 Clocked models exported artifacts that failed their own validator | Fixed |
| [TOOLBUG-014](TOOLBUG-014-structured-equations-not-exported.md) | Rumoca bitcode | array equation families are not exported, so the artifact under-reports the system; 1233 spurious structural findings | Reported |
