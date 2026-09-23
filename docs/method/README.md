# How ModelSan decides something is a finding

The detectors are the easy part. Everything below exists because a detector
reported something that turned out not to be a bug, and the check that would
have caught it was added afterwards. They are recorded here in the order a
candidate passes through them.

Every number in this document is reproducible from `tools/sweep/`.

## 1. Two front ends, for two different jobs

| | Rumoca | OpenModelica |
|---|---|---|
| Role | analysis, explanation | execution, coverage |
| Corpus reach | 332 / 847 compiled | ~93% built |
| Gives | typed DAE, incidence, bitcode | executable + parameter bounds |

Neither is sufficient alone.

**Rumoca cannot be the execution engine.** 515 of 847 models never reach a
detector, for reasons that have nothing to do with the models: 86 need MLS §12.9
external objects, 30 need Fluid media, ~30 hit a record-array vectorisation gap.
Those are compiler gaps, and waiting on them caps the sanitizer at 39% of the
corpus.

**OpenModelica cannot be the analysis engine.** It offers no IR to read, so
there is no incidence information to say *which* parameter is a sole
coefficient. That is what makes the search targeted rather than brute force, and
it is why [BUG-006](../verified%20bugs/BUG-006-bound-propagated-into-a-different-component.md)
was findable at all — the bound and the singular coefficient were in different
components, linked through `C = k/(2*pi*f*R)`.

So: OMC runs the search, Rumoca explains and confirms it. The OMC backend is
`packages/modelsan/modelsan/omc_backend.py`; it calls `buildModel` once per
model and re-runs the executable with `-override` per trial, because rebuilding
per trial is what made the first differential sweep unaffordable.

## 2. A baseline, before anything is attributed

The model must simulate cleanly at its declared values. Without this, the first
candidate tried gets blamed for a pre-existing failure — which produced two
false reports in the first MSL sweep, fixed in `01c758d2`.

## 3. Probe only values the declaration permits

Four declaration shapes, three behaviours:

| Shape | Probe | Why |
|---|---|---|
| `min=0` | `0` | explicitly permitted; strongest claim |
| no bound | `0` | permitted by omission |
| `min=DBL_MIN` | nothing | OMC's spelling of "positive". Zero is excluded and DBL_MIN is a denormal no author chose. |
| real positive bound | the bound | the value the component claims to support |

Array *data* elements (`table.table[2]`) are skipped: zeroing one entry of a
lookup table is data corruption, not an operating point, and says nothing about
a declared domain.

Before this filter, one 100-model run produced 178 findings. After it, the same
models produced a handful.

## 4. Attribute by component type, never by parameter name

A finding names an instance path — `L.L`, `genericFluxTube.material.B_myMax`.
Grouping by the parameter's leaf name is unsound: **14 components declare `k`,
26 declare `Goff`.** Name-grouping was about to pin an OpAmps finding on
`Blocks/package.mo` because both spell it `k`.

`tools/sweep/resolve_types.py` walks the path through `getComponents`, so `L.L`
resolves to `Modelica.Electrical.Analog.Basic.Inductor` and `mass1.m` to
`Modelica.Mechanics.Translational.Components.Mass`.

## 5. Find where the bound is actually declared

Most MSL components declare no bound of their own — it arrives with the SI type.
`Capacitor.mo` says only `parameter SI.Capacitance C(start=1)`; the `min=0`
lives in `type Capacitance = Real(..., min=0)`.

Reporting that as the component's bound would send a maintainer to the wrong
file. See [the SI type study](../findings/si-type-bounds.md), which is where
this check turned into a finding of its own.

## 6. Drop what the component already guards

MSL has two correct idioms besides tightening a bound, and neither is a defect:

```modelica
// structural branch — Magnetic.FundamentalWave.Components.EddyCurrent
if G > 0 then (pi/2)*V_m.re = G*der(Phi.re); else V_m.re = 0; end if;

// guarded expression — Blocks.Logical
rate = if u and (rising > 0) then amplitude/rising else ...;
```

A third pattern needs branch reachability rather than a guard test:
`Blocks.Sources.Ramp` divides by `duration` inside `time < startTime + duration`,
which is empty when `duration = 0`.

## 7. Separate what the finding proves

Never summed, because they are not the same claim:

* **`zero-permitted-by-bound`** — a written bound *includes* the value that
  breaks the model. The declaration is provably a promise the component cannot
  keep. Strongest.
* **`zero-permitted-by-omission`** — nothing was declared. Real, but arguing the
  value is reachable is a judgement about the quantity, not a contradiction of
  anything written down.
* **`fails-at-its-own-positive-bound`** — e.g. `min=Modelica.Constants.small`,
  which is 1e-60. The same kind of contradiction, far weaker in practice: no
  calibration loop lands there by accident.

## 8. Cross-confirm in the other tool

A failure in one tool is ambiguous. `Inductor.L = 0` yields `0 = v`, which a
tool could fail on merely by not re-indexing a degenerate equation — a gap in
the tool, not a defect in MSL.

Of 12 parameter-triggered failures Rumoca found in MSL and ModelicaTest:

| | Count |
|---|---|
| Confirmed — both tools pass at declared values, fail at the trigger | **10** |
| **Excluded** — OpenModelica survives, so the failure is Rumoca's | **2** |

The two excluded (`CompareBrakingTorque`, `CompareBrakingForce`) would otherwise
have been filed as MSL bugs.

**Known limit:** for models Rumoca cannot compile, findings are single-tool.
That is a real weakening, partly offset for `zero-permitted-by-bound`, whose
argument is about the declaration rather than about tool behaviour.

## What each stage removed

| Stage | Effect |
|---|---|
| Probe policy | 178 findings → a handful, on the same 100 models |
| Type attribution | 116 name-groups → correctly attributed classes |
| Guard + reachability | rejected the `EddyCurrent` and `Ramp` patterns |
| Cross-confirmation | 12 → 10, removing 2 tool artifacts |
| Text-level census (superseded) | ran at 23% precision; see [min0-census](../findings/min0-census.md) |

- [divide-by-zero-analysis.md](divide-by-zero-analysis.md) — what the divisor detector must prove, and the regression cases that check it.
- [zero-behavior-contracts.md](zero-behavior-contracts.md) — one classification of what zero means, shared by three detectors.
- [physical-intent-advisory-instructions.md](physical-intent-advisory-instructions.md) — implementation and regression instructions for keeping uncertain physical anomalies visible without treating guessed intent as an error.
