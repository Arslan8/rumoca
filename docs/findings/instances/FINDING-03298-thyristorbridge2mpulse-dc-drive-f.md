# FINDING-03298: `pulse2.f` in `ThyristorBridge2mPulse_DC_Drive`

| | |
|---|---|
| **Model** | `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive` |
| **Reached as** | `pulse2.f` |
| **Declaration** | `VoltageBridge2mPulse.mo:6` |
| **Parameter** | `f` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0559](../../site-reports/SITE-0559-f-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | pulse2.f |
| `shape` | propagated |
| `path` | pulse2.f -> pulse2.fCut -> pulse2.twomPulse.filter[1].fCut -> pulse2.twomPulse.filter[1].firstOrder.T |
| `declared_min` | None |
| `divisor_sites` | 18 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `VoltageBridge2mPulse.mo:6` is reached by this model through
`pulse2.f`, and the analysis reached it statically — no value has been observed
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
