# FINDING-02276: `smeeData.xdTransient` in `SMEE_Generator`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator` |
| **Reached as** | `smeeData.xdTransient` |
| **Declaration** | `SynchronousMachineData.mo:29` |
| **Parameter** | `xdTransient` |
| **Claim** | a divisor vanishes when two parameters are equal |
| **Kind** | `divisor-zero-when-parameters-equal` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0273](../../site-reports/SITE-0273-xdtransient-divisor-zero-when-parameters-equal.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | smeeData.xdTransient |
| `shape` | relational |
| `path` | smeeData.xdTransient |
| `declared_min` | None |
| `divisor_sites` | 2 |
| `partner` | smeeData.xdSubtransient |
| `note` | zero when the two are equal; min/max cannot express a constraint between two parameters, so an assertion is the only mechanism |


## What this is

One occurrence. The declaration at `SynchronousMachineData.mo:29` is reached by this model through
`smeeData.xdTransient`, and the analysis reached it statically — no value has been observed
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
