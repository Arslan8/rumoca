# FINDING-03901: `l_pole` in `AdvancedSolenoid`

| | |
|---|---|
| **Model** | `Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid` |
| **Reached as** | `l_pole` |
| **Declaration** | `AdvancedSolenoid.mo:21` |
| **Parameter** | `l_pole` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0369](../../site-reports/SITE-0369-l-pole-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | l_pole |
| `shape` | propagated |
| `path` | l_pole -> g_mFeArm.l |
| `declared_min` | None |
| `divisor_sites` | 2 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `AdvancedSolenoid.mo:21` is reached by this model through
`l_pole`, and the analysis reached it statically — no value has been observed
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
