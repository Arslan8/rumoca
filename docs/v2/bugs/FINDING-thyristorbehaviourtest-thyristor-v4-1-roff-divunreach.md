# FINDING-01208: `thyristor_v4_1.Roff` in `ThyristorBehaviourTest`

|  |  |
|---|---|
| **Tier** | **Candidate** — static only, not execution-confirmed |
| **Model** | `Modelica.Electrical.Analog.Examples.ThyristorBehaviourTest` |
| **Reached as** | `thyristor_v4_1.Roff` |
| **Found by** | **DivisorSan** — `packages/modelsan/modelsan/sanitizers/divisor.py` |
| **Reported as** | `divisor-unreachable-under-witness` |
| **Severity** | low |
| **Declaration** | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/Thyristor.mo:59` |
| **Signature** | `divisor:divisor-unreachable-under-witness:exp:448:ca7415e0` |
| **From run** | `docs/runs/data/STATIC_INTENT_DEFAULT.jsonl`, `tools/sweep/static_eval.py` over `tools/sweep/ALL.list`, default flags |
| **Status** | **candidate — no execution has decided it either way** |


## The claim

The assignment that zeroes the denominator also makes the branch containing the division unreachable, so the division is never evaluated at that value.

It does **not** claim that anything is wrong.

## Why DivisorSan fired

DivisorSan proposes an assignment for each division's **complete denominator**, substitutes it and evaluates: a finding exists only when the denominator actually comes out zero, under values the declarations, assertions and branch conditions all permit.

The assignment it found, and the arithmetic that verifies it:

```
denominator            thyristor_v4_1.Roff
witness                thyristor_v4_1.Roff = 0
  found by             set to zero
denominator at witness 0.0
at declared values     980392.1568627452
path condition         not ((thyristor_v4_1.vAK < -thyristor_v4_1.VRRM)) and not ((thyristor_v4_1.vControl < thyristor_v4_1.Voff)) and ((thyristor_v4_1.vControl < thyristor_v4_1.Von))
constraints consulted  thyristor_v4_1.Roff: unbounded
```

The last four lines are the check. A denominator that does not evaluate to zero under the witness is not a finding, and this pass previously reported many that did not.

`constraints consulted` is where a disagreement usually lands. A symbol is only offered as a witness when its declaration permits the value: a `constant` never is, a `final` declaration is not unless its binding reads something adjustable, and `protected` is visibility rather than immutability. The contract behind that decision is carried in the artifact per symbol, so it can be read rather than inferred.


## Evidence

| key | value |
|---|---|
| `denominator` | thyristor_v4_1.Roff |
| `witness` | thyristor_v4_1.Roff = 0 |
| `witness_rationale` | set to zero |
| `denominator_at_witness` | 0.0 |
| `denominator_at_declared_values` | 980392.1568627452 |
| `denominator_range` | [-inf, inf] |
| `path_condition` | not ((thyristor_v4_1.vAK &lt; -thyristor_v4_1.VRRM)) and not ((thyristor_v4_1.vControl &lt; thyristor_v4_1.Voff)) and ((thyristor_v4_1.vControl &lt; thyristor_v4_1.Von)) |
| `verdict` | UNSAT |
| `proof` | the guard not ((thyristor_v4_1.vControl &lt; thyristor_v4_1.Voff)) is false under the witness |
| `constraints` | thyristor_v4_1.Roff: unbounded |
| `note` | reported so the guard can be seen and challenged, not as a defect; zero is outside the domain this division is evaluated in |


## How to verify

**1. Reproduce this exact finding** (seconds):

```console
$ python3 tools/sweep/check_one.py Modelica.Electrical.Analog.Examples.ThyristorBehaviourTest \
      --target thyristor_v4_1.Roff --sanitizer divisor
```

This compiles the one model, runs the one sanitizer, and prints what it finds.
It should print the evidence table above.

The flags matter and are not optional: they are the ones the run in the header
used. Adding `--keep-parameter-chains` keeps derived parameter bindings
symbolic, which changes *which* parameter a divisor finding names, so a
reproduce command with different flags can legitimately print nothing.

**2. Read the declaration it points at.** The finding is about what the
declaration permits, so this is the check that decides whether it is right:

```console
$ sed -n '59p' "target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/Thyristor.mo"
```

That line is the declaration. Read its `min`: a declaration with no `min`, or
with `min=0`, permits the trigger value. Check the *type* too — a bound can be
inherited, and an inherited bound would refute the finding.

**3. See it in the IR, if the claim is about reach rather than a bound:**

```console
$ python3 tools/sweep/check_one.py Modelica.Electrical.Analog.Examples.ThyristorBehaviourTest --keep-artifact /tmp/m.rbc \
      --sanitizer divisor >/dev/null
$ ./target/debug/rumoca bitcode disasm /tmp/m.rbc | grep -n "thyristor_v4_1.Roff"
```

**4. Decide it by execution** — this is what would move it out of the candidate
tier, and nothing here has done it:

```console
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check \
      --param thyristor_v4_1.Roff=0
```

The second command applies **the witness this finding names**, not an arbitrary
zero. A finding that claims a denominator vanishes has already been checked
arithmetically; what execution adds is whether the vanishing matters.

A clean baseline and a failing perturbation makes this **confirmed**. A failing
baseline makes it **undecidable** — the model does not run, so nothing can be
attributed to the parameter.


## What would disprove this

- Something on the path does exclude zero: an `assert`, an `if` guard, or a `min` on an intermediate declaration. DivisorSan follows bindings, not control flow, so a guard in an algorithm section is exactly the case it can miss.
- The denominator is never evaluated in any configuration this model reaches.


## Where the fix goes

At the declaration, not in this model. Every model that reaches the same declaration is a separate file here; one edit closes all of them. Use the declaration line above to find the others:

```console
$ grep -rl '| `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/Thyristor.mo:59` |' docs/v2/bugs/
```

## How strong is this?

| Tier | Evidence |
|---|---|
| **Confirmed** | fails under **two independent tools**, and the model is clean at its declared values |
| -> **Candidate** | static analysis of the canonical DAE reached it; **no execution has decided it either way** |
| **Latent** | a declaration *permits* a physically impossible value; **nothing has been observed failing** |

This instance is in the **Candidate** tier.
