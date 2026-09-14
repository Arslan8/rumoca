# `SI.Period` — 4 unbounded declarations

Domain: timing

`Units.mo` declares `type Period` with **no `min`**, so every
declaration below accepts a negative value.

## Exposed

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Blocks/Interfaces.mo` | 1303 | `samplePeriod` | `(start=0.01)` |
| `Blocks/package.mo` | 1855 | `samplePeriod` | `—` |
| `Blocks/package.mo` | 2676 | `samplePeriod` | `—` |
| `Math/Random.mo` | 14 | `samplePeriod` | `—` |
