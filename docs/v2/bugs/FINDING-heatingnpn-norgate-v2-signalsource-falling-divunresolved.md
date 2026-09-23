# FINDING-00354: `V2.signalSource.falling` in `HeatingNPN_NORGate`

|  |  |
|---|---|
| **Tier** | **Candidate** — static only, not execution-confirmed |
| **Model** | `Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate` |
| **Reached as** | `V2.signalSource.falling` |
| **Found by** | **DivisorSan** — `packages/modelsan/modelsan/sanitizers/divisor.py` |
| **Reported as** | `divisor-zero-unresolved` |
| **Severity** | medium |
| **Declaration** | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Blocks/Sources.mo:928` |
| **Signature** | `divisor:divisor-zero-unresolved:exp:752:f0217ae6` |
| **From run** | `docs/runs/data/STATIC_INTENT_DEFAULT.jsonl`, `tools/sweep/static_eval.py` over `tools/sweep/ALL.list`, default flags |
| **Status** | **candidate — no execution has decided it either way** |


## The claim

An assignment drives the denominator to zero, but whether the division is evaluated there could not be decided from the artifact.

It does **not** claim that the model is wrong — this is **unresolved**, not confirmed, and is reported so it is not silently dropped.

## Why DivisorSan fired

DivisorSan proposes an assignment for each division's **complete denominator**, substitutes it and evaluates: a finding exists only when the denominator actually comes out zero, under values the declarations, assertions and branch conditions all permit.

The assignment it found, and the arithmetic that verifies it:

```
denominator            V2.signalSource.falling
witness                V2.signalSource.falling = 0
  found by             set to zero
denominator at witness 0.0
at declared values     5.0
path condition         not ((((time < V2.signalSource.startTime) or (V2.signalSource.nperiod == 0)) or ((V2.signalSource.nperiod > 0) and (V2.signalSource.count >= V2.signalSource.nperiod)))) and not ((time < (V2.signalSource.T_start + V2.signalSource.T_rising))) and not ((time < (V2.signalSource.T_start + V2.signalSource.T_width))) and ((time < (V2.signalSource.T_start + V2.signalSource.T_falling)))
constraints consulted  V2.signalSource.falling: min=0
```

The last four lines are the check. A denominator that does not evaluate to zero under the witness is not a finding, and this pass previously reported many that did not.

`constraints consulted` is where a disagreement usually lands. A symbol is only offered as a witness when its declaration permits the value: a `constant` never is, a `final` declaration is not unless its binding reads something adjustable, and `protected` is visibility rather than immutability. The contract behind that decision is carried in the artifact per symbol, so it can be read rather than inferred.


## Evidence

| key | value |
|---|---|
| `denominator` | V2.signalSource.falling |
| `witness` | V2.signalSource.falling = 0 |
| `witness_rationale` | set to zero |
| `denominator_at_witness` | 0.0 |
| `denominator_at_declared_values` | 5.0 |
| `denominator_range` | [0, inf] |
| `path_condition` | not ((((time &lt; V2.signalSource.startTime) or (V2.signalSource.nperiod == 0)) or ((V2.signalSource.nperiod &gt; 0) and (V2.signalSource.count &gt;= V2.signalSource.nperiod)))) and not ((time &lt; (V2.signalSource.T_start + V2.signalSource.T_rising))) and not ((time &lt; (V2.signalSource.T_start + V2.signalSource.T_width))) and ((time &lt; (V2.signalSource.T_start + V2.signalSource.T_falling))) |
| `verdict` | UNKNOWN |
| `proof` | the path depends on quantities the artifact does not determine: (time &lt; (V2.signalSource.T_start + V2.signalSource.T_falling)); (time &lt; (V2.signalSource.T_start + V2.signalSource.T_rising)); (time &lt; (V2.signalSource.T_start + V2.signalSource.T_width)) |
| `constraints` | V2.signalSource.falling: min=0 |
| `note` | an assignment drives the denominator to zero, but whether the division is evaluated there could not be decided from the artifact; this is unresolved, not confirmed |


## How to verify

**1. Reproduce this exact finding** (seconds):

```console
$ python3 tools/sweep/check_one.py Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate \
      --target V2.signalSource.falling --sanitizer divisor
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
$ sed -n '928p' "target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Blocks/Sources.mo"
```

That line is the declaration. Read its `min`: a declaration with no `min`, or
with `min=0`, permits the trigger value. Check the *type* too — a bound can be
inherited, and an inherited bound would refute the finding.

**3. See it in the IR, if the claim is about reach rather than a bound:**

```console
$ python3 tools/sweep/check_one.py Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate --keep-artifact /tmp/m.rbc \
      --sanitizer divisor >/dev/null
$ ./target/debug/rumoca bitcode disasm /tmp/m.rbc | grep -n "V2.signalSource.falling"
```

**4. Decide it by execution** — this is what would move it out of the candidate
tier, and nothing here has done it:

```console
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check \
      --param V2.signalSource.falling=0
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
$ grep -rl '| `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Blocks/Sources.mo:928` |' docs/v2/bugs/
```

## How strong is this?

| Tier | Evidence |
|---|---|
| **Confirmed** | fails under **two independent tools**, and the model is clean at its declared values |
| -> **Candidate** | static analysis of the canonical DAE reached it; **no execution has decided it either way** |
| **Latent** | a declaration *permits* a physically impossible value; **nothing has been observed failing** |

This instance is in the **Candidate** tier.
