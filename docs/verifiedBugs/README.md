# Report verification — 2026-09-15–16

This audit accounts for **all 6,079 issue reports** in `docs/v2/bugs`: 26 BUG claims, 5,142 FINDING candidates and 911 DECL census entries. It does **not** certify all candidates as defects. Originals are preserved. This directory supersedes neither history nor upstream status; in particular, it does not inherit the verdicts in `docs/verified bugs` (with a space).

| Verdict | Reports | Browse |
|---|---:|---|
| Verified defect / unsafe unguarded calculation | 503 | [Verified reports](confirmed.md) |
| False positive for the stated claim | 3304 | [Reasons and evidence](false-positives.md) |
| Unresolved — not called real or fake | 2272 | [Remaining evidence gaps](unresolved.md) |
| Total | 6079 | [Filterable CSV](index.csv) · [JSON](index.json) |

Counts are **report instances**, not unique bugs. The grouped table below prevents counting the same declaration repeatedly. Confirmed includes source-proved domain/guard defects on invalid input, not claims that default simulations fail. False positive means the specific claim is refuted, not that every use of the component is bug-free. **Unresolved work remains**; absent evidence is never called a false positive.

## Verified root-cause groups

| Group | Reports | Proposed-fix location |
|---|---:|---|
| [Braking example fails to propagate positive speed-scale bounds](groups/braking-speed-scales.md) | 4 | Per-report source, fix proposal and regression cases |
| [Control-circuit time constants create zero divisions](groups/control-design.md) | 3 | Per-report source, fix proposal and regression cases |
| [CriticalDamping accepts zero order then divides by it](groups/critical-damping-order.md) | 8 | Per-report source, fix proposal and regression cases |
| [Filter cutoff frequency divides by zero](groups/cutoff-frequency.md) | 2 | Per-report source, fix proposal and regression cases |
| [Zero nominal speed makes DC-machine scaling undefined](groups/dc-data-nominal-speed.md) | 19 | Per-report source, fix proposal and regression cases |
| [Zero nominal excitation flux divides the turns-ratio calculation](groups/dc-machine-flux-scale.md) | 15 | Per-report source, fix proposal and regression cases |
| [SwitchedRLC divides directly by unconstrained resistance](groups/example-rlc-resistance.md) | 1 | Per-report source, fix proposal and regression cases |
| [FirstOrder divides by an unconstrained zero time constant](groups/first-order-time-constant.md) | 21 | Per-report source, fix proposal and regression cases |
| [Zero medium specific heat capacity enters an unguarded division](groups/fluid-medium-cp.md) | 23 | Per-report source, fix proposal and regression cases |
| [Zero medium density enters an unguarded division](groups/fluid-medium-rho.md) | 172 | Per-report source, fix proposal and regression cases |
| [Zero flux-tube area makes the model undefined](groups/flux-area.md) | 6 | Per-report source, fix proposal and regression cases |
| [Zero flux-tube length divides by zero](groups/flux-length.md) | 10 | Per-report source, fix proposal and regression cases |
| [Zero magnetic normalization scale divides by zero](groups/flux-normalization-scale.md) | 16 | Per-report source, fix proposal and regression cases |
| [IdealPump permits zero nominal speed then divides by it](groups/ideal-pump-speed.md) | 2 | Per-report source, fix proposal and regression cases |
| [Inactive material data still enter an unguarded division](groups/inactive-flux-normalization.md) | 9 | Per-report source, fix proposal and regression cases |
| [Zero nominal frequency divides induction-machine data](groups/induction-data-frequency.md) | 41 | Per-report source, fix proposal and regression cases |
| [Equal machine reactances divide by zero](groups/machine-reactance-equality.md) | 6 | Per-report source, fix proposal and regression cases |
| [Zero MultiBody visualization fraction divides geometry by zero](groups/multibody-visual-scale.md) | 34 | Per-report source, fix proposal and regression cases |
| [Multivibrator capacitance formula has zero divisors](groups/multivibrator-design.md) | 11 | Per-report source, fix proposal and regression cases |
| [OneWayValve divides by unconstrained nominal scales](groups/one-way-valve-scales.md) | 2 | Per-report source, fix proposal and regression cases |
| [Der circuit has an unguarded design denominator](groups/opamp-design-der.md) | 6 | Per-report source, fix proposal and regression cases |
| [Derivative circuit has an unguarded design denominator](groups/opamp-design-derivative.md) | 5 | Per-report source, fix proposal and regression cases |
| [FirstOrder circuit has an unguarded design denominator](groups/opamp-design-firstorder.md) | 9 | Per-report source, fix proposal and regression cases |
| [Integrator circuit has an unguarded design denominator](groups/opamp-design-integrator.md) | 8 | Per-report source, fix proposal and regression cases |
| [PI circuit has an unguarded design denominator](groups/opamp-design-pi.md) | 6 | Per-report source, fix proposal and regression cases |
| [Equal op-amp supplies divide by zero](groups/opamp-supply-span.md) | 2 | Per-report source, fix proposal and regression cases |
| [LC oscillator design divides by zero](groups/oscillator-design.md) | 10 | Per-report source, fix proposal and regression cases |
| [SpacePhasor permits zero turns ratio then divides by it](groups/space-phasor-turns-ratio.md) | 22 | Per-report source, fix proposal and regression cases |
| [Tank permits a direct zero divisor](groups/tank-zero-divisor.md) | 2 | Per-report source, fix proposal and regression cases |
| [Example waveform timing divides by zero frequency](groups/trapezoid-frequency.md) | 19 | Per-report source, fix proposal and regression cases |
| [Vehicle exposes zero regularization speed to reciprocal equations](groups/vehicle-regularization-speed.md) | 9 | Per-report source, fix proposal and regression cases |

