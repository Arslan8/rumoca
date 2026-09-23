# Native demonstration results

Generated and independently checked on 2026-09-23 from the current working
tree. These are native RK45 runs of saved execution RBC, not oracle fixtures.

| Equation rewrite | Executable artifact | Trace manifest | Oracle result |
|---|---|---|---|
| scale = 1 | [saved program](thermal-scale-1/04-instrumented.rbc) | [manifest](thermal-scale-1/traces/manifest.json) | 4 connectors × 51 rows; analytic temperature/flow and energy checks pass |
| scale = 2 | [saved program](thermal-scale-2/04-instrumented.rbc) | [manifest](thermal-scale-2/traces/manifest.json) | 4 connectors × 51 rows; analytic temperature/flow and energy checks pass |

The `01`, `02`, `03`, `04` artifacts in each run preserve the original equations,
rewritten equations, uninstrumented execution and instrumented execution.

For scale 2, native initial records were:

| Connector | Temperature (K) | Flow into owner (W) | CSV |
|---|---:|---:|---|
| hot.port | 350 | -100 | [records](thermal-scale-2/traces/connector-0000.csv) |
| link.a | 350 | 100 | [records](thermal-scale-2/traces/connector-0001.csv) |
| link.b | 300 | -100 | [records](thermal-scale-2/traces/connector-0002.csv) |
| cold.port | 300 | 100 | [records](thermal-scale-2/traces/connector-0003.csv) |

Recheck these outputs without importing the SDK:

```bash
python3 new_inst/check_thermal_csv.py new_inst/results/thermal-scale-1/traces --conductance-scale 1
python3 new_inst/check_thermal_csv.py new_inst/results/thermal-scale-2/traces --conductance-scale 2
```

The acceptance suite separately compares uninstrumented and instrumented native
results exactly for both scales, then tests intentional executable behavior
changes and stale derivations. Passing these tests establishes this profile's
behavior; it is not evidence that every MSL model fits the profile.
