# Independent MSL issue recall: fresh current-tool evaluation

**Result: standalone static analysis identifies the exact reported zero witness
for 5/7 variants (4/5 root-cause reports).** It produces unresolved candidates
for the other two, not confirmed detections. All seven have a matching zero
fuzz hint. Native runtime verification is substantially narrower: only three
nominal variants run cleanly through ModelSan, and only `FirstOrder` produces
the exact reached-zero-denominator diagnostic. The two Thyristor triggers
produce a generic non-finite failure, without an operation-level observation.

This evaluates the pre-existing [five independent reports](../../llm/bugs/README.md),
not the sanitizer's own generated findings. Seven rows are witness variants:
the two CriticalDamping implementations and the two Thyristor currents are
separate rows. `IdealTransformer` occurs inside the transformer example; this
is not an additional standalone execution test. These targeted parameter-domain
reports are **not a representative recall benchmark for all MSL bug classes**.

## Results table

All seven nominal sources compile with the current compiler and
`--no-fold-parameter-bindings`. Fresh OpenModelica controls succeed nominally and
fail on the exact source trigger in **7/7 pairs**. OMC is an independent failure
oracle here, not a trace-parity measurement.

| Original issue / exact witness | Current static result for that witness | Current ModelSan runtime pair | Exact-trigger source compilation | Why detection or verification is limited |
|---|---|---|---|---|
| [FirstOrder](../../llm/bugs/LLM-BUG-001-firstorder-zero-time-constant.md), `dut.T=0` | HIGH `divisor-reachable-zero`; DomainSan and DivisorSan zero hints | Nominal success; zero fails; **DomainSan records divisor 0 at internal evaluation time 0** | Compiles; exact source also fails at runtime | Detected. Native anchor identifies the execution instruction, not a canonical source expression. |
| [Blocks CriticalDamping](../../llm/bugs/LLM-BUG-002-criticaldamping-zero-order.md), `dut.n=0` | MEDIUM `divisor-zero-unresolved`; correct zero hints | Nominal **backend error**: missing requested array column `dut.x`; zero override non-finite failure is not a valid pair | **ET009**, `x[1]` outside dimension size 0 | Boolean guard reasoning, array observations, structural source-rebuild campaign. |
| [Clocked utility CriticalDamping](../../llm/bugs/LLM-BUG-002-criticaldamping-zero-order.md), `dut.n=0` | Same unresolved result and hints | Same array-observation gap | **ET009**, `x[1]` outside dimension size 0 | Same gaps; distinct implementation regression. |
| [Thyristor](../../llm/bugs/LLM-BUG-003-thyristor-zero-current-parameters.md), `dut.ITM=0` | HIGH `divisor-reachable-zero`; correct hints | Nominal success; zero non-finite failure, **SolverSan only**, no native domain fault | **ED019**, `dut.Ron`: division by zero | Parameter-binding evaluation is outside the instrumented Solve-row domain hooks. |
| [Thyristor](../../llm/bugs/LLM-BUG-003-thyristor-zero-current-parameters.md), `dut.IH=0` | HIGH `divisor-reachable-zero`; correct hints | Nominal success; zero non-finite failure, **SolverSan only**, no native domain fault | **ED019**, `dut.Roff`: division by zero | Same pre-solve domain-observation gap. |
| [SignalPWM](../../llm/bugs/LLM-BUG-004-signalpwm-zero-frequency.md), `dut.f=0` | HIGH `divisor-reachable-zero`; correct hints | **Preparation blocked**: unsupported `string_conversion` expressions 172 and 177 in bitcode v1 | **ED019**, `dut.zeroOrderHold.samplePeriod=1/f`: division by zero | Bitcode expression support; pipeline currently discards available static analysis when runtime preparation fails. |
| [CompareTransformers](../../llm/bugs/LLM-BUG-005-comparetransformers-zero-turns-ratio.md), `n=0` | HIGH `divisor-reachable-zero`; correct hints | Nominal and zero both fail: **coordinate names an unknown variable**; cannot attribute this failure to the witness | **ED019**, `L2sigma`: division by zero | Canonical coordinate/import completeness; correct tool-failure classification. |

Compiler rejection is not credited as a sanitizer finding. Likewise, an
unrelated HIGH finding such as `CriticalDamping.alpha=0` does not earn detection
credit for the reported `n=0` structural issue. Duplicate expression findings
are not counted as extra recovered issues.

## What to implement, in practical priority order

| Priority | Change | Concrete regression from this run | Required result |
|---|---|---|---|
| 1 | Run static analyses independently of backend preparation; separate model availability from runtime capability | SignalPWM has a valid static `dut.f=0` finding, but actual `Pipeline.run` exits with only a network coverage notice | Preserve the static finding and report runtime refusal separately. |
| 2 | Typed Boolean guard evaluation in the existing divisor engine | Both CriticalDamping artifacts retain `dut.normalized=True`, but the environment drops Boolean values and guard truth accepts only binary relations | Prove the true branch for the declared Boolean binding; retain UNKNOWN when genuinely undetermined; test false branch and `not`/`and`/`or`. |
| 3 | Preserve structural dependency contracts and add an explicit source-modification/recompile campaign | Both `dut.n` declarations are exported `tunable=true`, without `contract.structural`, despite sizing `dut.x[n]`; `--param dut.n=0` is accepted against the already-sized artifact | Reject same-artifact structural overrides; rebuild the real source for `n=0`, classify ET009 as witness-specific elaboration failure, and keep nominal `n=2` as the control. |
| 4 | Scalar-element observations for array variables | CriticalDamping's trace contains `source.y`, `dut.u`, `dut.y`, but **no `dut.x` observations** although requested | Emit/map every requested array element with canonical identity and complete synchronization. Never fill missing elements with fabricated values. |
| 5 | Native typed domain diagnostics for parameter bindings and starts, before Solve evaluation | Thyristor ITM/IH fail before any Solve-row domain observation; `faults=[]` and `unobserved_evaluations=0` | Preserve a typed denominator-zero cause and source/canonical identity from the owning evaluator; indicate pre-solve coverage separately. No regex claim that an empty fault list proves safety. |
| 6 | Complete current bitcode expression/coordinate support and distinguish importer failures from model failures | PWM's `string_conversion`; transformer fails even **without ModelSan instrumentation** | Support the real expressions/coordinates or fail as BACKEND_ERROR. Do not introduce reduced surrogate models and call these original cases supported. |

