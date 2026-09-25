# TOOLBUG-026: a stale binary decides the verdict

**Status:** open (three instances found the same day, none yet fixed)
**Found:** 2026-09-24, while re-verifying the MSL known-issues campaign.

## The defect

Nothing in this project pins the compiler a result was produced with. Every
layer resolves `rumoca` differently, and each resolver can silently pick a
binary that is older than the code under test. The result is not an error: it
is a *verdict*, recorded and published, that says working code is broken.

Three independent instances, all on the same afternoon:

| Where | Resolver | What it picked | The false verdict |
|---|---|---|---|
| Campaign run | `./target/debug/rumoca` | binary 7 min older than `cli.rs` | 11/11 cases `blocked` — no `--diagnostics-json` |
| `detection-native.json` | recorded `executable_sha256 1c1218b3…` | superseded build | MoistAir `blocked`, "no native detection is claimed" |
| ModelSan test suite | `shutil.which("rumoca")` (`compiler.py:11`) | `~/.cargo/bin/rumoca` **0.4.5** | 30 failures, `unexpected argument 'bitcode'` |

The third is the worst, because 0.4.5 predates the `bitcode` subcommand
entirely. The suite was not testing an old version of the feature; it was
testing a binary with no knowledge the feature exists, and reporting that as
30 red tests against current code.

## Why it matters here

This project's whole output is verdicts about other people's models. A
sanitizer that cannot establish which compiler produced its evidence cannot
distinguish "the model is wrong" from "my binary is old". Two of the three
instances above moved in the *pessimistic* direction — they made Rumoca look
less capable than it is, and one of them was already written into a published
evaluation document. A future instance could as easily move the other way.

## Fix

1. `compiler()` should prefer an in-tree `target/{debug,release}/rumoca` over
   `PATH`, and `RUMOCA` over both. PATH last, not first.
2. Assert a minimum version once at session start and fail with one clear
   message, rather than producing N identical downstream failures.
3. Every recorded campaign result already carries `executable_sha256`. Nothing
   *checks* it. A re-run against a different hash should refuse to be compared
   against the stored result without saying so.

## Regression

A test that runs the suite's `compiler()` with a doctored `PATH` containing an
old binary and asserts it still selects the in-tree build.
