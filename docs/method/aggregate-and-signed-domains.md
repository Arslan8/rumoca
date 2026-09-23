# Aggregate rules, and sign rules scoped by component

Two false-positive families, **268 reports**, with one cause each.

| Group | Reports | Cause |
|---|---:|---|
| `signed-inertia-tensor` | 182 | the subject of the rule was wrong |
| `signed-polyphase-element` | 63 | the authority for the rule was wrong |
| `signed-machine-data-resistance` | 21 | the rule itself was wrong |
| `signed-electrical-element` | 2 | the authority for the rule was wrong |

## 1. A moment of inertia is not a positive scalar

`Modelica.Mechanics.MultiBody.Parts.Body` declares six fields:

```modelica
parameter SI.Inertia I_11(min=0) = 0.001 "Element (1,1) of inertia tensor";
...
parameter SI.Inertia I_21(min=-C.inf) = 0 "Element (2,1) of inertia tensor";
```

They assemble into

```
I = | I_11  I_21  I_31 |
    | I_21  I_22  I_32 |
    | I_31  I_32  I_33 |
```

and the constraint on *that* object is that it is symmetric positive
semidefinite. The off-diagonal entries are products of inertia: signed, as the
declaration says with `min = -Modelica.Constants.inf`, and zero when the body's
principal axes line up with the frame, which is the ordinary case.

Checking each field against `> 0` was wrong in both directions. It reported 182
valid tensors, and it would have passed an invalid one:

```
[[1, 2, 0],
 [2, 1, 0],
 [0, 0, 1]]
```

Three positive diagonal entries, every scalar rule satisfied, eigenvalues
−1, 1, 3.

### What the pass does

`modelsan/physical/aggregate.py` groups the six fields by component instance
and declaring class. Recognition requires **all six**: a class declaring three
of them is not this idiom and keeps the scalar rule, because suppressing a rule
on a partial match is how a real defect goes quiet.

For a numerically resolvable tensor it checks every value is finite, assembles
the symmetric matrix, and tests positive semidefiniteness with a scale-relative
tolerance (`1e-12 * max|entry|`) over **all** principal minors:

```
I_11 >= 0        I_11*I_22 - I_21^2 >= 0
I_22 >= 0        I_11*I_33 - I_31^2 >= 0        det(I) >= 0
I_33 >= 0        I_22*I_33 - I_32^2 >= 0
```

Not the leading minors alone: Sylvester's criterion with leading minors decides
positive *definiteness*. `[[0,0,0],[0,1,0],[0,0,-1]]` has leading minors
0, 0, 0 and an eigenvalue of −1.

The eigenvalues are computed anyway, in closed form (Smith 1961) so the package
takes no numerical dependency, and travel in the diagnostic.

| Verdict | What happens |
|---|---|
| valid | the scalar findings are suppressed and nothing is reported |
| invalid | **one** finding, `physical-inertia-tensor-not-semidefinite`, naming the violated minor |
| unknown | **one** low-severity `physical-inertia-tensor-undecided`, naming the binding it could not evaluate |

Either way the six fields are *excluded* from the scalar `MomentOfInertia`
rule. Exclusion rather than suppression: the aggregate verdict should be the
only thing said about them.

### A tensor declared only as a matrix

`Parts.BodyBox` computes its inertia from the box geometry and never declares
the six fields, so the group above does not see it — and the scalar rule
compared a 3×3 with zero and reported `boxBody1.I > 0`, which is not a
proposition. A 3×3 declaration carrying a `MomentOfInertia` quantity is
recognised on its own and gets the same treatment.

### Rigid-body realizability is computed and never reported

For any rigid body each principal moment is at most the sum of the other two.
`[[2,-1,0],[-1,2,0],[0,0,1]]` has principal moments 1, 1, 3, so 3 > 1 + 1 — and
the specification requires that tensor to **pass**. The check is therefore a
diagnostic field (`rigid_body_realizable`) and never a verdict. A test pins
that, because the tempting version of this rule fails a tensor the library
uses.

## 2. One quantity, three contracts

`SI.Resistance` is declared by a passive resistor, by a negative-impedance
converter, by a machine winding and by anything else measuring ohms. A rule
keyed on the quantity gives all four the same answer.

| Component | Domain | Why |
|---|---|---|
| `Basic.Resistor.R` | signed | "The Resistance R is allowed to be positive, zero, or negative" |
| `Basic.Conductor.G` | signed | the same sentence, for conductance |
| `Polyphase.Basic.Resistor.R` | signed | an array of `Analog.Basic.Resistor`; inherits the scalar contract |
| machine winding resistance | **nonnegative** | copper cannot be negative; zero is the ideal lossless winding |
| explicit passive component | positive | the passive premise, established by the declaring class |
| active negative resistance | signed | the negative slope is the device |
| unknown | advisory only | see below |

