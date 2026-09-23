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

`constant_value` now folds sign and constant arithmetic.

## The same bug, one level up

Stopping at a reference to another parameter looked conservative and was not.
It made the verdict depend on the compiler rather than on the model:

```modelica
parameter Real scale = 2;      parameter Real scale = 2.5;
parameter SI.Resistance R = -scale * 5;
```

Rumoca rewrites a derived parameter's binding to its value, but only when that
value is an exact integer. So the left column arrives as `R = -10` and was
reported **violated**, while the right arrives as `R = -(scale * 5)` and was
reported merely **unenforced** — the weaker claim, for an equally impossible
-12.5, decided by whether the arithmetic happened to land on a whole number.

`constant_value` now follows a parameter's binding, with a visited set so a
cyclic binding terminates. Only the *binding* is followed: a `start` is a
solver's initial guess, and treating one as fixed partway down a chain would
report a violation the declaration never commits to. Nor is a reference under
`der()` or `pre()` followed — those name a trajectory, not a declaration.

This is what makes the sanitizer agree with itself under
`--no-fold-parameter-bindings` (below), and it is a detection gain in the
default mode too, because the non-integral chains were never folded to begin
with.

## Reading a chain the compiler would erase

`rumoca compile --no-fold-parameter-bindings` keeps every derived parameter
binding as written, so `d = k * 10` reaches the DAE naming `k` instead of
carrying `20`. DivisorSan needs this: with the chain gone it reports `d`, which
is a real unbounded divisor but not something a user can set, so the fix it
implies is in the wrong place.

The flag suppresses only the rewrite, never the evaluation. MLS §18.3
structural parameters decide array extents and branch selection, and Integer,
Boolean and String parameters seed those decisions for nested components, so
all of them resolve either way. The regression test in
`crates/rumoca/tests/suite_core/parameter_binding_fold_option.rs` pins that
split by asserting the two modes produce the same variables and the same
equation count, differing only in the Real binding.

`static_eval.py --keep-parameter-chains` passes the flag.

## Tests

`packages/modelsan/tests/test_physical.py` — the open domain, multi-variable
predicates, name-blind matching, unit-only rejection, negative-literal folding,
parameter-chain folding (including the `start`, `der`/`pre` and cyclic cases
that must *not* fold), bound suppression, four domains valid *and* invalid, and
provenance.

`crates/rumoca/tests/suite_core/parameter_binding_fold_option.rs` — the
compiler flag: folded by default, unfolded on request, and identical model
shape either way.

## Semantic binding: what an object *represents*

Matching on the declared `quantity` recovers physical semantics cheaply and
automatically, and it remains the first level. It is not always enough, and the
failure is not hypothetical:

```
Nr.Ga = -0.757576   quantity=Conductance   unit=S   confidence=QUANTITY_AND_UNIT
  -> physical-invariant-violated: elec.conductance.positive
```

`Nr` is Chua's diode in `Modelica.Electrical.Analog.Examples.ChuaCircuit`. The
quantity is genuinely Conductance and the unit genuinely S; both agree, at the
highest confidence the matcher can report, and both are beside the point. The
negative slope of the characteristic *is* the device. Quantity-only matching
produced two false positives on a stock MSL example.

The general shape: a unit or quantity says what *kind* of thing something is,
never *which* thing.

```
rad/s  -> angular velocity.  Wheel? Motor shaft? Fan? Joint?
Ohm    -> resistance-like.   Passive resistor, or an equivalent one that may
                             legitimately be negative?
```

### The layer

```
                   RBC Model
                       |
                       v
                Semantic Binder
       user > component type > connector > quantity > unit > heuristic
                       |
                       v
                  Semantic Map          bindings, conflicts, ambiguities
                       |
                       v
                 PhysicalSan rules      written against roles
```

`packages/modelsan/modelsan/semantics/`. A role is an open dotted string, not
an enum — nobody can enumerate in advance that someone will need
`hvac.supply_air_temperature`, and an enum would mean editing the module to add
a domain.

### What each source is for

| Priority | Source | Answers |
|---|---|---|
| 1 | `UserProvider` | anything the model cannot state. Final authority. |
| 2 | `ComponentTypeProvider` | passive or active, from the declaring class |
| 3 | `ConnectorProvider` | torque vs angle, from connector role plus domain |
| 4 | `QuantityProvider` | what physics it is, from `quantity` then `unit` |
| 5 | `NameHeuristicProvider` | a hint. Off by default. |

