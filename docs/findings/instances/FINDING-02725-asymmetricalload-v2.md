# FINDING-02725: `transformerData.V2` in `AsymmetricalLoad`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.Transformers.AsymmetricalLoad` |
| **Reached as** | `transformerData.V2` |
| **Declaration** | `TransformerData.mo:9` |
| **Parameter** | `V2` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0147](../../site-reports/SITE-0147-v2-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | transformerData.V2 |
| `shape` | propagated |
| `path` | transformerData.V2 -> transformerData.V2ph |
| `declared_min` | None |
| `divisor_sites` | 6 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `TransformerData.mo:9` is reached by this model through
`transformerData.V2`, and the analysis reached it statically — no value has been observed
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
