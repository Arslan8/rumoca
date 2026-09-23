# TOOLBUG-013: a type's `min`/`max` never reached the DAE

| | |
|---|---|
| **Component** | Rumoca, `crates/rumoca-phase-instantiate/src/attributes.rs` |
| **Severity** | High — the DAE understated what the model declares |
| **Status** | Fixed, 2026-09-15 |

## What went wrong

MLS §4.8: a type's attribute modifications are part of the variable's type, so

```modelica
type Mass = Real(quantity="Mass", final unit="kg", min=0);
parameter SI.Mass m = 1;
```

declares `m >= 0` as surely as writing `m(min=0)` would. Instantiation
inherited `quantity`, `unit` and `displayUnit` from the type hierarchy —
`merge_type_hierarchy_string_attributes` — and nothing inherited the numeric
ones. They were dropped:

```text
parameter SI.ThermodynamicTemperature T1 = 300;   type says min=0.0  ->  DAE: None
parameter SI.Mass                     m1 = 1;     type says min=0    ->  DAE: None
parameter SI.Resistance               R1 = 1;     type says no min   ->  DAE: None
parameter SI.Mass m2(min=0) = 1;                  declaration repeats->  DAE: 0
```

Only a modifier written on the declaration survived. **29 SI types in MSL
declare a `min`**, and every variable typed by one reached the DAE unbounded.

## What it cost

Anything reading the DAE saw no bound where the library states one. For this
project's own sanitizers: **6424 of 10942 findings — 59% —** were on a type
that declares a `min`, reporting "nothing bounds this declaration" about
declarations MSL does bound.

| Finding kind | on a bounded type |
|---|---|
| `physical-runtime-invariant-unobserved` | 3015 / 3017 (100%) |
| `physical-domain-unenforced` | 3193 / 5118 (62%) |
| `physical-invariant-violated` | 56 / 318 (18%) |
| `physical-bound-permits-zero` | 160 / 1233 (13%) |
| `divisor-reachable-zero` | 0 / 1248 |

It is worse than a wrong count. A consumer using the DAE to *enforce* bounds
would not have enforced these, and a code generator emitting range assertions
would have omitted them.

## How it was found

Not by reading the compiler. By hand-adjudicating a random sample of findings
for a precision figure: the first entry claimed `ambient1.TAmbient >= 0` was
unenforced, and `Units.mo` plainly says `type ThermodynamicTemperature = Real(
final quantity="ThermodynamicTemperature", final unit="K", min = 0.0)`.

The sanitizer results had been read several times without anyone noticing that
the largest category was impossible.

## Fix

`merge_type_hierarchy_numeric_attributes`, the numeric counterpart of the
string one, walking the same `extends` chain for `min`, `max` and `nominal`. A
modifier on the declaration still wins: it is more specific, and MLS §7.2.5
lets it narrow the inherited bound.

The value is carried as an **expression**, not a rendered string — a bound may
be `Modelica.Constants.eps`, and later phases have to be able to evaluate it.

## Regression

`crates/rumoca/tests/suite_core/type_level_bounds.rs`.
