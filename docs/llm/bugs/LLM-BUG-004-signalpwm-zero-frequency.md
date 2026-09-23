# LLM-BUG-004: `SignalPWM.f=0` invalidates every generated timing parameter

| Field | Value |
|---|---|
| Status | Confirmed |
| Class | `Modelica.Electrical.PowerConverters.DCDC.Control.SignalPWM` |
| Trigger | `f=0` |
| Nominal control | `f=1000` |
| Source | `Electrical/PowerConverters/DCDC/Control/SignalPWM.mo:10,37-56` |
| Reproducer | [`LLM_SignalPWMFrequencyZero.mo`](repro/LLM_SignalPWMFrequencyZero.mo) |

## Defect

The public switching frequency has no positive bound. It unconditionally sets
the zero-order-hold sample period to `1/f`; the selected carrier additionally
uses `1/f`, and the triangular carrier uses `0.5/f` for both edges. Therefore
`f=0` cannot represent a disabled PWM mode in the current implementation.

The denominators are explicit MSL parameter bindings, not solver-generated
quotients. The documentation calls `f` the switching frequency and provides no
zero-frequency sentinel behavior.

## Evidence

- OpenModelica: `f=1000` initializes and simulates; `f=0` terminates at
  initialization with division by zero and names `dut.f`.
- Rumoca: the nominal source translates. The invalid source is rejected at
  `samplePeriod=1/f` and identifies `SignalPWM.mo:38`.

Rumoca's current runtime cannot complete this nominal discrete probe for an
unrelated implementation limitation, so the complete nominal/invalid execution
pair is OpenModelica evidence; Rumoca is the independent source-level check.

Source SHA-256: `c3e33e9530aed21362dba9daf48b366a1e46f9fdbb91696da055aec1d5593148`.

## Proposed fix

Require `f > 0` at the public declaration and emit a direct domain diagnostic.
If zero is intended to disable switching, add a structural disabled branch that
does not instantiate any `1/f` timing binding and specify both Boolean outputs.

## Regression test

Exercise both carrier types at a nominal positive frequency. Test `f=0` and a
negative frequency as domain errors, or—if a disabled mode is added—verify its
documented constant outputs without evaluating a reciprocal.

## Rumoca reproduction

```sh
./target/debug/rumoca compile \
  docs/llm/bugs/repro/LLM_SignalPWMFrequencyZero.mo \
  --model LLM_SignalPWMFrequencyZero \
  --source-root target/msl/ModelicaStandardLibrary-4.1.0 \
  --emit-bitcode /tmp/pwm-zero.rbc --cache-dir /tmp/rumoca-llm-cache
```

The expected result names `samplePeriod=1/f` at `SignalPWM.mo:38`.

[Index](README.md)