## What changed from the earlier “confirmed” list

All 26 BUG entries were checked with nominal execution, runtime overrides, source-level parameter modifications, and final-evaluated recompilation in OpenModelica. Some storage-zero override failures disappear when the model is retranslated. Others disappear after incompatible fixed initial conditions are relaxed; the zero is retained. Those failures do not justify globally banning zero mass, inertia, capacitance or inductance. The controls and full results are retained.

The direct arithmetic issues are separate: waveform/design frequencies, op-amp supply equality, magnetic geometry, design resistances/time constants, and machine reactance equalities. Inactive magnetic material normalization remains unconditionally evaluated in source; OpenModelica may optimize it away, so it is explicitly documented as compiler-dependent rather than falsely called a robust two-tool active-physics failure.

## Coverage and limitations

- Fresh Rumoca compile/nominal-run attempts: **266 distinct models**; outcomes: `{'tool-error': 179, 'clean': 43, 'reported-failure': 44}`.
- After clean baselines: **333 distinct runtime probes**; outcomes: `{'reported-failure': 168, 'clean': 165}`. These are evidence, not automatic verdicts.
- Independent OpenModelica model batches: **21**, plus initialization controls and projections using the actual library record. Nominal and every wrapper result are parsed individually; an omc process exit code of zero alone is not success.
- Source-resolved declarations and exact snapshots are retained, including compiler-provided effective bounds. Repeated findings reuse narrow, reviewed source proofs; no blanket “Ideal”, “Spice3”, or missing-min rule was used.
- The current bitcode runtime cannot simulate many nominal models (for example unsupported expression forms). Those blocked claims remain unresolved unless a separate source proof establishes/refutes them. No claim of exhaustive behavioral verification is made.
- The test horizon is 0–0.5 s, not an exhaustive exploration of all events, all parameter combinations or long-run stability. Declaration-only entries do not provide a complete executable model.
- For equality reports the witness is the partner value, not automatically zero. A nonzero-sum denominator is analyzed as a whole; existing assertions and unreachable branches matter.
- No library/compiler fixes were applied. Proposed fixes are specific to the actual design/geometry/domain layer, not blanket stricter bounds on SI types.

## Reproduce and inspect

Run from the repository root, with the existing Rumoca binary, Python bitcode package and GCC-backed OpenModelica available:

```sh
python3 docs/verifiedBugs/audit.py --jobs 4
python3 docs/verifiedBugs/check_translation.py
python3 docs/verifiedBugs/check_additional.py
python3 docs/verifiedBugs/check_controls.py
python3 docs/verifiedBugs/build_reports.py
```

`audit.py` resumes existing per-model evidence; it does not silently refresh cached results after a source/binary change. For a new revision use a fresh evidence location/archive the old run first. Every JSON evidence file retains exact commands, return codes, timeout status and output SHA-256/byte counts; repetitive compile logs are bounded to 32 KiB while simulation diagnostics remain complete. The source wrappers and `.mos` scripts are embedded in OpenModelica evidence; transient executables/bitcode live under `target/bug-review-20260915`.

[Input inventory with hashes](inventory.json) · [Source snapshot manifest](evidence/source-manifest.json) · [Environment](evidence/environment.json) · [Validation](validation.json)
