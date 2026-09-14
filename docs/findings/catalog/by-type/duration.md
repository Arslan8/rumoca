# `SI.Duration` — 1 unbounded declarations

Domain: timing

`Units.mo` declares `type Duration` with **no `min`**, so every
declaration below accepts a negative value.

## Exposed

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Clocked/BooleanSignals/TimeBasedSources/Pulse.mo` | 14 | `Twidth` | `—` |

## Guarded — these add their own bound

Same library, same quantity, bound written. This is why the exposed
cases read as omissions rather than as a deliberate choice.

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Blocks/Nonlinear.mo` | 531 | `delayMax` | `(min=0, start=1)` |
