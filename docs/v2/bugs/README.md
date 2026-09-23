# Bugs, one file per instance

Every instance this project reports, at every strength of evidence, as a file that can be opened, linked and argued with. Each one names **which sanitizer found it** and carries the commands to check it.

> **The total is not the number to quote.** These are three different kinds of claim and merging them would be dishonest — 26 are proven, the rest are reach.

| Tier | Meaning | Instances |
|---|---|---|
| **Confirmed** | fails under **two independent tools**, and the model is clean at its declared values | 26 |
| **Candidate** | static analysis of the canonical DAE reached it; **no execution has decided it either way** | 5503 |
| **Latent** | a declaration *permits* a physically impossible value; **nothing has been observed failing** | 911 |

**6440 files total.**

## Which sanitizer found what

This is the column a reader usually wants first: it says which detector is responsible, and therefore which one to doubt.

| Sanitizer | What it does | Instances |
|---|---|---|
| [PhysicalSan](by-sanitizer/physical.md) <br>`packages/modelsan/modelsan/sanitizers/physical.py` | binds each variable to a physical role from its `quantity`, unit and declaring class, then checks the domain invariant that role carries | 3593 |
| [DivisorSan](by-sanitizer/divisor.md) <br>`packages/modelsan/modelsan/sanitizers/divisor.py` | proposes an assignment for each division's **complete denominator**, substitutes it and evaluates: a finding exists only when the denominator actually comes out zero, under values the declarations, assertions and branch conditions all permit | 1935 |
| [SI type-bound census](by-sanitizer/type-census.md) <br>`tools/sweep/min0_census.py` | the same bound rule PhysicalSan applies, run over the library's *declarations* rather than over one model's variables | 911 |
| [the parameter probe + SolverSan](by-sanitizer/probe.md) <br>`packages/modelsan/modelsan/sanitizers/solver.py` | sets one parameter to a suspect value, runs the model, and reports a solver or initialization failure that the declared values do not produce | 1 |

## By finding kind

| Kind | Instances | Asserts |
|---|---|---|
| `physical-zero-is-a-supported-limit` | 2018 | the positivity rule does **not** apply: this component documents zero as a meaningful limit, so a missing-bound claim would contradict its contract |
| `divisor-reachable-zero` | 1475 | a permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it |
| `declaration-permits-impossible-value` | 911 | the type supplies no lower bound and the declaration adds none, so this parameter accepts a value that is not a physical quantity |
| `physical-rule-does-not-apply` | 681 | the component documents this quantity as taking the value it holds, so the rule derived from the SI quantity alone does not bind it |
| `physical-intent-question` | 638 | the value or the declaration is unusual for the **quantity** it declares, and nothing says what this component is — so this is a question for the author, not a claim about the model |
| `physical-domain-unenforced` | 204 | nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones |
| `divisor-zero-unresolved` | 127 | an assignment drives the denominator to zero, but whether the division is evaluated there could not be decided from the artifact |
| `divisor-guarded-by-assertion` | 122 | the denominator can be zeroed arithmetically, but the model asserts it is bounded away from zero, so the assignment is one the model already rejects |
| `divisor-unreachable-under-witness` | 121 | the assignment that zeroes the denominator also makes the branch containing the division unreachable, so the division is never evaluated at that value |
| `divisor-zero-when-parameters-equal` | 45 | the denominator is a difference, so it vanishes when the two sides are equal; no `min` on either can express a constraint between two parameters |
| `divisor-introduced-by-translation` | 41 | zero is a supported limit of this component; the quotient the DAE shows is the compiler's solved form, not a division in the source |
| `physical-bound-permits-zero` | 34 | the declaration carries `min=0`, and the physical role bound to this variable requires strictly greater than zero |
| `physical-inertia-tensor-undecided` | 18 | this component's inertia tensor could not be assembled from values this analysis can resolve, so **neither its validity nor its invalidity is claimed** |
| `divisor-zero-at-declared-values` | 4 | the denominator is zero at the model's own declared values |
| `solver-failure` | 1 | setting this parameter to a value its declaration permits makes the solver fail, in two independent tools, where the declared values run clean |

## Have these been checked?

Yes, by running the commands the reports themselves print — extracted from the published markdown, not from the generator, so a report whose steps do not execute is caught:

```console
$ python3 tools/sweep/verify_bug_reports.py --tier confirmed --all
$ python3 tools/sweep/verify_bug_reports.py --tier latent --all
$ python3 tools/sweep/verify_bug_reports.py --tier candidate --sample 400
```

| Tier | Checked | Result |
|---|---|---|
| Confirmed | all 26 | 26 ok |
| Latent | all 911 | 911 ok |
| Candidate | 400 of 5142, sampled | 400 ok |

"ok" means the commands run and produce what the report says they will — for a latent report, that the declaration line opens and its type really carries no `min`; for a candidate, that the sanitizer still reports a finding naming the same target. It does **not** mean the finding is a real defect: that is what the tier says, and for the candidate tier nothing has decided it.

## Verifying any of these

Every report carries its own commands. They all reduce to one tool, which compiles a single model and runs a single sanitizer over it:

```console
$ python3 tools/sweep/check_one.py <model> --target <name> --sanitizer <sanitizer>
```

Prerequisites, and the known weak points of each tier, are in [VERIFY.md](../../VERIFY.md). The corpus runs these reports were generated from are in [runs/data/](../../runs/data/), so a disagreement can be traced to a row rather than argued about.

## Naming

| Prefix | Tier |
|---|---|
| `BUG-nnn` | confirmed |
| `FINDING-nnnnn` | candidate |
| `DECL-nnnn` | latent |

## What changed since the last run

[withdrawn.md](withdrawn.md) lists the findings that stopped reporting and the ones that started, with why. None were withdrawn for being wrong; the compiler fixes made array equations and call arguments visible, which moved attribution from the propagated parameter to the one that actually divides.

The root-cause argument for a confirmed instance — why the declaration is wrong, and what the fix is — lives in [`../verified bugs/`](../../verified%20bugs/). These files are the *instances*; that directory holds the *fix sites*.

