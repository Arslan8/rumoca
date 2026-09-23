# LLM-BUG-002: both `CriticalDamping` blocks accept an impossible zero order

| Field | Value |
|---|---|
| Status | Confirmed |
| Classes | `Modelica.Blocks.Continuous.CriticalDamping`; `Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.CriticalDamping` |
| Trigger | `n=0` |
| Nominal control | `n=2` |
| Sources | `Blocks/Continuous.mo:1504-1538`; `ComponentsMixingUnit/CriticalDamping.mo:8-22` |
| Reproducers | [`LLM_BlocksCriticalDampingOrderZero.mo`](repro/LLM_BlocksCriticalDampingOrderZero.mo); [`LLM_CriticalDampingOrderZero.mo`](repro/LLM_CriticalDampingOrderZero.mo) |

## Defect

Both implementations declare `parameter Integer n=2` without `min=1`. With
`n=0`, they allocate `x[0]`, compute `1/n` while deriving `alpha`, and then
unconditionally reference `x[1]` and `x[n]`. A zero-order critically damped
filter is not implemented as a pass-through, and the documentation repeatedly
calls `n` the filter order without defining zero behavior.

The two classes duplicate the same missing structural contract, so this is one
root cause with two fix sites rather than two inflated bug instances.

## Evidence

- OpenModelica: both `n=2` probes simulate successfully; both `n=0` probes fail
  model construction.
- Rumoca: both nominal probes translate and simulate; both zero probes fail
  during source elaboration with `ET009`, identifying `x[1]` as out of bounds
  for an array of size zero.

Source SHA-256 values: main block
`e0c05b204354b734193f074495eaff174fcda05321e097560c4434cd4a697e61`;
Clocked utility
`39e253add206d7550a9568adbe28dcb2dd51abfe19a94f4934610e02795be524`.

## Proposed fix

Change both declarations to an integer parameter whose contract requires
`n >= 1`. Because `n` determines array dimensions, enforce the constraint
during elaboration rather than relying only on a runtime assertion.

## Regression test

Retain nominal tests for `n=1` and `n=2`. Add a negative elaboration test for
`n=0` that expects a clear parameter-domain diagnostic at the declaration,
before array construction or evaluation of `1/n`.

## Rumoca reproduction

```sh
./target/debug/rumoca compile \
  docs/llm/bugs/repro/LLM_BlocksCriticalDampingOrderZero.mo \
  --model LLM_BlocksCriticalDampingOrderZero \
  --source-root target/msl/ModelicaStandardLibrary-4.1.0 \
  --emit-bitcode /tmp/critical-zero.rbc --cache-dir /tmp/rumoca-llm-cache
```

The expected result is `ET009` at `Continuous.mo:1534`; substitute
`LLM_BlocksCriticalDampingOrderTwo` to compile the nominal control.

[Index](README.md)
