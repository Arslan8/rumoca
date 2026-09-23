# LLM-BUG-003: `Thyristor.IH` and `ITM` permit zero but define resistances by division

| Field | Value |
|---|---|
| Status | Confirmed |
| Class | `Modelica.Electrical.Analog.Semiconductors.Thyristor` |
| Triggers | `ITM=0`; independently, `IH=0` |
| Nominal control | `ITM=25`, `IH=6e-3` |
| Source | `Electrical/Analog/Semiconductors/Thyristor.mo:9-10,38-40` |
| Reproducer | [`LLM_ThyristorITMZero.mo`](repro/LLM_ThyristorITMZero.mo) |

## Defect

The public holding current `IH` and conducting current `ITM` have no lower
bounds or assertions. Protected bindings compute
`Ron=(VTM-0.7)/ITM` and `Roff=(VDRM^2)/VTM/IH`. Either zero-current setting
therefore invalidates the component before its circuit equations can run.

These are two triggers for the same missing current-domain contract. The
division is present directly in MSL source and is evaluated regardless of the
external circuit's operating mode.

## Evidence

- OpenModelica: the grounded nominal component simulates. `ITM=0` fails at
  initialization and names divisor `dut.ITM`; `IH=0` fails and names
  `dut.IH * dut.VTM`.
- Rumoca: the nominal component simulates cleanly. The invalid probes are
  rejected while evaluating `dut.Ron` and `dut.Roff`, respectively, at the MSL
  source lines above.

Source SHA-256: `dbc15414032e03eeb9cbd893db2913061fab13568315a704cf0dd228d1e45861`.

## Proposed fix

Require `IH > 0` and `ITM > 0`. Add positive bounds and explicit assertions,
and guard the protected resistance bindings so diagnostic evaluation cannot
itself divide by zero. Review `VTM` in the same change because it is also a
denominator of `Roff`.

## Regression test

Run the nominal grounded component and separate probes for `IH=0`, `ITM=0`,
and `VTM=0`. Each invalid setting should fail with the intended domain message,
not a generic floating-point or solver failure.

## Rumoca reproduction

```sh
./target/debug/rumoca compile docs/llm/bugs/repro/LLM_ThyristorITMZero.mo \
  --model LLM_ThyristorITMZero \
  --source-root target/msl/ModelicaStandardLibrary-4.1.0 \
  --emit-bitcode /tmp/thyristor-zero.rbc --cache-dir /tmp/rumoca-llm-cache
```

The expected result identifies division by `dut.ITM` while evaluating
`dut.Ron`; use model `LLM_ThyristorIHZero` for the independent `IH` trigger.

[Index](README.md)