The machine winding is the case neither existing answer covered. Reporting
`Rs > 0` made an idealisation the machine examples use deliberately look like a
defect; marking it unrestricted would have stopped a negative stator resistance
being reported at all. `elec.machine_winding_resistance.non_negative` says
`>= 0`, and the 20 findings that used to claim `> 0` now claim `>= 0`.

### A quantity match is not a component

Where no declaring class establishes the premise, a violated invariant is
reported as `physical-invariant-violated-by-quantity-alone` at low severity,
carrying the same evidence and a `premise` field saying so. Component-type
semantics outrank the quantity heuristic; the heuristic may advise and may not
confirm.

### Why keep an advisory at all?

A negative resistance, mass-like value or other unusual sign is worth showing
to the programmer, but it is not automatically an error. A static analyzer
knows the unit and perhaps the broad physical quantity; it does not know the
programmer's intent. The value may represent an active device, a linearized
incremental model, an optimization intermediate, a fault-injection case, or a
deliberate nonphysical test. Even when none of those interpretations seems
likely, likelihood is not a component contract.

The fallback heuristic therefore exists to ask a question, not to deliver a
verdict:

> Negative resistance is unusual for an uncatalogued component. Is this
> intentional? Add a component contract or an assumption to declare the
> intended signed domain.

This distinction is part of the analyzer's public contract:

| Evidence | Result |
|---|---|
| explicit component/delegated contract or user assumption is violated | error: the program contradicts a stated premise |
| executable source arithmetic fails, such as an active division by zero | error: the failure does not depend on guessed physical intent |
| only quantity, unit or name suggests the value is implausible | advisory warning: ask whether it was intended |
| component contract explicitly permits the value | no violation; optionally retain a non-defect audit record |

An advisory must not say “resistance must be positive,” contribute to the
confirmed-bug count, or cause a failing exit status. It must carry the uncertain
premise, the evidence used to infer it, and the question for the user. If the
user answers that the value is unintended, that decision becomes an explicit
assumption or component contract; subsequent violations can then be errors.

This preserves the useful signal without pretending that the analyzer knows
more about the model than its author.

## 3. Assumption fallback

The same `[[contracts]]` table as the
[zero-behaviour contracts](zero-behavior-contracts.md), with three more keys:

```toml
[[contracts]]
match = "declaration"
target = "MyLibrary.Body.I"
aggregate = "symmetric_inertia_tensor"
domain = "positive_semidefinite"
reason = "Rigid-body inertia tensor about the center of mass"

[[contracts]]
match = "declaration"
target = "MyLibrary.Motor.Rs"
role = "machine_winding_resistance"
sign_domain = "nonnegative"
reason = "Copper resistance; zero permits an ideal lossless winding"

[[contracts]]
match = "declaration"
target = "MyLibrary.NegativeImpedance.R"
role = "active_resistance"
sign_domain = "signed"
```

`zero_behavior` is required only of an entry that makes no other statement: an
entry carrying `aggregate` or `role` is about something else and is not made to
invent one. An unknown `aggregate`, `role` or `sign_domain` is **refused**, for
the same reason a misspelt `zero_behavior` is — an entry that silently does
nothing is worse than one that fails loudly.

A `role` entry reaches the semantic binder at `USER` authority, through
`UserDeclarationProvider`: it keys on the declaring class, where the existing
`UserProvider` keys on the flattened instance path. Every decision that used
one keeps the configuration file, the target and the reason in its diagnostic.

## Effect

| | before | after |
|---|---:|---:|
| `physical-bound-permits-zero` | 295 | 207 |
| `physical-zero-is-a-supported-limit` | 2973 | 2695 |
| `physical-domain-unenforced` | 664 | 655 |
| inertia tensors reported | 278 scalar findings | 18 undecided, 0 invalid |
| **findings** | **5860** | **5503** |
| **defect claims** | **2468** | **2371** |

No inertia tensor in the corpus is invalid, and none of the 18 undecided ones
is undecided for an interesting reason: they are bound to `resolveDyade1(...)`
or to an index into a computed matrix, neither of which this analysis
evaluates.

Of the external review's 3304 false positives, **3007 (91%)** are now either
not reported or reported under a kind that makes no defect claim. Of the four
groups this work targeted, `signed-inertia-tensor` (182),
`signed-polyphase-element` (63) and `signed-electrical-element` (2) are fully
resolved. `signed-machine-data-resistance` keeps 19 of its 21, by design: the
specification asks for zero to be allowed and negative values still reported,
and those 19 now claim `>= 0`.
