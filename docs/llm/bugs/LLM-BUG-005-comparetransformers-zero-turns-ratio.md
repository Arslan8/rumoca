# LLM-BUG-005: transformer turns ratio admits zero despite reciprocal equations

| Field | Value |
|---|---|
| Status | Confirmed |
| Classes | `Modelica.Electrical.Analog.Examples.CompareTransformers`; contract also reaches `Modelica.Electrical.Analog.Ideal.IdealTransformer` |
| Trigger | `n=0` |
| Nominal control | `n=2` |
| Sources | `CompareTransformers.mo:10,17-26`; `IdealTransformer.mo:4,14` |
| Reproducer | [`LLM_CompareTransformersRatioZero.mo`](repro/LLM_CompareTransformersRatioZero.mo) |

## Defect

The example exposes an unconstrained turns ratio `n` and uses it in five
reciprocal bindings: `L2sigma`, `R2`, `RL`, `L2`, and `M`. It also passes `n`
to `IdealTransformer`, whose own public `n` is unconstrained and whose source
equation contains `i2/n`. Neither class states a nonzero contract even though
the implementation requires one.

Negative ratios may encode winding orientation, so the essential generic
contract is nonzero rather than blindly positive. Zero has no documented
transformer interpretation in either class.

## Evidence

- OpenModelica: the `n=2` example initializes and simulates. The otherwise
  identical `n=0` model terminates at initialization with division by zero and
  names divisor `n`.
- Rumoca: the nominal source translates. The zero source is rejected while
  evaluating `L2sigma=0.05/(2*pi*f)/n^2` at `CompareTransformers.mo:17`.

Rumoca cannot currently complete the nominal example's runtime because of an
unrelated trace-coordinate limitation; the complete execution comparison is
therefore OpenModelica evidence, with Rumoca independently confirming the
source binding failure.

Source SHA-256 values: example
`d966c9a4658ed8b44705fb58a962943e6623479a9bf6911e75754a0866ec6aba`;
component
`a5bbe8e9c0cad68c527bba93c56d51608b8721dce19d8ffa833ec372c1d00374`.

## Proposed fix

Give `CompareTransformers.n` a positive bound because the example's derived
physical values assume a magnitude. Add an explicit nonzero assertion to
`IdealTransformer.n`; use an absolute-value tolerance if signed ratios remain
supported. Ensure the assertion is checked before any reciprocal binding.

## Regression test

Keep `n=2` and add a negative nonzero ratio test for the generic transformer if
signed orientation is supported. Require `n=0` to produce a clear turns-ratio
domain diagnostic before evaluating any derived inductance or resistance.

## Rumoca reproduction

```sh
./target/debug/rumoca compile \
  docs/llm/bugs/repro/LLM_CompareTransformersRatioZero.mo \
  --model LLM_CompareTransformersRatioZero \
  --source-root target/msl/ModelicaStandardLibrary-4.1.0 \
  --emit-bitcode /tmp/transformer-zero.rbc --cache-dir /tmp/rumoca-llm-cache
```

The expected result identifies the `n^2` denominator in `L2sigma` at
`CompareTransformers.mo:17`.

[Index](README.md)
