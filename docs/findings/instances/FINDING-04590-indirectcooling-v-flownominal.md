# FINDING-04590: `outerPipe.V_flowNominal` in `IndirectCooling`

| | |
|---|---|
| **Model** | `Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling` |
| **Reached as** | `outerPipe.V_flowNominal` |
| **Declaration** | `SimpleFriction.mo:9` |
| **Parameter** | `V_flowNominal` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0057](../../site-reports/SITE-0057-v-flownominal-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | outerPipe.V_flowNominal |
| `shape` | direct |
| `path` | outerPipe.V_flowNominal |
| `declared_min` | None |
| `divisor_sites` | 1 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `SimpleFriction.mo:9` is reached by this model through
`outerPipe.V_flowNominal`, and the analysis reached it statically — no value has been observed
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
