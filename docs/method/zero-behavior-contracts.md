# Shared zero-behaviour contracts

Implementation note. DivisorSan, PhysicalSan and StructureSan share one
classification of what zero means for a parameter, because three separate
opinions produced **1448 false positives across ten component families**.

`Inductor.L` reaches a denominator in the *solved* DAE, so DivisorSan called it
a divide-by-zero. Its declared quantity is an inductance, so PhysicalSan called
it a missing positivity bound. The library documentation says plainly that `L`
may be zero, at which point the element is an ideal short. Two of the three
were wrong about the same parameter, for different reasons.

## The contract

```
ZeroBehavior:  DIRECT_DIVISOR | ALGEBRAIC_LIMIT | FEATURE_DISABLED
               ALLOWED | FORBIDDEN | UNKNOWN
```

| Behaviour | Meaning |
|---|---|
| `DIRECT_DIVISOR` | zero reaches an active denominator **written in the source** |
| `ALGEBRAIC_LIMIT` | zero turns a differential relation into an algebraic constraint |
| `FEATURE_DISABLED` | zero removes an optional term, leaving the rest intact |
| `ALLOWED` | zero is explicitly supported, without more specific semantics |
| `FORBIDDEN` | a bound or an assertion excludes zero |
| `UNKNOWN` | insufficient evidence — never treated as safe |

Every result carries `behavior`, `confidence` (`PROVEN | DECLARED | ASSUMED`),
`source` (`equation | bound | class_catalog | user_config`), `reason`,
`canonical_declaration` and, for a user contract, the file and rule that
supplied it.

## Inference, from source-origin equations only

```modelica
L*der(i) = v;                      ALGEBRAIC_LIMIT — at zero, v = 0
m*a = flange_a.f + flange_b.f;     ALGEBRAIC_LIMIT — at zero, a force balance
Q_flow = G*dT;                     FEATURE_DISABLED — at zero, no heat
flow = level/resistance;           DIRECT_DIVISOR — proven
```

Six rules, each of which a case in the corpus requires:

1. **Every use, not one.** A parameter may multiply in one equation and divide
   in another.
2. **A direct reachable denominator overrides any safe multiplicative use.**
   `p*der(x) = 1` alongside `y = x/p` is a divide-by-zero.
3. **Propagate through wrappers and bindings.** `Rotational.Examples.First`
   binds `inertia1.J = Jmotor`; `Jmotor` appears in no equation, and must
   inherit the contract of what it configures or the rule fires on the knob
   while being suppressed on the component.
4. **Source equations, not solved ones.** `L*der(i) = v` contains no division.
   The DAE's `der(i) = v/L` is the compiler's.
5. **`min=0` proves nothing.** Permitting zero is the absence of a statement,
   not a statement.
6. **Ambiguous is `UNKNOWN`.**

A derivative may be one step away: `Mass` writes `m*a = f` with `der(v) = a`
alongside, so a variable that *is* a rate under another name counts as one.

### Two rules added after the first corpus run

7. **The *denominator* has to be able to vanish.** `SwitchedCapacitor` writes
   `C = clock/max(eps*oneOhm, abs(R))`. Tagging `R` as a `DIRECT_DIVISOR`
   because it sits under a `/` is
   [TOOLBUG-017](../toolbugs/TOOLBUG-017-divisor-reported-parameters-not-denominators.md)
   happening again one layer down, and the wrong tag then outranked the
   catalogue entry saying this component represents a *signed* resistance. The
   denominator's interval is checked before the tag is applied; a denominator
   provably bounded away from zero yields `guarded-divisor`, which claims
   nothing.

8. **A declaration that names zero has spoken about zero.**
   `CoreParameters.GcRef = if PRef <= 0 then 0 else PRef/VRef^2/m` with
   `PRef(min=0) = 0` ships at zero, and `Losses.Core` writes
   `if PRef <= 0 then Gc = 0` beside it. Either a binding that evaluates to
   zero or a conditional with a literal zero branch yields
   `FEATURE_DISABLED`/`DECLARED` at `BOUND` authority — below a proven source
   division, above the catalogue. The default run folds parameter bindings
   before the sanitizers see them, so this fires only with
   `--keep-parameter-chains`; in the folded run the catalogue carries the same
   conclusion.

## Authority

```
hard source arithmetic
    > explicit source bounds and assertions
    > user contract
    > component catalog
    > quantity/unit heuristic
```

A user assumption may override a heuristic or a catalog entry. It may **never**
override a proven active source division — asserting a parameter is safe does
not stop the source dividing by it. That is a test, not a convention.

## Assumptions

Added to the existing semantics file, not a new configuration system:

