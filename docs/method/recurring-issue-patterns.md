# Recurring issue patterns in the Modelica Standard Library

A checker is worth building when the defect it finds *recurs*. A one-off bug is
cheaper to fix than to detect. This catalogue is the evidence for which MSL
defects repeat, mined from the 352 independent open issues in
[the 2026-09-24 snapshot](../evaluations/msl-upstream-open-issues-2026-09-24/),
and it is what decides the sanitizer backlog.

## Method

Issues were grouped by *mechanism*, not by library or symptom. A group is a
pattern when two or more independent issues share a mechanism, or when one
issue's mechanism is a general Modelica hazard that will recur regardless of
how many instances the tracker happens to hold today. Each pattern records what
a checker would need to see, because a pattern nothing in the IR can observe is
a research item, not a backlog item.

247 of the 352 are documentation, enhancement, external-tool, reference or
unresolved entries; they are out of scope for a numerical sanitizer and are not
catalogued here. 105 are plausibly in scope.

## The patterns

| # | Pattern | Instances | Static? | Data available |
|---|---|---:|---|---|
| P1 | Declared unit disagrees with declared quantity | 21 | yes | now |
| P2 | Pure function calls an impure function | 5 | yes | frontend has it |
| P3 | Missing `homotopy` on nonlinear flow/friction | 4 | partly | needs a shape rule |
| P4 | Locally unbalanced class (MLS §4.7) | 3 | yes | now |
| P5 | Conservation term dropped from a balance | 3 | yes | now |
| P6 | Medium inverse/round-trip contract broken | 5 | no — runtime | contracts exist |
| P7 | Uninitialized record field or function output | 2 | yes | needs check |
| P8 | `Constants.eps`/`small`/`inf` used as a physical value | 3 | yes | now |
| P9 | Size-determining parameter not constrained `min=0` | 1+ | yes | now |
| P10 | Missing `each` on an array modifier | 1+ | yes | needs check |

### P1 — declared unit disagrees with declared quantity (21)

The largest cluster by a wide margin, and the cheapest to check: MSL states both
the `quantity` and the `unit` on nearly every declaration, so the two can be
cross-checked with no execution and no inference.

Sub-patterns, each a separate check because each has a different fix:

