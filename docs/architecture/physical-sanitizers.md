# PhysicalSan — physical invariants over arbitrary domains

Infrastructure for sanitizing physical models, not an electrical-circuit
checker. Electrical, mechanical, thermal, fluid and battery rules share one
invariant representation and one engine, and a sixth domain requires touching
neither.

```
                       RBC model
                           |
                    +------v------+
                    |   engine    |   domain-blind
                    +------+------+
                           |  loads
   +---------+---------+---+-----+---------+---------+
   |         |         |         |         |         |
electrical mechanical thermal   fluid   battery   (yours)
   |         |         |         |         |         |
   +---------+---------+----+----+---------+---------+
                            |
                +-----------v-----------+
                | static | runtime|hints|
                +-----------+-----------+
                            v
                        Findings
```

## What made this possible

The bitcode did not carry enough to match rules semantically. Variables had a
`unit` but no declared quantity, and the brief is explicit that a unit is not
sufficient — `Ohm` does not imply a value must be positive.

Flat *did* carry MLS §4.8 `quantity`, so `RbcVariable.physical_quantity` was
added to the schema and exporter. On a Damper, 78 of 81 variables now arrive
with `Mass`, `Force`, `TranslationalDampingConstant` and so on: the author's own
statement of what a variable measures.

## Matching, and what it refuses to do

Evidence is ranked, and every match records what supported it:

| Confidence | Evidence |
|---|---|
| `QUANTITY_AND_UNIT` | declared quantity and unit agree |
| `QUANTITY` | the declared `quantity` attribute matched |
| `UNIT_ONLY` | only the unit matched — **rejected by default** |
| `NONE` | no evidence |

A variable *named* `R` with no metadata does not match a resistance rule. A
differently-named variable declared `quantity="Resistance"` does. This is
enforced by test, not convention.

Unit-only is rejected because negative resistance is a real device (a
negative-impedance converter), and MSL's own Spice3 uses `-1e40` on a
`SI.Resistance` as an "unset" sentinel. What justifies `R > 0` is that the
*component* is passive.

## Adding a domain

Nothing in `physical/` outside `domains/` changes. `Domain` is an open string
subclass rather than an enum precisely so this holds.

```python
from modelsan.physical.invariant import Comparison, Domain, Enforcement
from modelsan.physical.rules import QuantityRule, RulePack

AERODYNAMIC = Domain("aerodynamic")

PACK = RulePack(domain=AERODYNAMIC, rules=[
    QuantityRule(
        rule_id="aero.drag_coefficient.positive",
        domain=AERODYNAMIC,
        quantities=frozenset({"DragCoefficient"}),
        op=Comparison.GT, bound=0.0,
        origin="drag opposes motion; a negative coefficient would propel the body",
        enforcement=Enforcement.STATIC, parameters_only=True,
    ),
])
```

Then `PhysicalSan(packs=[*BUILTIN, PACK])`. `test_domain_is_open` verifies the
engine enforces a domain it has never heard of.

A rule needing something structural — a relation between several variables, a
conservation law — implements the `Rule` protocol directly instead of using
`QuantityRule`. `Term` already supports sums over several variables, so
`sum(flows) = 0` needs no representation change.

## Static, runtime, and "permitted but unenforced"

Three outcomes, deliberately distinguished:

| Kind | Meaning |
|---|---|
| `physical-invariant-violated` (static) | a declared value breaks the invariant |
| `physical-invariant-violated` (runtime) | an observed value breaks it |
| `physical-domain-unenforced` | nothing in the model stops a forbidden value |

The third is the large class in MSL: 17 SI types permit physically impossible
values and 917 declarations inherit them. It is reported at MEDIUM because
nothing has gone wrong *yet* — but nothing prevents it either.

An invariant whose variable already declares a `min` at least as strong is
**not** reported. The model is enforcing it, and saying otherwise would be noise.

## Provenance, both kinds

A physical invariant is an external claim, so a finding cites the claim as well
as the code:

```
domain        mechanical
rule          mech.mass.positive
rule_origin   m*a = f determines acceleration only for m > 0; negative mass
              is not a physical body
matched_by    {quantity: Mass, unit: kg, confidence: QUANTITY_AND_UNIT}
observed      -2
required      b.m > 0
```

Without `rule_origin` a reader cannot tell a law of physics from someone's
guess.

## A bug worth recording

The first implementation read only bare literals when folding a declaration.
`-2.0` reaches the DAE as a **unary minus over a literal**, not as a literal, so
every *negative* declaration read as "no value" — the exact case the sanitizer
exists for. `-998` happened to fold and `-2.0` did not, which made the omission
look like it worked on one of four test models.

`constant_value` now folds sign and constant arithmetic, and stops at anything
referring to another parameter, which stays undecided rather than guessed.

## Tests

`packages/modelsan/tests/test_physical.py` — 25 assertions covering the open
domain, multi-variable predicates, name-blind matching, unit-only rejection,
negative-literal folding, bound suppression, four domains valid *and* invalid,
and provenance.
