# FINDING-04441: `world.defaultWidthFraction` in `MechanicalStructure`

| | |
|---|---|
| **Model** | `Modelica.Mechanics.MultiBody.Examples.Systems.RobotR3.Utilities.MechanicalStructure` |
| **Reached as** | `world.defaultWidthFraction` |
| **Declaration** | `package.mo:128` |
| **Parameter** | `defaultWidthFraction` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0028](../../site-reports/SITE-0028-defaultwidthfraction-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | world.defaultWidthFraction |
| `shape` | direct |
| `path` | world.defaultWidthFraction |
| `declared_min` | None |
| `divisor_sites` | 20 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `package.mo:128` is reached by this model through
`world.defaultWidthFraction`, and the analysis reached it statically — no value has been observed
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
