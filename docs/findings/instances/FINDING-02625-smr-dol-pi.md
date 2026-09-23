# FINDING-02625: `smr.pi` in `SMR_DOL`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL` |
| **Reached as** | `smr.pi` |
| **Declaration** | `PartialBasicInductionMachine.mo:117` |
| **Parameter** | `pi` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0012](../../site-reports/SITE-0012-pi-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | smr.pi |
| `shape` | product |
| `path` | smr.pi |
| `declared_min` | None |
| `divisor_sites` | 4 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `PartialBasicInductionMachine.mo:117` is reached by this model through
`smr.pi`, and the analysis reached it statically — no value has been observed
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
