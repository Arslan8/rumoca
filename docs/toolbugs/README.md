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
| [BUG-001](BUG-001-comprehension-in-for-equation-panic.md) | High | `rumoca-phase-dae` | Process abort on a comprehension in an algorithm, `when`, `assert` or `for`. Root cause: `all_model_expressions` walks 3 of 9 expression-bearing fields; 4 of its 5 other callers each patch around that differently. |
| [BUG-004](BUG-004-record-array-destructured-without-subscript.md) | Medium | `rumoca-phase-flatten` | Blocks all of `QuasiStatic.Polyphase`. |
| [BUG-007](BUG-007-dae-drops-predefined-enum-in-assert.md) | Medium | `rumoca-phase-dae` | 3-argument `assert(..., AssertionLevel.x)` unusable; 27 uses across 7 MSL files. |
| [LIMITATION-001](LIMITATION-001-index-reduction-drops-fixed-start.md) | — | `rumoca-phase-structural` | Correct, deliberate refusal; costs 2 MSL examples. |
| [LIMITATION-002](LIMITATION-002-no-solver-tolerance-control.md) | — | `compile-bitcode --simulate` | No `--rtol`/`--atol`, so the trajectory-differential detector cannot use a tight threshold. |

## In this project's own code

Both found by running the sweep against real MSL rather than hand-written
fixtures, and both were the same shape — export and import disagreeing, which
no test of either side alone could see.

| ID | Severity | Status |
|---|---|---|
| [BUG-008](BUG-008-bitcode-enumeration-round-trip.md) | High | **Fixed.** Enumerations were exported as integers, so import rejected its own output. |
| [BUG-009](BUG-009-bitcode-omits-discrete-definitions.md) | High | **Fixed.** No field existed for MLS Appendix B.1c definitions, so any discrete-valued variable broke round-trip. Affected every Boolean produced by a comparison. |

Bitcode tests: 29 passing, was 23. Round-trip audit over 60+ construct probes:
0 export-but-cannot-import, down from 9 models.
