# Bitcode linker verification — 2026-09-23

Implementation base: `c8c6a5960f91d55843f1d68668fcfaf3affff033`, plus the
linker and connector-hardening changes committed with this record. No cohort
parity claim is made by this record.

## Focused evidence

| Check | Result |
|---|---|
| `cargo build -p rumoca --bin rumoca --offline` | Passed |
| `cargo test -p rumoca-bitcode -p rumoca-phase-solve --lib --offline --quiet` | 53 bitcode tests and 110 lowering tests passed |
| `python3 -m unittest discover -s new_inst -p 'test_*.py' -q` | 24 passed: 9 linker acceptance tests plus 15 execution regressions |
| `python3 -m pytest packages/modelsan/tests/test_sdk_builder.py -q` | 8 passed |
| Strict Clippy for `rumoca-phase-solve --lib` | Passed |
| Clippy for `rumoca-bitcode --lib --tests` | Blocked by 73 existing diagnostics in each target; filtered diagnostics report no new linker-file errors |
| New Rust linker files: rustfmt check; working diff: whitespace check | Passed |

Cargo used `CARGO_BUILD_JOBS=4 RUST_TEST_THREADS=4 RAYON_NUM_THREADS=4`.
Python used `PYTHONPATH=packages/rumoca-bitcode:new_inst` and
`RUMOCA=/data/mrumoca/rumoca/target/debug/rumoca` for native subprocess tests.
The full ModelSan suite and full workspace suite were not rerun: these checks
target linking, builder compatibility, and the replay correction below.

## First-divergence regression discovered during linking

The standalone SDK fixture `der(x) = -k*x` failed even before linking:
`continuous.implicit_row_targets expected 0 rows, got 1`. Two linked copies
failed with `got 2`. The failure was in public execution reconstruction, not
equation ID remapping or numerical integration: replay allocated target entries
from the Y variable count, while the canonical checker expected the implicit
block's output count. A pure explicit ODE has no implicit residual outputs.

The adapter now obtains that count from `ComputeBlock::output_count`; the
canonical validator is unchanged. The native regression runs independent and
linked ODEs with different rates/initial values and compares all 11 published
samples against both independent native runs and analytic exponential decay
(absolute error tolerance `1e-7`). A compiled Modelica fixture passes the same
end-to-end check. Existing thermal/execution tests remain green.

## Other proof boundaries

The fixed Tier 1 canary was attempted once with:

```bash
CARGO_BUILD_JOBS=4 RUST_TEST_THREADS=4 RAYON_NUM_THREADS=4 CARGO_NET_OFFLINE=true \
  timeout 240s cargo xtask verify msl-parity \
  --sim-targets-file infra/verification/msl-canary-20.json
```

It exited `124` at the outer 240-second limit while building the separate
`msl-fast` worker/test binaries, before model evaluation or trace comparison.
This is an infrastructure/cold-build timeout, not a passing canary and not a
model failure classification. The canary delta is **unmeasured**; the Tier 1
canary obligation remains open. No full 566-model Tier 2 sweep was run in this
bounded linker task. Full parity is **unmeasured** and no baseline was promoted.

The cross-table Rust fixture checks relocation only; it intentionally includes
metadata whose types/roles do not constitute a runnable physical model. Native
ODE and thermal tests separately prove reconstruction and execution. Preserving
event/array/function metadata is not a claim of runtime support for those
features in execution v1. Linking never removes closed-boundary equations.

See [the user guide](../docs/bitcode-linking.md) for behavior and invocation.

## Native connection hardening follow-up

The same working change now includes mandatory validation of declared scalar
connection contracts and a complete-contract audit flag. The original bypass
was reproduced: a flow residual replaced by `0.0` passed native strict checking.
The regression now fails with a connection-law error, including when the helper
is bypassed by raw JSON/CBOR edits. See
[the root-cause and contract document](../docs/connector-validation.md).

| Follow-up check | Result |
|---|---|
| Native acceptance discovery (`test_*.py`) | 38 passed: 14 native connection-validation tests, 9 linker tests, 15 execution regressions; includes a 21-case corruption matrix and entry-point/encoding subtests |
| SDK builder pytest regressions | 8 passed |
| Bitcode Rust unit tests | 53 passed |
| Original saved thermal artifacts, scales 1 and 2 | Both pass native strict checking with `--connections`, including existing executable freshness checks |
| Bitcode Clippy lib and test targets | Still 73 pre-existing errors per target; no diagnostics in new linker/connector-validation modules |
| New Rust files rustfmt and working diff whitespace | Passed |

The canary was attempted again after hardening with the same fixed target list,
fixed concurrency and offline Cargo, bounded by `timeout 300s`. This attempt
failed during the optimized worker/test build (Cargo exit 101; xtask exit 1),
before model evaluation/comparison. The setup report records 48.946 seconds at
`target/msl/results/msl_cargo_setup_timing.md`. This is a build-gate failure, not
a canary pass; there is still no measured canary delta or cohort parity result.
The failure was traced to the RK45-only `NativePublication` helper and imports
being compiled in non-RK45 builds. They now carry the same feature gate as their
caller. The non-RK45 `solver-diffsol` check passes after that correction.

A final canary retry built successfully (47.72 seconds) and evaluated all 20
targets: 11 compiled, 9 failed ToDae; of 11 simulation attempts, 8 completed and
3 failed solve-IR checks. These are completion counts, **not parity** and not a
measured regression delta. OMC reference generation reached report preparation,
but its npm dependency installation failed because `registry.npmjs.org` could
not resolve. Trace comparison did not run; the wrapper correctly exited 1 with
**parity unmeasured**. No baseline was promoted, and no full 566-model sweep was
run. The Tier 1 parity obligation remains open. Current detailed artifacts are
under `target/msl/results/` (untracked), notably `msl_results.json`,
`msl_cargo_setup_timing.md`, and `msl_parity_timing.md`.

The 110 `rumoca-phase-solve` unit tests also passed again after hardening.
