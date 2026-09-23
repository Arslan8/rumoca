# LLM-BUG-001: `FirstOrder.T=0` reaches a direct denominator

| Field | Value |
|---|---|
| Status | Confirmed |
| Class | `Modelica.Blocks.Continuous.FirstOrder` |
| Trigger | `T=0` |
| Nominal control | `T=1` |
| Source | `Blocks/Continuous.mo:354,370` |
| Reproducer | [`LLM_FirstOrderZero.mo`](repro/LLM_FirstOrderZero.mo) |

## Defect

`T` is a public `SI.Time` parameter with only `start=1`; it has no positive
lower bound or assertion. The equation unconditionally evaluates
`der(y) = (k*u - y)/T`. Thus a source-valid component modification produces an
undefined model at initialization.

This is not a compiler-created quotient or an inactive branch. The division is
written directly in the block. The documentation describes a one-pole transfer
function and does not define `T=0` as a supported algebraic pass-through mode.

## Evidence

- OpenModelica with the pinned MSL 4.1.0: `T=1` initializes and simulates;
  `T=0` terminates at initialization with `division by zero` and names `dut.T`.
- Rumoca: the nominal bitcode simulates for 11 requested points with no property
  violations; the zero probe reports a non-finite derivative evaluation.

Source SHA-256: `e0c05b204354b734193f074495eaff174fcda05321e097560c4434cd4a697e61`.

## Proposed fix

Declare and enforce `T > 0`, preferably with a positive `min` plus a diagnostic
assertion that is checked before derivative evaluation. If the library wants
`T=0` to mean the algebraic limit `y=k*u`, implement that as an explicit
structural branch and document the change instead.

## Regression test

Keep the paired probe. Require the nominal case to simulate and require `T=0`
either to be rejected with the new domain diagnostic or to execute the newly
documented algebraic branch without any non-finite value.

## Rumoca reproduction

```sh
./target/debug/rumoca compile docs/llm/bugs/repro/LLM_FirstOrderZero.mo \
  --model LLM_FirstOrderNominal \
  --source-root target/msl/ModelicaStandardLibrary-4.1.0 \
  --emit-bitcode /tmp/first-nominal.rbc --cache-dir /tmp/rumoca-llm-cache
./target/debug/rumoca compile-bitcode /tmp/first-nominal.rbc \
  --simulate --check --t-end 0.1 --dt 0.01 --cache-dir /tmp/rumoca-llm-cache
./target/debug/rumoca compile docs/llm/bugs/repro/LLM_FirstOrderZero.mo \
  --model LLM_FirstOrderZero \
  --source-root target/msl/ModelicaStandardLibrary-4.1.0 \
  --emit-bitcode /tmp/first-zero.rbc --cache-dir /tmp/rumoca-llm-cache
./target/debug/rumoca compile-bitcode /tmp/first-zero.rbc \
  --simulate --check --t-end 0.1 --dt 0.01 --cache-dir /tmp/rumoca-llm-cache
```

[Index](README.md)