- **P1a — a quantity maps to more than one unit across the library.** MLS §4.8
  makes `quantity` the semantic identity of what is measured, so the mapping
  quantity → dimension must be a function. Six quantities in `Modelica.Units`
  violate this today: `Angle` (`rad`, `deg`), `Energy` (`J`, `eV`),
  `Power` (`W`, `V.A`, `var`), `ThermodynamicTemperature`
  (`K`, `degC`, `degF`, `degRk`), `AngularFrequency` (`rad/s`, `s-1`),
  `SpecificEnergy` (`J/kg`, `Gy`). Covers [#3158], [#4062], [#4088].
- **P1b — a type declares a unit and no quantity.** Eleven instances in
  `Units.mo` alone (`Stress`, `PerUnit`, `DimensionlessRatio`, eight
  `Der*By*` types). Covers [#4086], [#4085].
- **P1c — an SI symbol differs from the intended one only by case.**
  `LogarithmicDecrement` is declared `unit="1/S"`; capital `S` is siemens, so
  the declared unit is ohms for a dimensionless quantity. Covers [#3853].
- **P1d — a non-SI unit on a public interface.** Covers [#3917], [#2302], [#414].
- **P1e — a physical variable with no unit at all.** Covers [#2347], [#4632].

The reference mapping is **derived from `Modelica/Units.mo` itself** (347
quantities, 436 definitions), never hardcoded here. A hand-written table would
be one more record that silently falls behind the library, which is the failure
mode [TOOLBUG-027](../toolbugs/TOOLBUG-027-tests-and-docs-assert-limitations-that-were-fixed.md)
is about.

### P2 — pure function calls an impure function (5)

[#3655], [#3855], [#3856], [#3857], [#4182]. MLS §12.3: a function is pure
unless declared `impure`, and a pure function may not call an impure one. The
compiler already emits `WR001` for external functions that declare neither, so
the frontend carries the information; it is not yet in the bitcode.

Five independent reports of one rule is the clearest "this will happen again"
signal in the corpus.

### P3 — missing `homotopy` on nonlinear flow/friction (4)

[#665], [#666], [#667], [#668] — four near-identical reports, differing only in
which Fluid component they name (pipe wall friction, volume heat transfer, valve
friction, fitting friction). A pattern that was filed four times is a pattern.

Detection is not a pure syntax check: the signal is a nonlinear pressure/flow
relation in an initial system with no `homotopy` operator anywhere in its
partition. Scoped as a shape rule over the DAE, not a name match.

### P4 — locally unbalanced class (3)

[#4697], [#4703], [#4317]. MLS §4.7 requires a balanced model. Counting
equations against unknowns per class is exactly what the Flat IR already knows.

### P5 — conservation term dropped from a balance (3)

[#322], [#329], [#3569] — kinetic-energy term missing from a fluid balance.
This is the pattern the existing connection-graph work already addresses
(`network-conservation-violated`); these three are the upstream evidence that it
was worth building.

### P6 — medium inverse/round-trip contract broken (5)

[#4749], [#4750], [#1659], [#4728], [#4730]. Two are already detected by
`BehaviorSan` contracts. Inherently runtime: the defect is a wrong number, not a
wrong shape. Each new instance needs a declared expectation, which is why this
pattern does **not** scale the way P1–P4 do.

### P7–P10

Smaller but each a standing Modelica hazard rather than an MSL accident:
uninitialized record fields ([#1910], [#3687]); `Constants.eps` used as a
physical threshold ([#4607], [#4503], [#1064]); a vector-length parameter that
permits a negative value ([#2062]); a missing `each` on an array modifier
([#4684]).

## What this implies

P1–P5, P7–P10 are static and together account for ~40 of the 105 in-scope
issues. They need **no fixture and no declared expectation**, so one checker
covers every present and future instance — unlike P6, where each instance costs
a hand-written contract. That asymmetry is the reason the backlog is ordered
this way and not by issue count alone.

[#414]: https://github.com/modelica/ModelicaStandardLibrary/issues/414
[#665]: https://github.com/modelica/ModelicaStandardLibrary/issues/665
[#666]: https://github.com/modelica/ModelicaStandardLibrary/issues/666
[#667]: https://github.com/modelica/ModelicaStandardLibrary/issues/667
[#668]: https://github.com/modelica/ModelicaStandardLibrary/issues/668
[#1064]: https://github.com/modelica/ModelicaStandardLibrary/issues/1064
[#1659]: https://github.com/modelica/ModelicaStandardLibrary/issues/1659
[#1910]: https://github.com/modelica/ModelicaStandardLibrary/issues/1910
[#2062]: https://github.com/modelica/ModelicaStandardLibrary/issues/2062
[#2302]: https://github.com/modelica/ModelicaStandardLibrary/issues/2302
[#2347]: https://github.com/modelica/ModelicaStandardLibrary/issues/2347
[#322]: https://github.com/modelica/ModelicaStandardLibrary/issues/322
[#329]: https://github.com/modelica/ModelicaStandardLibrary/issues/329
[#3158]: https://github.com/modelica/ModelicaStandardLibrary/issues/3158
[#3569]: https://github.com/modelica/ModelicaStandardLibrary/issues/3569
[#3655]: https://github.com/modelica/ModelicaStandardLibrary/issues/3655
[#3687]: https://github.com/modelica/ModelicaStandardLibrary/issues/3687
[#3853]: https://github.com/modelica/ModelicaStandardLibrary/issues/3853
[#3855]: https://github.com/modelica/ModelicaStandardLibrary/issues/3855
[#3856]: https://github.com/modelica/ModelicaStandardLibrary/issues/3856
[#3857]: https://github.com/modelica/ModelicaStandardLibrary/issues/3857
[#3917]: https://github.com/modelica/ModelicaStandardLibrary/issues/3917
[#4005]: https://github.com/modelica/ModelicaStandardLibrary/issues/4005
[#4062]: https://github.com/modelica/ModelicaStandardLibrary/issues/4062
[#4085]: https://github.com/modelica/ModelicaStandardLibrary/issues/4085
[#4086]: https://github.com/modelica/ModelicaStandardLibrary/issues/4086
[#4088]: https://github.com/modelica/ModelicaStandardLibrary/issues/4088
[#4182]: https://github.com/modelica/ModelicaStandardLibrary/issues/4182
[#4317]: https://github.com/modelica/ModelicaStandardLibrary/issues/4317
[#4451]: https://github.com/modelica/ModelicaStandardLibrary/issues/4451
[#4503]: https://github.com/modelica/ModelicaStandardLibrary/issues/4503
[#4607]: https://github.com/modelica/ModelicaStandardLibrary/issues/4607
[#4632]: https://github.com/modelica/ModelicaStandardLibrary/issues/4632
[#4684]: https://github.com/modelica/ModelicaStandardLibrary/issues/4684
[#4697]: https://github.com/modelica/ModelicaStandardLibrary/issues/4697
[#4703]: https://github.com/modelica/ModelicaStandardLibrary/issues/4703
[#4728]: https://github.com/modelica/ModelicaStandardLibrary/issues/4728
[#4730]: https://github.com/modelica/ModelicaStandardLibrary/issues/4730
[#4749]: https://github.com/modelica/ModelicaStandardLibrary/issues/4749
[#4750]: https://github.com/modelica/ModelicaStandardLibrary/issues/4750

## Measured: P1, first implementation

`QuantitySan` (per model) and `tools/units/library_audit.py` (per library),
swept over the 848-model corpus list on 2026-09-24. 285 models compiled.

| Check | Findings | Verified | Precision |
|---|---:|---|---|
| `binding-unit-conflict` | 7 | 7 true, all checked against MSL source | 7/7 |
| `quantity-unit-dimension-conflict` | 0 | — | — |
| `quantity-unit-not-si-coherent` | 4 | 4 genuine non-SI declarations, low severity | 4/4 |
| `quantity-missing` | 375 | genuine, 45 distinct signatures | advisory |

Seven true positives, three mechanisms:

| Models | Mechanism | Upstream |
|---|---|---|
| CauerLowPass **Analog**, **OPV**, **SC** | capacitance bound to a reciprocal inductance or capacitance | [#4079], [#4078], and **SC is a third instance named in neither** |
| DCPM_Drive | resistance bound to a voltage over an unstated current | not filed — [our report](../findings/msl-dcpm-drive-resistance-from-voltage.md) |

The library audit additionally reproduces [#3158] (`Angle` in `rad` and `deg`),
[#4062] (`Energy` in `J` and `eV`, six types) and [#4086] (11 types declaring a
unit and no quantity) directly from `Units.mo`, without compiling anything.

### What the sweep corrected

The first 240-model sample reported **100%** precision on three findings. The
full sweep found ten, of which **three were false** — correct MSL code that
[TOOLBUG-028](../toolbugs/TOOLBUG-028-constant-folding-discards-the-unit.md)
made look wrong, because constant folding discards a constant's unit and
`mu_r = B_r/(mu_0*H_cB)` reaches the artifact with `mu_0` as a bare number.
True precision before mitigation was 70%.

Two lessons, both about measurement rather than about units:

- a precision claim from three draws is not a precision claim, and the
  temptation to publish one is strongest exactly when the checker is new;
- a false positive is worth more than a true one when it is caused by the
  tool, because it points at a defect that silently affects every other
  analysis over the same IR. `DimensionSan` shares TOOLBUG-028's exposure and
  has not been audited for it.

Two further false-positive sources were found and fixed before this run: whole-
string unit comparison reported every `ApparentPower` declaration (`V.A` is
watts spelled compositely), and dimensionless values with no quantity produced
24 findings for MultiBody direction-vector components. Both are pinned by named
tests in `packages/modelsan/tests/test_quantity.py`.
