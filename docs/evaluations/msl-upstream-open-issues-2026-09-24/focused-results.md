# Focused upstream reproductions and source checks

These results concern six independent upstream issue patterns. Five were exercised in this continuation; #4771 retains the earlier paired run. They are issue-derived witnesses against the local cached MSL 4.1.0, not executions of every original attachment or of current upstream master. External OMC expectations are evaluation oracles, **not discoveries by current ModelSan**.

## Executed evidence

| Issue | Witness and independent result | Current ModelSan/Rumoca result |
|---|---|---|
| [#4749](https://github.com/modelica/ModelicaStandardLibrary/issues/4749) | SimpleAir: construct state at 300 K, compute entropy, invert at the same pressure. OMC API evaluation returns 300 K at reference pressure 101325 Pa (control), but **5204.05361678 K** at 102338.25 Pa. | Both compile attempts fail ED008 on unresolved `PartialSimpleIdealGasMedium.cp_const` before bitcode. No sanitizer observation of the issue. |
| [#4750](https://github.com/modelica/ModelicaStandardLibrary/issues/4750) | ConstantPropertyLiquidWater: same entropy/state round trip at 100000 Pa, 300 K returns **327.45744097 K** in OMC API evaluation. | ED008 on unresolved `PartialSimpleMedium.cp_const`; blocked before bitcode. |
| [#3624](https://github.com/modelica/ModelicaStandardLibrary/issues/3624) | BooleanPulse, period=1, width=50. At t=0.1, start=-0.25 gives true; phase-equivalent start=-1.25 gives **false**. OMC simulates both successfully. | Both produce bitcode; backend refuses clocked conditions. Static width/start warning occurs in both controls and is unrelated to the phase defect. |
| [#4451](https://github.com/modelica/ModelicaStandardLibrary/issues/4451) | UnitDelay samplePeriod=.05, continuous input sin(2πt). At t=.175, OMC output **0.80901699437** equals the .15 input; one-sample delay should retain the .10 input **0.58778525229**. | Bitcode produced; event execution blocked by unsupported clocked conditions. No relevant static finding. |
| [#4459](https://github.com/modelica/ModelicaStandardLibrary/issues/4459) | SampleWithADeffects, bits=2, limited/quantized, default symmetric limits; sine sampled at .01. OMC observes **five levels {-1,-.5,0,.5,1}**, exceeding four. | Original bitcode produced; instrumentation cannot save unsupported `string_conversion` nodes 183/188. Independent static warnings do not establish level cardinality. |
| [#4771](https://github.com/modelica/ModelicaStandardLibrary/issues/4771) | Earlier issue-derived MoistAir public API pair: full composition {0,1} succeeds with 300 K; reduced {0} fails with index 2 out of extent 1 in OMC. | Both controls fail earlier with ED019 during record/package/function lowering, so no sanitizer detection. See [original run evidence](probes-results.json). |

These are **blocked evaluations**, not six measured algorithmic misses and not six ModelSan hits. They also are not a six-out-of-352 recall estimate. Static/source analysis indicates the specific semantic oracles are absent, but backend support must first allow an end-to-end test.

### Why the entropy functions are wrong in the tested source

In local `Modelica 4.1.0/Media/package.mo`, the SimpleIdealGas entropy expression uses `cp_const*log(T/T0) - R_gas*log(p/reference_p)` (around line 6342), while `setState_psX` adds `R_gas*log(p/reference_p)` directly in the exponent (around line 6281). That pressure contribution needs normalization by heat capacity to invert entropy. Reference pressure cancels the bad term, which is why the positive control matters.

For SimpleMedium, entropy uses `cv_const*log(T/T0)` (around line 6134), while inversion uses `exp(s/cp_const + log(reference_T))` (around line 5984). ConstantPropertyLiquidWater sets cp=cv=4184 and T0=273.15 K, while inherited reference_T=298.15 K. The observed wrong result is 300×298.15/273.15. This case isolates a reference-temperature inconsistency without relying on a speculative numerical overflow.

Neither round-trip expectation was inserted as a Modelica assertion or supplied as a ModelSan detector. A future contract should cover valid pressures/temperatures and compare restored state variables with scaled tolerances.

### Probe corrections and controls

Exploratory OMC simulations of nested record-return calls produced misleading values, and a rewrite with explicit records omitted the recovered constants from CSV output. Those exploratory numbers are **not** used as entropy evidence. The retained run uses direct OMC scripting evaluation of the actual MSL APIs and reports the returned thermodynamic record. It reproduces the algebraic expectations above, including the passing gas reference-pressure control. The phase/delay/quantization evidence comes from simulation CSV traces.

An initial evaluation-driver mistake read a nonexistent `BugDatabase.findings` attribute. The driver was corrected to flatten `database.bugs[].findings`, and all seven retained cases were rerun. [semantic-results.json](semantic-results.json) has no harness errors; it retains compiler output, OMC output, static findings, backend coverage and failures. This correction changes no production implementation.

## Source/discussion checks without execution credit

**[#4807 quadratureLobatto](https://github.com/modelica/ModelicaStandardLibrary/issues/4807).** Its body is now available. The linked [PR #4800 discussion](https://github.com/modelica/ModelicaStandardLibrary/pull/4800) describes a moving sinusoidal integral that hangs near a zero integral, around t=.25. The recursive stopping test relies on floating-point absorption of the estimated error into a tolerance-scaled integral. A guard for exactly zero does not handle a very small nonzero integral. The discussion proposes an absolute-aware scale and an explicit absolute error comparison. The cached `Math/Nonlinear.mo` contains the old scheme. A useful detector needs recursion/evaluation budgets plus an independent mixed absolute/relative quadrature-accuracy oracle. Generic timeout/solver failure provides only a symptom. The attached model was not executed here, and no reproduction or detection is credited. The supplemental [PR archive](linked-pr-4800.json) includes its comments and diff; PR #4800 is not part of the 353-issue census.

**[#4801 SupportFriction smoothness](https://github.com/modelica/ModelicaStandardLibrary/issues/4801).** The question infers missing behavior from a shared lookup function. The local component passes `smoothness` into `ExternalCombiTable1D` when constructing the table object; the shared lookup consumes that configured object. This source check undermines the accusation that the option is simply unused. It is not proof that every interpolation mode is correct; matched-mode tests would be required. Marked not established, not a sanitizer miss.

**[#4770 spline interpolation](https://github.com/modelica/ModelicaStandardLibrary/issues/4770).** Discussion distinguishes interpolating splines from a MATLAB smoothing spline and its smoothing parameter. Comparing different mathematical interpolation contracts cannot by itself demonstrate an MSL error. Marked unresolved pending a matched-method witness.

**[#4794 temporary files](https://github.com/modelica/ModelicaStandardLibrary/issues/4794), [#4773 Windows paths](https://github.com/modelica/ModelicaStandardLibrary/issues/4773).** These require external/platform checks for atomic creation and path encoding. They remain important engineering issues but are outside Modelica numerical sanitizers.

## Reproduce and inspect

From the repository root, with the existing debug executable, Python packages and cached MSL available:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/evaluations/msl-upstream-open-issues-2026-09-24/semantic_probes.py --output target/msl-upstream-new-run
```

Use a fresh output directory. Each compiler/OMC process is bounded; runtime backend attempts are bounded separately. The driver enables all default sanitizers plus DimensionSan, InitStaticSan, NetworkSan and StructureSan. It does not rebuild the compiler or alter MSL. OMC version in the retained run is **1.27.1~2-g6db4671**. The seven cases include two controls for five issue patterns; the older #4771 pair is separate.

- [Model source](SemanticProbes.mo), [driver](semantic_probes.py), [retained results](semantic-results.json).
- [Provenance](provenance.json): dirty-tree HEAD/status, compiler binary digest, driver/model and relevant Python/MSL source hashes. There is no claim that the preexisting binary was rebuilt from the current dirty tree.
- Full temporary build/CSV artifacts are under `target/msl-upstream-open-issues-20260924/semantic-run-03`; durable results retain trace hashes and observations. Earlier exploratory runs are not authoritative results.
- [Earlier #4771 driver](probes.py) and [retained results](probes-results.json) are historical evidence with their own source/binary hashes.
