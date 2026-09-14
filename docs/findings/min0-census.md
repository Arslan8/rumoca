# Census: the `min=0` idiom in MSL 4.1.0, and why the text-level version of this check does not work

BUG-002 found one instance of a general shape: a parameter whose declared lower
bound admits a value its own equations cannot survive. The obvious next question
is how many more there are. This note answers it, and records that the cheap way
of asking is not good enough — which is the reason the detector lives on the DAE.

Reproduce with `tools/sweep/min0_census.py <msl-root> out.json`.

## What MSL declares

Across all 2 556 `.mo` files, parameters declared with an explicit numeric lower
bound:

| Bound | Count |
|---|---|
| `min=0` (admits zero) | 326 |
| `min=Modelica.Constants.eps` / `.small` (excludes zero) | 147 |

MSL therefore knows the guarded idiom and uses it 147 times. The question is
whether the 326 are all cases where zero is genuinely fine.

## Narrowing to parameters zero would actually break

Restricting to parameters that appear, *in the same file's equation section*, as
a divisor or as a multiplier of a `der(...)`:

| | `min=0` | `min=eps`/`small` |
|---|---|---|
| Used in such a position | 16 | 49 |
| …and not self-guarded by a `p > 0` test | **13** | 47 |

"Self-guarded" means the file tests the parameter before relying on it. MSL has
two correct idioms here besides tightening the bound:

```modelica
// Magnetic/FundamentalWave/Components/EddyCurrent.mo — structural branch
if G > 0 then
  (pi/2)*V_m.re = G*der(Phi.re);
else
  V_m.re = 0;
end if;

// Blocks/Logical.mo:700 — guarded expression
rate = if u and (rising > 0) then amplitude/rising else ...
```

Neither is a defect. Both honour `min=0` by handling zero explicitly.

## Then checking all 13 by hand

This is the part that matters. Of the 13 survivors:

| Verdict | Count | Examples |
|---|---|---|
| **Genuine** | 3 | `Rotor1D.J` ([BUG-005](BUG-005-multibody-rotor1d-zero-inertia.md)) ×2 decls, `OpAmpCircuits/Der.k` ([BUG-006](BUG-006-bound-propagated-into-a-different-component.md)) |
| Division is unreachable at zero | 5 | `Blocks.Sources.Ramp.duration`, `Sources.Trapezoid.rising` — the division sits in a `time < start + duration` branch that is empty when the parameter is `0`, and the preceding branch already covers `time < start`. MSL documents the Ramp case: *"If parameter duration is set to 0.0, the limiting case of a Step signal is achieved."* |
| Unknown is on the other side | 3 | `MultiBody.Forces.Damper.d` — `f = d*der(s)` determines `f`, not `der(s)`. At `d = 0` the damper exerts no force, which is exactly what `start = 0` intends. |
| Parameter is the numerator | 1 | `Fluid/Pipes.m_flow_turbulent` |
| Divisor, but does not fail | 1 | `Fluid/Pipes.perimeter` — see below |

**3 of 13 real: 23% precision.** For a sanitizer that is not a usable rate.

## The one that is neither

`Fluid/Pipes.mo` computes `4*crossArea/perimeter` with `perimeter(min=0)` and no
guard. Isolating that shape and setting `perimeter = 0`:

```console
$ rumoca compile-bitcode p.rbc --simulate --check --t-end 0.5 --param perimeter=0
[]
```

It does not fail. The division yields `inf`, the characteristic dimension
becomes `inf`, and the model integrates cleanly to a physically meaningless
answer. That is arguably worse than a failure, but it is not the defect this
detector claims to find, and no property currently states it. Recorded, not
filed.

## Why the misses happen, and what fixes them

Every false positive above is the same mistake: deciding from *text* what can
only be decided from *structure*.

- Unreachable-at-zero needs to know which branch is live.
- "Unknown on the other side" needs to know which variable an equation
  determines — incidence, not syntax.
- [BUG-006](BUG-006-bound-propagated-into-a-different-component.md) is the
  converse: the text-level check found it only by accident, because the chain
  `k → C → C*der(v)` crosses a component boundary and a `final` binding. A
  per-file scan should have missed it entirely.

All four are available in the DAE, after flattening and structural analysis, and
none are available in the source. That is what `find_singular_risks` in
`packages/modelsan/modelsan/analysis.py` runs on, via the bitcode export — and
it is the concrete reason the analysis needed a compiled IR to read rather than
a parser.

The text census keeps its use as a *recall* instrument: it says the population
is 326, which bounds how much the structural detector could still be missing.
