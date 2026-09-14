# LIMITATION-001: index reduction refuses MSL models that state `fixed = true` on a demoted state

| | |
|---|---|
| **Kind** | Coverage limitation, not a defect — the refusal is deliberate and correct |
| **Component** | `rumoca-phase-structural` |
| **Diagnostic** | `ES012` (`DroppedStatedInitialValue`) |
| **Affects** | At least 2 of 74 MSL example models swept |
| **Found by** | ModelSan corpus sweep, 2026-09-13 |
| **Status** | Documented; filed so the coverage cost is visible |

## What happens

```console
$ rumoca compile-bitcode InitialConditions.rbc --simulate --check
DAE structural proof failed: index reduction would discard the stated initial
value of `sd1.s_rel`: MLS 3.6 section 8.6 adds `sd1.s_rel = sd1.s_rel.start` to
the initialization equations for a `fixed = true` variable, and demoting
`sd1.s_rel` leaves no equation that states it
```

Affected models seen in the sweep:

- `Modelica.Mechanics.Translational.Examples.InitialConditions`
- `Modelica.Mechanics.Rotational.Examples.RollingWheel`

Both fail with their declared parameter values — no override involved.

## Why this is not filed as a bug

The refusal is principled and well-implemented. It has a dedicated error type
(`StructuralError::DroppedStatedInitialValue`), a diagnostic code
(`ES012`), a message citing MLS 3.6 §8.6, and an acceptance contract written
into `diagnostic_codes.rs` stating exactly which reductions it rejects.

This is SPEC_0031's stated philosophy working: *"Unsupported or unproved
semantics fail with a typed diagnostic at their first owning phase. Producing a
plausible artifact and discovering the gap from a wrong trace is a soundness
failure, not partial support."*

Silently dropping a user's `fixed = true` initial value and integrating anyway
would be worse than refusing.

## Why it is still worth recording

The cost is concrete: two standard MSL examples cannot be simulated. Other
tools handle this shape via dummy-derivative selection that preserves the
stated initial condition rather than demoting the variable that carries it.

Anyone reading MSL parity numbers should know these two are refusals of this
specific kind, not general failures — the distinction matters when deciding
whether the gap is worth closing.

## How ModelSan surfaced it

Initially as a **false bug report**, which is the more useful part of this
story.

The sweep attributed `InitialConditions` to `fixed2.s0 = 0`. That was wrong:
`s0` already defaults to `0`, so the "override" changed nothing, and the model
fails with no overrides at all. ModelSan had no nominal baseline, so the first
candidate it tried was blamed for a pre-existing failure.

Fixed in `01c758d2`: ModelSan now simulates the declared configuration first
and, when that fails, reports the failure without attributing it to any
parameter. Two of five MSL findings were reclassified by that change.
