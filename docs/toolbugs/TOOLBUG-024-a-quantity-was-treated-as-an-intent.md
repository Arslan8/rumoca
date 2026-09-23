# TOOLBUG-024: a quantity was treated as a statement of intent

| | |
|---|---|
| **Component** | `modelsan.physical.{rules,engine}`, `modelsan.sanitizers.physical` |
| **Severity** | High — it asserted an intent the analyzer did not know, on 638 declarations |
| **Found by** | External review of the v2 reports, 2026-09-17 |
| **Status** | Fixed. Premise states carried end to end; 15 cases in `tests/test_intent_policy.py`. |

## The defect

A physical rule is two facts:

1. the **predicate**, `R > 0`;
2. the **authority** for applying it *here*.

The analyzer carried the first and inferred the second. `SI.Resistance`
describes a passive resistor, an active negative impedance, a linearised
incremental model, an optimisation variable and a fault-injection input. The
quantity says what kind of value this is; it does not say what the component is
for.

The violation path had already been split
([TOOLBUG-023](TOOLBUG-023-a-tensor-checked-one-entry-at-a-time.md)). The
`unbounded()` path had not, and it was the larger one: **638 declarations** were
reported as medium-severity domain defects on the strength of a quantity match
alone.

## What the fix is not

It is not suppression. Dropping every unestablished case would have raised
apparent precision by destroying recall — the negative resistance nobody
catalogued is exactly the thing worth surfacing. Nothing was removed: the
corpus total is **5503 before and 5503 after**, and every divisor kind is
unchanged to the finding.

What changed is who the finding is addressed to:

> `mystery.R` holds -1, which is unusual for a resistance — but nothing
> declares what this component is, so the analyzer cannot tell whether it is
> intended. Is it? If so, declare it: add a component contract, or a
> `[[contracts]]` entry naming the intended `sign_domain`. If not, bound the
> declaration.

## Three states, carried

| Premise | Meaning | Result |
|---|---|---|
| `established` | a component contract, a delegated one, or a user assumption | enforce |
| `refuted` | an authoritative contract permits the value | record, never enforce |
| `unknown` | quantity, unit or name only | ask |

They travel in `Match`, in `PhysicalInvariant` and in the published evidence,
beside the authority, the matched role and the canonical declaration — not
collapsed into a severity, so a later stage cannot promote an advisory back
into an error by changing one number. A refuted premise is a *result*: the
engine keeps it in `analysis.refuted` rather than returning `None`, because a
rule that silently does not fire is indistinguishable from one nobody wrote.

## The rung above intent

Gate 5 of the brief — previously confirmed numerical cases must stay confirmed
— is not satisfied by the premise policy on its own, and this is the part that
had to be got right rather than merely implemented.

`LCOscillator.C` is reported as `physical-bound-permits-zero`, its premise is
not established by any component contract, and OpenModelica reports a division
by zero in `C*R`. Under the policy as stated it would have become a question
about intent, and an execution-confirmed arithmetic failure would have been
downgraded.

So the authority order has a rung above every contract: **intent-independent
source arithmetic**. A parameter the source divides by has its premise
established by the division, with authority `source_arithmetic`, and no
declared intent waives it. `LCOscillator.C` and `Multivibrator.R2` keep their
kinds, their severities and their place in the confirmed tier; a
`[[contracts]]` entry calling an area `signed` and `allowed` still does not
stop `1/area` being reported.

## Effect, by category

Same flags, policy the only difference:

| kind | before | after | |
|---|---:|---:|---|
| `physical-zero-is-a-supported-limit` | 2695 | 2018 | ALLOWED now refutes the *sign* premise, not only the zero claim |
| `physical-rule-does-not-apply` | 4 | 681 | where those 677 went |
| `physical-domain-unenforced` | 655 | 201 | 454 had no established premise |
| `physical-bound-permits-zero` | 207 | 23 | 184 likewise |
| `physical-intent-question` | 0 | 638 | the 454 + 184, re-addressed |
| every divisor kind | — | — | unchanged, to the finding |
| **total** | **5503** | **5503** | nothing lost |

The 224 physical findings that keep a defect kind are the ones with a real
premise: 122 machine-winding resistances established by the component
catalogue, and 102 established by a source division.

Against the independent review of the v2 reports: confirmed **829 → 830** (the
extra one is a case that had been timing out at 240 s and resolves at 600 s,
not a policy effect), false positives **3602 → 3373**, unresolved **1822 →
1555**, plus **638 advisories**. The advisories remain indexed and reviewable,
but are separated because an unanswered intent question is neither a defect
claim, a refuted claim, nor a failed attempt to decide an asserted claim.

## A defect found while writing the tests

`tests/test_physical.py` collected failures into a list for its standalone
`main()` and never asserted, so under pytest every test in that module passed
whatever it found. Making `check()` assert immediately surfaced a real
disagreement the suite had been unable to report.

Two smaller ones, both in text a reader sees: `static_eval.py` clipped every
evidence string at 200 characters, cutting an advisory's question off at
"whether it is intende"; and the question lower-cased the quantity identifier
whole, producing "unusual for a translationalspringconstant".

## The weighted precision figure fell, and that is arithmetic

Population-weighted precision over defect claims goes **44.0% → 26.7%**. Both
surviving physical strata are still 100% precise. What changed is the mix: the
two high-precision physical strata shrank from 862 findings to 224, so the
1465-strong divisor stratum at 14.5% now dominates the average.

An aggregate over two populations that behave nothing alike moves when their
relative sizes move, and reporting that as a regression in the detector would
be wrong. The per-stratum table is in
[`../findings/precision.md`](../findings/precision.md), and the advisories are
excluded from the population because a question is not a claim.
