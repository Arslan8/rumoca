# Physical intent: a predicate and the authority to apply it

A physical rule is two facts, and the analyzer had been carrying one.

1. **The predicate.** `R > 0`.
2. **The authority for applying it here.** An explicit passive-resistor
   contract, a user assumption, or merely the fact that the value has unit
   `Ohm`.

An SI quantity identifies what kind of value something is. It does not identify
what the component is for. `SI.Resistance` describes a passive resistor, an
active negative impedance, a linearised incremental model, an optimisation
variable and a fault-injection input. Without the component, the analyzer does
not know the author's intent — and a checker that asserts one anyway reports
`Nr.Ga = -0.76` in a stock MSL example as a defect, at its highest confidence,
with the quantity and the unit both agreeing and both beside the point.

## Three states, carried, never collapsed into a severity

| Premise | Meaning | Result |
|---|---|---|
| `established` | a component contract, a delegated one, or a user assumption applies | enforce the predicate |
| `refuted` | an authoritative contract permits the value | no violation; a non-defect record |
| `unknown` | only quantity, unit or a name matched | a non-blocking question |

The state, the authority, the matched role and the canonical declaration travel
in the IR and in the published finding. Encoding the distinction only as a
severity would let a later stage turn an advisory back into an error by
changing one number.

## What this is not

It is **not** a fix for false positives by suppression. Suppressing every
unknown case would raise apparent precision by destroying recall: the negative
resistance nobody catalogued is exactly the thing worth surfacing. The signal
is preserved and re-addressed — to the author, as a question:

> `mystery.R` holds -1, which is unusual for a resistance — but nothing
> declares what this component is, so the analyzer cannot tell whether it is
> intended. Is it? If so, declare it: add a component contract or a
> `[[contracts]]` entry with the intended `sign_domain`. If not, bound the
> declaration.

## Authority order

Lower authorities cannot contradict higher ones.

1. **Intent-independent source facts** — an active denominator that becomes
   zero. No physical assumption waives this. A `[[contracts]]` entry declaring
   an area `signed` and `allowed` does not stop `1/area` being reported.
2. **Source declaration bounds and assertions.**
3. **Explicit user assumptions.** The author is supplying missing application
   intent.
4. **Component and delegated-component contracts**, including those inherited
   through arrays and wrappers: a polyphase resistor's premise belongs to
   `Analog.Basic.Resistor.R`, and the canonical declaration is carried so the
   wrapper cannot forget it.
5. **Quantity and unit.**
6. **Name heuristics**, opt-in and off by default.

The operative rule: **component semantics override a generic physical
heuristic.** A catalogued signed resistor does not inherit a generic
`Resistance > 0` verdict. An uncatalogued resistance stays visible, as an
intent question.

## Finding policy

| Evidence | Kind | Severity | Blocking |
|---|---|---|---|
| established contract violated by an observed or default value | `physical-invariant-violated` | high | yes |
| established contract not enforced by the declaration | `physical-domain-unenforced`, `physical-bound-permits-zero` | medium / low | not until independently confirmed |
| unknown premise, suspicious value or permissive declaration | `physical-intent-question` | low | no |
| authoritative contract permits the value | `physical-rule-does-not-apply`, `physical-zero-is-a-supported-limit` | low | no |
| executable arithmetic fails independently | `divisor-reachable-zero` and the confirmed tier | high | yes |

An advisory carries `premise_state`, `authority`, `semantic_role`,
`canonical_declaration`, `contract_source`, the observed value or the
permissive bound, an `observation` field saying which of the two paths produced
it, and the question itself. An advisory-only run exits zero. Advisories are
excluded from the defect population in `tools/sweep/precision_table.py` and are
never described as "physics forbids this value".

## Zero contracts excuse zero

`ALGEBRAIC_LIMIT` and `FEATURE_DISABLED` are statements about *zero*: an
inductance of zero is an ideal short, a conductance of zero disables a loss
term. They do not excuse `-1`. `ALLOWED` is the different and stronger
statement that the quantity rule does not bind this component at all, and it
refutes the premise for any value. The two are kept apart by a test, because
collapsing them is the easy mistake and it silently drops negative-value
findings.

## Regression fixtures

| Case | Expected |
|---|---|
| `Basic.Resistor.R` negative | no positivity violation; the contract is signed |
| Chua `Nr.Ga < 0` | no passive-conductance error; the negative slope is the device |
| `SwitchedCapacitor.R = -1` | no sign error; either sign is documented |
| polyphase resistor, negative element | inherits the scalar signed contract |
| machine winding `R = 0` | accepted; the claim is `>= 0` |
| machine winding `R < 0` | still reported |
| negative off-diagonal inertia entry | the assembled tensor is evaluated, not the entry |
| `Basic.Inductor.L = 0` | accepted algebraic ideal-short limit |
| uncatalogued `Resistance = -1` | exactly one low advisory, `premise_state=unknown` |
| uncatalogued `Mass = -1` | the same; not special-cased to electrical names |
| user `sign_domain = "nonnegative"`, value `-1` | promoted to an established violation claiming `>= 0` |
| user `sign_domain = "signed"` | refutes the generic heuristic |
| `1/area` with a user contract calling `area` signed and allowed | still a divide-by-zero |

Held in `packages/modelsan/tests/test_intent_policy.py`, with the premise
matrix — both paths, all three states — in `tests/test_physical.py`.

## A defect found while writing these tests

`tests/test_physical.py` collected its failures into a list for a standalone
`main()` and never asserted. Under pytest every test in that module passed
whatever it found. Making `check()` assert immediately surfaced one real
disagreement — the cross-domain case still expected an uncatalogued negative
resistance to be a violation — which is the behaviour this policy changes, and
which the suite had been unable to tell anyone about.
