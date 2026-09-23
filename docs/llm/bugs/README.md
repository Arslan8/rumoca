# Independent LLM audit of MSL 4.1.0

This directory contains a conservative, root-cause-level review of the local
Modelica Standard Library 4.1.0 snapshot. It reports **five confirmed contract
bugs affecting seven MSL classes**. Counts are root causes, not every model that
can instantiate the affected component.

| ID | Affected class | Trigger | Failure | Confidence |
|---|---|---|---|---|
| [LLM-BUG-001](LLM-BUG-001-firstorder-zero-time-constant.md) | `Modelica.Blocks.Continuous.FirstOrder` | `T=0` | direct division by zero | two-tool reproduction |
| [LLM-BUG-002](LLM-BUG-002-criticaldamping-zero-order.md) | both `CriticalDamping` implementations | `n=0` | zero-length state indexed at `1`; `1/n` also undefined | two-tool reproduction |
| [LLM-BUG-003](LLM-BUG-003-thyristor-zero-current-parameters.md) | `Modelica.Electrical.Analog.Semiconductors.Thyristor` | `ITM=0` or `IH=0` | protected resistance binding divides by zero | two-tool reproduction |
| [LLM-BUG-004](LLM-BUG-004-signalpwm-zero-frequency.md) | `Modelica.Electrical.PowerConverters.DCDC.Control.SignalPWM` | `f=0` | sample period and carrier timings divide by zero | OMC execution plus Rumoca source rejection |
| [LLM-BUG-005](LLM-BUG-005-comparetransformers-zero-turns-ratio.md) | `CompareTransformers` and `IdealTransformer` contract | `n=0` | derived transformer values divide by zero | OMC execution plus Rumoca source rejection |

## Promotion rule

A report appears in this table only when all of the following held:

1. The public parameter declaration does not exclude the exact witness.
2. The failing operation is present in MSL source, rather than introduced by a
   compiler's solved representation.
3. A paired nominal probe succeeds under OpenModelica using the pinned local
   MSL 4.1.0 package.
4. The otherwise identical invalid probe fails for the source-owned operation.
5. Rumoca independently either reproduces the runtime failure or rejects the
   exact MSL source expression while its nominal probe translates.
6. The component documentation does not define the witness as a supported
   sentinel or ideal limit.

This is deliberately stricter than treating a satisfiable static denominator
as a bug. [Method and limitations](METHOD.md) records the remaining uncertainty.

## Reproduction

The paired models are in [`repro/`](repro/). Run all OpenModelica controls from
the repository root without leaving generated simulation files in the tree:

```sh
RUMOCA_REPO="$PWD" sh -c 'eval_dir=$(mktemp -d); cd "$eval_dir" && CC=gcc omc "$RUMOCA_REPO/docs/llm/bugs/repro/run_omc.mos"'
```

The script prints `MSL 4.1.0`, then the nominal and invalid result for every
report. Each report also includes its focused Rumoca command.

## Evaluation identity

- MSL: `4.1.0`, loaded from `target/msl/ModelicaStandardLibrary-4.1.0`
- OpenModelica: `1.27.0~dev.beta.2`
- Rumoca source revision: `a49b89dd99623de5e585adf8a93a8d543020157b`
- Evaluation date: 2026-09-16

[Machine-readable index](index.csv)
