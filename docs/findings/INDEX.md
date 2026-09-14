# Index

Everything produced by this project, in the order you would read it.

## Start here

| | |
|---|---|
| [../README.md](../README.md) | Why findings, method and toolbugs are separate folders |
| [README.md](README.md) | The findings, with the corpus numbers behind them |
| [../method/README.md](../method/README.md) | How a candidate becomes a finding — the eight verification stages, and what each one removed |

## Findings — bugs in target programs

Latent parameter-triggered failures: the model simulates cleanly at its declared
values and fails at a value its own declaration permits.

| ID | Target | Trigger | Confirmed in |
|---|---|---|---|
| [BUG-010](BUG-010-inductor-documents-zero-it-cannot-honour.md) | `Analog.Basic.Inductor` | `L = 0` | both tools, 3 models |
| [BUG-002](BUG-002-msl-zero-mass-within-declared-bound.md) | `Translational.Mass`, `Rotational.Inertia` | `m = 0`, `J = 0` | both tools; 17 + 29 models in the full sweep |
| [BUG-013](BUG-013-capacitor-zero-capacitance-topology-dependent.md) | `SI.Capacitance` → `Analog.Basic.Capacitor` | `C = 0` | both tools, 12 models |
| [BUG-014](BUG-014-genericfluxtube-geometry-divisors.md) | `FluxTubes.GenericFluxTube` | `l = 0`, `area = 0` | both tools, 3 models each |
| [BUG-015](BUG-015-idealgear-zero-ratio.md) | `Rotational.Components.IdealGear` | `ratio = 0` | both tools, 1 model |
| [BUG-011](BUG-011-fluxtubes-b-mymax-unguarded-divisor.md) | `SoftMagnetic.BaseData` | `B_myMax = 0` | both tools, 2 models |
| [BUG-012](BUG-012-variablepermeance-unbounded-input.md) | `FluxTubes.VariablePermeance` | permeance input ≤ 0 | both tools, 1 model |
| [BUG-005](BUG-005-multibody-rotor1d-zero-inertia.md) | `MultiBody.Parts.Rotor1D` | `J = 0` | static only |
| [BUG-006](BUG-006-bound-propagated-into-a-different-component.md) | `OpAmpCircuits.Der` | `k = 0` | isolated shape only |
| [BUG-003](BUG-003-switchedrlc-zero-resistance.md) | `examples/models/SwitchedRLC.mo` | `R = 0` | this repo, not MSL |

## Studies

| | |
|---|---|
| [si-type-bounds.md](si-type-bounds.md) | Where MSL's declared domains come from, and the three ways components inherit a bound they cannot keep. The sharpest single item: MSL defines `SelfInductance(min=0)` and `Basic.Inductor` does not use it. |
| [min0-census.md](min0-census.md) | All 326 `min=0` declarations against 147 guarded ones — and why the text-level version of this check, at 23% precision, is not usable. |

## Upstream drafts — nothing has been filed

| | |
|---|---|
| [UPSTREAM-msl-inherited-bounds.md](UPSTREAM-msl-inherited-bounds.md) | Consolidated issue for `modelica/ModelicaStandardLibrary`, with a pre-filing checklist |
| [UPSTREAM-rumoca-compiler-defects.md](UPSTREAM-rumoca-compiler-defects.md) | Compiler defects, for the Rumoca remote |

## Tool defects — not results

In [`../toolbugs/`](../toolbugs/). Recorded because each caps how much of a
corpus the detectors can see.

| | |
|---|---|
| [BUG-001](../toolbugs/BUG-001-comprehension-in-for-equation-panic.md) | Compiler panic; root cause verified by prediction |
| [BUG-004](../toolbugs/BUG-004-record-array-destructured-without-subscript.md) | Blocks `QuasiStatic.Polyphase` |
| [BUG-007](../toolbugs/BUG-007-dae-drops-predefined-enum-in-assert.md) | `AssertionLevel` — **fixed** |
| [BUG-008](../toolbugs/BUG-008-bitcode-enumeration-round-trip.md) | Bitcode enumerations — **fixed**, in this project's own code |
| [BUG-009](../toolbugs/BUG-009-bitcode-omits-discrete-definitions.md) | Bitcode discrete definitions — **fixed**, likewise |
| [LIMITATION-001](../toolbugs/LIMITATION-001-index-reduction-drops-fixed-start.md) | Correct refusal; costs 2 MSL examples |
| [LIMITATION-002](../toolbugs/LIMITATION-002-no-solver-tolerance-control.md) | No `--rtol`/`--atol` |
| [coverage-blockers.md](../toolbugs/coverage-blockers.md) | The measured 515 blocked models, and one abandoned fix attempt |

## Tools

All in `tools/sweep/`, all reproducible.

| Script | Does |
|---|---|
| `fullsweep.py` | Rumoca-backed sweep, all detectors |
| `omcsweep.py` | OpenModelica-backed parameter search — one model, fan out with `xargs -P` |
| `verify2.py` | The funnel: type attribution, bound provenance, guards, claim strength |
| `resolve_types.py` | Resolves an instance path to the class that declares the parameter |
| `crossconfirm.py` | Re-runs each finding in the other tool |
| `trajdiff.py` | Trajectory differential, with signal-scaled tolerance |
| `diffbatch.py` | Batched acceptance differential |
| `min0_census.py` | Source-level `min=0` census |
| `roundtrip_audit.py` | Bitcode export/import fidelity over construct probes |
| `tests/test_compare_scaled.py` | Calibration for the divergence detector — 7 cases, both directions |
