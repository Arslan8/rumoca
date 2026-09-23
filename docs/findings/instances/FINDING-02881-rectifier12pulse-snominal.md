# FINDING-02881: `transformerData2.SNominal` in `Rectifier12pulse`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.Transformers.Rectifier12pulse` |
| **Reached as** | `transformerData2.SNominal` |
| **Declaration** | `TransformerData.mo:16` |
| **Parameter** | `SNominal` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0104](../../site-reports/SITE-0104-snominal-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | transformerData2.SNominal |
| `shape` | propagated |
| `path` | transformerData2.SNominal -> transformerData2.I1ph |
| `declared_min` | None |
| `divisor_sites` | 8 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `TransformerData.mo:16` is reached by this model through
`transformerData2.SNominal`, and the analysis reached it statically — no value has been observed
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
