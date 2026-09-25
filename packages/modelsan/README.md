# ModelSan

ModelSan checks Modelica models using static analyses and observations from an explicitly selected execution backend. Findings retain the property, input configuration, source or backend identity, and observed evidence. Unsupported compilation and missing observations are coverage gaps. A typed compiler proof of an array-bounds violation is a model finding with its original source location.

## Check known upstream issues

The [known-issue campaign](../../examples/modelsan/known-msl-issues.json) exercises actual MSL APIs and includes non-triggering controls. It uses general behavioral contracts; the sanitizer contains no issue-number or model-name special cases.

From the repository root, with the existing Rumoca executable and cached MSL 4.1.0:

```sh
PYTHONPATH=packages/rumoca-bitcode:packages/modelsan python3 -m modelsan.cli contracts \
  examples/modelsan/known-msl-issues.json \
  --backend rumoca-source \
  --freeze-parameters \
  --source-root target/msl/ModelicaStandardLibrary-4.1.0 \
  --output target/modelsan-known-issues/native.json
```

The native source profile executes `rumoca sim` directly. It supports nominal runs and variable/failure observations, with backend names rather than invented canonical IDs. It rejects unsupported overrides and instrumentation requests. This is an explicit profile, not a silent fallback from the separate editable-bitcode backend.

Use `--backend rumoca` with the same options to compile, instrument and execute a saved equation artifact. Its runtime findings use the artifact's canonical identities. The campaign's `--freeze-parameters` option explicitly fixes declared parameter values during compilation; changing them requires recompilation. This permits pure constant evaluation of MoistAir's nonlinear inverse and reports its bounds defect before execution. Ordinary compilation keeps tunable parameters. The profile does not provide general runtime convergence-loop support.

OpenModelica is also an explicit backend:

```sh
PYTHONPATH=packages/rumoca-bitcode:packages/modelsan python3 -m modelsan.cli contracts \
  examples/modelsan/known-msl-issues.json --backend openmodelica \
  --library 'target/msl/ModelicaStandardLibrary-4.1.0/ModelicaServices 4.1.0/package.mo' \
  --library target/msl/ModelicaStandardLibrary-4.1.0/Complex.mo \
  --library 'target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/package.mo' \
  --output target/modelsan-known-issues/omc.json
```

Exit status is **0** when no violation was observed, **1** for observed violations, proven model rejection or execution failures, and **2** when any case is blocked, inconclusive or unobserved. An expected-failure benchmark must inspect the specific finding and its passing controls, not just assert a nonzero exit code. Reports include evidence, traces, coverage and execution/source fingerprints. `model-rejected` means the compiler proved a defect; it does not imply that a simulation ran.

## Behavioral contracts

`BehaviorSan` adds four reusable checks over real observations:

| Contract | Property |
|---|---|
| `equality` | Two synchronized signals agree within declared absolute/relative tolerance, e.g. a round trip restores the original value. |
| `periodic_pulse` | Output matches the configured period, start and duty cycle away from switching boundaries. |
| `sample_delay` | Output holds the previous sampled continuous input; required sample history must be observed. |
| `cardinality` | Observations require no more than the permitted number of output levels, accounting for declared observation uncertainty. |

Every contract requires an explicit origin and unique ID. It binds exact signal names chosen by the caller; it does not infer intent from names or units. Unknown, partial, unsynchronized or nonfinite evidence cannot establish a successful behavioral check. Temporal contracts additionally require ordered timestamps. Event boundaries are skipped where a timestamp cannot establish the event side. Cardinality tolerances define a possible-level interval around each reading; the minimum number of levels consistent with those intervals is compared to the limit.

Some OpenModelica clocked CSVs contain decreasing timestamps. The backend preserves their validated values as explicitly unordered observations, including original row numbers and reported times. Such a result has no temporal trace. Cardinality can use those values because its property is independent of order; pulse, delay and equality checks cannot. No timestamp sorting, jittering or inferred event order is applied.

A campaign JSON declares `schema: 1`, a source path relative to the JSON file, and cases containing `model` and `contracts`. For example:

```json
{
  "schema": 1,
  "source": "MyModel.mo",
  "cases": [{
    "model": "MyModel",
    "contracts": [{
      "kind": "equality",
      "contract_id": "state-round-trip",
      "origin": "My API: inverse(forward(x)) restores x",
      "actual": "recovered",
      "expected": "original",
      "atol": 1e-8,
      "rtol": 1e-7
    }]
  }]
}
```

Contracts are opt-in expectations, not automatic discovery of arbitrary physical correctness. The known-issue fixtures call the original MSL implementations. Their expectations are supplied to ModelSan, not inserted into MSL as assertions. Additional static/domain/range/physical sanitizers remain available through the Python registry and canonical bitcode pipeline; the contract CLI activates BehaviorSan, NumericSan and SolverSan without requiring a canonical model.

## Validation

Focused unit and backend tests:

```sh
RUMOCA="$PWD/target/debug/rumoca" PYTHONPATH=packages/rumoca-bitcode:packages/modelsan \
  python3 -m pytest packages/modelsan/tests -q
```

Actual known-issue detection gate (requires Rumoca, OpenModelica and the cached MSL):

```sh
MODELSAN_MSL_TESTS=1 RUMOCA="$PWD/target/debug/rumoca" \
  PYTHONPATH=packages/rumoca-bitcode:packages/modelsan \
  python3 -m pytest packages/modelsan/tests/test_known_msl_issues.py -q
```

The gate requires all six specific issue detections and five passing controls in each backend profile. Linux CI runs both native profiles with the cached MSL; missing prerequisites fail an enabled gate. Native and OpenModelica observations are separate results; this is not a compiler parity measurement or a 352-issue recall score. See the [upstream inventory](../../docs/evaluations/msl-upstream-open-issues-2026-09-24/README.md) for the broader scope and historical evaluation.

## Install

```sh
pip install -e packages/rumoca-bitcode -e packages/modelsan
```

This provides the same `modelsan contracts ...` entry point. Execution remains in the selected simulator; ModelSan does not implement a second Modelica evaluator.
