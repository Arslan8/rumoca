# TOOLBUG-018: the analysis IR lowered every declaration to an indistinguishable Real

| | |
|---|---|
| **Component** | `rumoca-ir-flat`, `rumoca-bitcode` schema and export, `modelsan.divisor` |
| **Severity** | High — a whole class of unreachable zero witnesses |
| **Found by** | Independent review of the published reports, 2026-09-16 |
| **Status** | Fixed. `RbcSymbolContract` carried per symbol; 10 regression cases in `tests/test_symbol_contract.py`. |

## The defect

By the time a variable reached the analysis it had `role` — the MLS Appendix-B
partition its coordinate belongs to — and nothing else about what the
declaration promised. `constant` and `parameter` are both role `parameter`, so
the two were indistinguishable, and `final`, `protected` and `Evaluate=true`
were not carried at all.

A divide-by-zero search reading only `role` proposes setting
`Modelica.Constants.pi` to zero, and did.

| Report | Symbol | Why it is unreachable |
|---|---|---|
| FINDING-01566 | `constant Real pi` | immutable, and nonzero |
| FINDING-01568 | `constant Integer m = 3` | a phase count cannot become zero |
| FINDING-01551 | `final parameter ZsRef = 1` | no modifier can override it |
| FINDING-01137 | `protected constant Lme = 1` | immutable equivalence scale |
| FINDING-04781 | `constant unitTime = 1` | a unit-conversion constant |
| FINDING-05098 | `constant vRef = 1` | a fixed reference scale |

## What the IR now carries

`RbcSymbolContract`, per symbol, preserved through flattening:

| Field | Question it answers |
|---|---|
| `variability` | constant / parameter / discrete / continuous |
| `is_final` | may a *modifier* override this declaration |
| `is_protected` | who may see it |
| `evaluate` | the MLS §18.3 substitution hint |
| `structural` | does changing it require retranslation |
| `effective_value` | the binding's value where it is statically evaluable |
| `binding_depends_on` | the symbols the binding reads |
| `binding_from_modification` | declaration or applied modifier |
| `declared_in` | the class that declared it |

Bounds were already carried, and array, alias and `extends` cases are covered
because the contract is attached to the *flattened* symbol rather than to a
source declaration.

### One conflation removed in the compiler

Flat's `evaluate` flag meant `annotation(Evaluate=true)` **or** `final`:

```rust
pub(crate) fn has_evaluate_annotation(comp: &ast::Component) -> bool {
    if comp.is_final { return true; }        // <- the conflation
    comp.annotation.iter().any(is_evaluate_true_annotation)
}
```

These are different promises. `Evaluate=true` says a value may be substituted
at translation time; `final` says a modifier may not override the declaration.
A consumer asking "can this change" needs the second and gets the wrong answer
from the first. `Variable::is_final` is now carried separately, and `evaluate`
keeps its original meaning with the distinction documented at both ends.

## The suppression rule

Deliberately narrow, and it is the rule the review asked for:

> Suppress only when the **complete effective binding and dependency chain**
> proves the denominator cannot be zero — not merely because a symbol is
> constant, final, or protected.

So each prefix is read for exactly what it says:

* `constant` fixes the value **provided everything its binding reads is also
  fixed**.
* `final` closes the declaration to modifiers, not the binding.
  `final parameter d = p` is reachable by setting `p`, and is reported.
* `protected` is visibility. A `protected parameter` is settable before
  translation and is reported.
* `Evaluate=true` is a hint. A structural parameter may be given another value
  and the model retranslated.

Every rejected witness records **why**, and the reason names the chain:

```
imc.pi     settable=False   declared constant
imc.ZsRef  settable=False   declared final, so no modifier can override it
imcData.m  settable=True    (settable)
```

## Not over-corrected

Four cases must still be reported, and each is a test:

| Case | Result |
|---|---|
| `constant Real c = 0; y = 1/c` | reported — `divisor-zero-at-declared-values` |
| `protected parameter Real p = 0; y = 1/p` | reported — protected is not immutable |
| `parameter p = 1; final parameter d = p; y = 1/d` | reported — reachable through `p` |
| `parameter p = 1; y = 1/p` | reported |

The first of these exposed a second defect while being written: the detector
asked for a witness *before* checking the baseline, so a denominator that was
already zero had no knob to turn and was dropped entirely. A guaranteed
division by zero was the one case it could not see.

## And a third defect, from fixing the second

Checking the baseline first then reported 8 sites where the denominator is zero
as declared **and the division is guarded** — `if F > 0 then a/F else b` is
written precisely so the zero case is never divided by. The baseline check now
applies the same path analysis as the witness check.

## Where this leaves one cited case

`Lme` occurs twice in MSL and the two want opposite answers:

* `DC_PermanentMagnet.mo:38` — `constant SI.Inductance Lme = 1`. Immutable,
  suppressed, as the review asked.
* `DC_SeriesExcited.mo:84` — `protected final parameter SI.Inductance
  Lme = Le*(1 - sigmae)`. Final and protected, but its binding reads `Le` and
  `sigmae`, which are ordinary parameters.

The review's table asks for the second to be suppressed; the review's stated
rule — *"continue analyzing dependencies of final parameters; do not blindly
mark every final value safe"* — requires it to be analysed. We followed the
rule: the witness names `Le` or `sigmae`, which is the knob a user can actually
turn, and suppressing it would hide a reachable zero behind a `final` that does
not prevent it. This is flagged rather than decided silently.