The first two changes reuse analysis that already exists; they do not require a
new generic sanitizer. Structural array safety is a separate analysis problem
from a scalar denominator: proving `1/n` safe does not prove `x[1]` exists.
Retain dimension dependencies/index obligations before elaboration if the tool
is to infer the missing `n>=1` contract from nominal bitcode alone.

### Discriminating evidence

The additional [gap-check script](independent-check-gaps.py) confirms:

- `Pipeline.run` on the PWM artifact returns `backend could not build the
  model` before invoking static analyzers. The same model analyzed directly
  produces the exact `dut.f=0` static finding.
- The CriticalDamping raw binding for `dut.normalized` is `True`; the divisor
  environment's declared value is absent. Thus the guard is not missing from
  the IR in this example—the consumer loses it.
- CriticalDamping's `dut.n` is exported tunable and not marked structural;
  `dut.x` retains `scalar_count=2`. An override cannot retroactively rebuild the
  source's zero-length array. It is not equivalent to the actual bad model.
- The transformer command without any trace instrumentation still emits
  `coordinate names an unknown variable`. Therefore ModelSan's observation pass
  alone is not the explanation. The current backend incorrectly normalizes
  this as a model `failed`/SolverSan failure rather than a tool error.
- For the failing Thyristor overrides the diagnostic file exists but contains
  no domain faults and zero observed/omitted-row evidence. This is a pre-solve
  evaluation coverage boundary, not proof that no undefined operation occurred.

Relevant owners are [pipeline orchestration](../../../packages/modelsan/modelsan/pipeline.py),
[divisor declared-value construction](../../../packages/modelsan/modelsan/divisor/constraints.py),
[guard truth evaluation](../../../packages/modelsan/modelsan/divisor/sites.py),
[Rumoca transport/classification](../../../packages/modelsan/modelsan/backends/rumoca.py),
and [native Solve-row domain hooks](../../../crates/rumoca-eval-solve/src/domain_diagnostics.rs).

## Evidence and reproduction

- [Compact machine-readable results](independent-results.json) include matching
  findings, exact witness hints, source compiler diagnostics, runtime failure
  details, typed contracts, native domain evidence, and per-case raw-log paths.
- Full evidence:
  `target/msl-issue-evaluation-20260924/independent/run-01/results.json`.
  Each variant directory retains nominal bitcode, stdout/stderr, OMC script,
  generated OMC results, and all sanitizer findings. The full evidence digest
  is recorded in the compact JSON; generated target files are not committed.
- Additional evidence:
  `target/msl-issue-evaluation-20260924/independent/discriminating-checks/results.json`.
- Evaluation began 2026-09-24 11:05:25 UTC. Head was
  `b38af3a38b0224bf22129cb1148ebf70e2492aa7`, **with the uncommitted current
  sanitizer/bitcode changes present**. Rumoca reports `0.10.0`; executed binary
  SHA-256:
  `6d50c5ababb18c68b367a7b353599d7ce2b595c61f65187f98abfb38b625aa06`.
  Head alone does not identify this dirty-tree build.
- OpenModelica: `1.27.1~2-g6db4671`; explicit bundled MSL `4.1.0`, confirmed by
  each OMC script. OMC uses `CC=gcc`, `CXX=g++`, one worker, and ordinary script
  execution. No socket transport or network download is required.
- Enabled sanitizers: all current `DEFAULT` sanitizers, plus StructureSan,
  InitStaticSan, DimensionSan, NetworkSan. No comparative oracle was credited.
- Runs are serial; each source compilation/OMC pair has a 120-second process
  group watchdog; each native backend execution has a 60-second timeout. No
  timeout or analysis exception occurred. Invalid-source compiler returns stay
  in the denominator.

From the repository root, choose a new output directory:

```sh
PYTHONPATH=packages/rumoca-bitcode:packages/modelsan RAYON_NUM_THREADS=1 \
  python3 docs/evaluations/msl-issues-2026-09-24/independent-evaluate.py \
  --output target/msl-issue-evaluation-20260924/independent/run-02

python3 docs/evaluations/msl-issues-2026-09-24/independent-summarize.py \
  target/msl-issue-evaluation-20260924/independent/run-02/results.json \
  target/msl-issue-evaluation-20260924/independent/run-02/summary.json
```

The report does not claim that all HIGH findings produced by these models are
true positives. It measures whether the **specific, independently reported
issue** is identified, and records the boundaries that block corroboration.
No production implementation was changed by this evaluation.
