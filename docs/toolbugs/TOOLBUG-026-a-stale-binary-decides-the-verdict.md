# TOOLBUG-026: a stale binary decides the verdict

**Status:** fixed 2026-09-25
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

1. **Done.** `compiler()` now resolves `RUMOCA`, then the working copy's own
   `target/{debug,release}/rumoca`, then `PATH`. An explicit choice beats a
   discovered one, and the build whose source sits beside the package beats
   whatever a shell happens to find.
2. **Done.** `MINIMUM_VERSION` is checked once, and a compiler below it is
   refused by name and version — "every rumoca found is older than 0.10.0:
   /home/…/.cargo/bin/rumoca is 0.4.5" — instead of producing N downstream
   failures that each blame something else. An executable that reports no
   parseable version is accepted, because unknown is not the same as too old.
3. **Not done.** Every recorded campaign result carries `executable_sha256` and
   nothing checks it. A re-run against a different hash should refuse silent
   comparison against the stored result. This remains open, and it is the
   instance that bit hardest: the 6/6 detection claim retracted in
   [TOOLBUG-027](TOOLBUG-027-tests-and-docs-assert-limitations-that-were-fixed.md)
   came from one run against one build and was repeated in three documents
   before anything re-ran it.

## Regression

`packages/modelsan/tests/test_compiler_resolution.py`, five cases: a doctored
`PATH` holding a 0.4.5 does not shadow the working copy; an explicit `RUMOCA`
still wins; a too-old compiler is refused by name and version; an executable
with no parseable version is not refused; and the probe reads the real
compiler's version.
