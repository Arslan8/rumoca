# FINDING-02807: `transformerData.C1` in `IMC_Transformer`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer` |
| **Reached as** | `transformerData.C1` |
| **Declaration** | `TransformerData.mo:7` |
| **Parameter** | `C1` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0105](../../site-reports/SITE-0105-c1-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | transformerData.C1 |
| `shape` | propagated |
| `path` | transformerData.C1 -> transformerData.V1ph |
| `declared_min` | None |
| `divisor_sites` | 6 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `TransformerData.mo:7` is reached by this model through
`transformerData.C1`, and the analysis reached it statically — no value has been observed
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
