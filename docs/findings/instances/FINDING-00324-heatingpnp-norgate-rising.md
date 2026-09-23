# FINDING-00324: `V2.signalSource.rising` in `HeatingPNP_NORGate`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate` |
| **Reached as** | `V2.signalSource.rising` |
| **Declaration** | `Sources.mo:894` |
| **Parameter** | `rising` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0130](../../site-reports/SITE-0130-rising-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | V2.signalSource.rising |
| `shape` | direct |
| `path` | V2.signalSource.rising |
| `declared_min` | 0.0 |
| `divisor_sites` | 1 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `Sources.mo:894` is reached by this model through
`V2.signalSource.rising`, and the analysis reached it statically — no value has been observed
breaking anything here.

The fix is at the declaration, not in this model. Other models reaching the same
declaration are separate files; the fix site groups them.

| Tier | Evidence | Where |
|---|---|---|
| confirmed | fails in two independent tools | [`INSTANCES.md`](../../verified%20bugs/INSTANCES.md) |
| **candidate** | **static analysis reached it** | **here** |
| latent | a declaration permits it | [`declaration-sites/`](../../declaration-sites/README.md) |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
