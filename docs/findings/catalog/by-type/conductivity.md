# `SI.Conductivity` — 5 unbounded declarations

Domain: electrical

`Units.mo` declares `type Conductivity` with **no `min`**, so every
declaration below accepts a negative value.

## Exposed

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Magnetic/FluxTubes/BaseClasses/GenericHysteresis.mo` | 10 | `sigma` | `—` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo` | 95 | `sigma` | `—` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer3PhaseYyWithHysteresis.mo` | 96 | `sigma` | `—` |
| `Magnetic/FluxTubes/Material/HysteresisEverettParameter/BaseData.mo` | 17 | `sigma` | `—` |
| `Magnetic/FluxTubes/Material/HysteresisTableData/BaseData.mo` | 103 | `sigma` | `—` |