Priority 2 needed compiler support: the DAE reduces a component to a path
prefix on a name, so the declaring class was simply gone. `flat::Model` now
carries `variable_declaring_classes`, exported as `RbcVariable.declaring_class`
— 100% populated on the models tested, against 73.8% for `quantity`.

### Coverage must not be the price of precision

The obvious fix — require the `component.passive.*` role — would have made
every rule silent on every class nobody has catalogued. So the suppressing
claim is the one that must be explicit:

```python
confirming_roles = {roles.PASSIVE_CONDUCTANCE}   # premise established
excluded_roles   = {roles.ACTIVE_CONDUCTANCE}    # premise refuted
```

A rule may still flag the declared quantity where nothing is known either way —
a negative resistance is unusual by default — but it must be a low-severity
advisory question rather than an error. It must not cause a failing exit status
or enter the confirmed-bug count. Only a component/delegated contract, explicit
user assumption, or intent-independent executable failure establishes an error.
A reader triaging a thousand findings can tell the two apart, and the evidence
that separated them travels in the finding. The rationale and required wording
are documented in [Aggregate rules and signed domains](../method/aggregate-and-signed-domains.md#why-keep-an-advisory-at-all).

### What the binder refuses to do

**Guess between candidates.** Several objects filling one inferred role yields
an `Ambiguity` and no binding, because binding the first would make a rule's
verdict depend on declaration order. A *user* glob matching four wheels is
exempt: that is one deliberate statement, not a guess.

**Overrule a member that labelled itself.** The connector inference is a guess
about a *neighbourhood*, not a statement about a member, and asserting it
regardless produced **640 spurious conflicts** over the corpus:

```
458  physical.position [connector]  vs  physical.length [quantity]
 90  physical.absolute_temperature [connector]  vs  physical.pressure [quantity]
 32  physical.position [connector]  vs  physical.velocity [unit]
```

Three separate errors, found only by running it at scale:

- `Thermal.FluidHeatFlow.Interfaces.FlowPort.p` is a **pressure**. The class
  path merely contains the word Thermal.
- `Electrical.Analog.Basic.VariableResistor.R` is a **`RealInput`**, marked
  `potential` because it is not a flow member. A causal signal carries no
  conservation law for "potential" to mean anything about; its unit says `Ohm`.
- `position` and `length` were reported against each other, though they are one
  claim at two specificities.

So a connector rule now stands down where any metadata *about that member* —
quantity or unit — genuinely disagrees, and `COMPATIBLE` in `role.py` names the
pairs that only appear to. This is not a change to the priority order: connector
context still outranks quantity as an authority. It is the rules being less
willing to speak.

**Silently accept a contradiction.** A user mapping always wins — the user
knows the application — but where the model's own metadata can check it, the
disagreement is reported:

```
semantic binding conflict on w_fan
  using   w_fan -> automotive.wheel.radius [user: origin=semantics.toml]
  ignored w_fan -> physical.angular_velocity [quantity: quantity=AngularVelocity]
  the model's own metadata makes this physical.angular_velocity, but
  automotive.wheel.radius is a physical.length; using the explicit user binding
```

Only checked where the model can actually check it. Nothing in a model can
confirm or deny that a given angular velocity is a *wheel's*.

**Swallow a typo.** A user mapping matching no variable is reported. Otherwise
the mapping never applies, the rule never fires, and the model reads as clean.

### Profiles are not bindings

`profiles = ["automotive"]` says those rules are relevant. It does not say
which variable is the vehicle speed. `auto.wheel.radius.positive` declares
`quantities=frozenset()` — no fallback, because `Length` is shared by a wheel
radius and every other length in a vehicle — so it fires only on a bound role.
Without the mapping the checker does not know which length is a wheel, and says
so by not firing.

### The map is a shared artifact

```python
bind_semantics(model, config=SemanticConfig.load("semantics.toml"))
model.semantics.get("automotive.vehicle_speed")
```

Not private to PhysicalSan: connector logging, differential analysis, fault
injection, model slicing and runtime monitoring all ask the same question.

### Demonstration and tests

`tools/demo/semantics/run.py` runs all three cases against a real compile, plus
the removed false positive, a conflict and an ambiguity.

`packages/modelsan/tests/test_semantics.py` — open roles and namespace-bounded
refinement, quantity over unit, the passive/active split, family-vs-exact
precedence, connector inference, user globs, heuristics off by default,
mistyped mappings, conflicts, ambiguity and its user-glob exemption, severity
grading, and a profile rule that needs a binding to fire at all.