```toml
[[contracts]]
match = "declaration"
target = "Modelica.Electrical.Analog.Basic.Inductor.L"
zero_behavior = "algebraic_limit"
sign_domain = "nonnegative"
reason = "Zero produces the ideal-short algebraic constraint v=0"

[[contracts]]
match = "instance"
target = "plant.optionalLoss.G"
zero_behavior = "feature_disabled"
reason = "Zero disables this optional loss model"
```

`match` is `declaration` or `instance`; a `*` makes it a pattern, which is
recorded as `prefix` and marked lower confidence. An unknown `zero_behavior` is
an error rather than a silent no-op. Unmatched assumptions are warned about.

```console
$ tools/sweep/check_one.py <model> --assumptions semantics.toml
$ tools/sweep/check_one.py <model> --no-assumptions        # source-proved only
$ tools/sweep/check_one.py <model> --explain-contract L
```

`--explain-contract` prints every candidate with its authority and marks the
winner:

```
L.L
 -> [5] ...Inductor.L: algebraic_limit (proven, from equation) — the parameter
        multiplies a derivative, so at zero the differential relation becomes
        an algebraic constraint rather than an undefined quotient
    [3] ...Inductor.L: algebraic_limit (assumed, from user_config) — Zero
        produces the ideal-short algebraic constraint v=0 [semantics.toml]
    [2] ...Inductor.L: algebraic_limit (declared, from class_catalog) — ...
```

## What each detector does

**DivisorSan** reports `DIRECT_DIVISOR`; suppresses a source divide-by-zero for
`ALGEBRAIC_LIMIT` and labels the DAE's reciprocal `generated-division`; returns
unresolved for `UNKNOWN`.

**PhysicalSan** does not apply a blanket `> 0` rule to `ALGEBRAIC_LIMIT` or
`ALLOWED`, reporting `physical-zero-is-a-supported-limit` with the contract
instead. Sign rules follow the component-specific contract, not the SI quantity
alone.

Both of its paths consult the contract, and this was a defect for one run:
the loop over declarations that *permit* a forbidden value asked, and the loop
over declarations that already *hold* one did not. See
[TOOLBUG-022](../toolbugs/TOOLBUG-022-a-violated-invariant-never-consulted-the-contract.md).

The two paths ask different questions, and the difference is load-bearing:

- **a zero contract excuses zero, and only zero.** `ALGEBRAIC_LIMIT` and
  `FEATURE_DISABLED` are statements about what happens at zero. A negative
  inductance is not made acceptable by a component documenting that zero is an
  ideal short, so those behaviours suppress a violation only when the observed
  value is exactly zero;
- **`ALLOWED` says the quantity rule does not bind this component at all.**
  `SwitchedCapacitor` is documented as representing "a positive or negative
  resistance" and `CauerLowPassSC` instantiates four of them at `R = -1`. That
  is reported as `physical-rule-does-not-apply`, a distinct kind, because it is
  a distinct statement.

**StructureSan** reports `STRUCTURE_DEGENERATES_AT_ZERO` — a *topology-specific*
observation about this model — and does not convert it into a universal
declaration constraint. It grades the evidence:

- `matching-shortfall` is a **proof**. Setting `p = 0` deletes every term
  `p * X` and every incidence that existed only through such a term; the graph
  is re-matched without those edges, and a smaller maximum matching means that
  many unknowns have no equation left to determine them.
- `scales-a-rate` is the **shape**, not a proof: the parameter multiplies a
  rate, so at zero a state and its equation go together. That is balanced in
  general and singular in particular models, and it is the shape every
  execution-confirmed instance of this kind has. Deciding it needs execution.

Keeping both matters. The matching test alone reports nothing for
`Mechanics.Translational.Examples.Damper` at `mass1.m = 0`, which OpenModelica
and Rumoca both fail on: that failure is an algebraic rank singularity, which a
structural matching cannot see and does not claim to.

## Regression suite

`packages/modelsan/tests/test_zero_contracts.py`, one test per family:

| Family | Historical reports | Expected |
|---|---:|---|
| ideal switch `Ron`/`Goff` | 748 | `ALLOWED` |
| zero inductance | 237 | `ALGEBRAIC_LIMIT` |
| zero capacitance | 190 | `ALGEBRAIC_LIMIT` |
| zero rotational inertia | 155 | `ALGEBRAIC_LIMIT` |
| zero translational mass | 70 | `ALGEBRAIC_LIMIT` |
| zero spring stiffness | 25 | `FEATURE_DISABLED` |
| zero thermal conductance | 20 | `FEATURE_DISABLED` |
| signed basic resistor | 1 | `ALLOWED` |

And four that must still report: a plain reciprocal, a reciprocal whose
parameter also multiplies a derivative, a reciprocal on a `min=0` parameter,
and the confirmed tank-resistance and op-amp-rail cases.

## Acceptance criterion

**Every suppression says whether zero safety was proven, declared or assumed,
and which exact contract supplied the conclusion.** A suppression that cannot
say is indistinguishable from a bug, and is tested for directly.
