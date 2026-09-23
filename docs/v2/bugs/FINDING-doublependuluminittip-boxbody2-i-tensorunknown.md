# FINDING-04366: `boxBody2.I` in `DoublePendulumInitTip`

|  |  |
|---|---|
| **Tier** | **Candidate** — static only, not execution-confirmed |
| **Model** | `Modelica.Mechanics.MultiBody.Examples.Elementary.DoublePendulumInitTip` |
| **Reached as** | `boxBody2.I` |
| **Found by** | **PhysicalSan** — `packages/modelsan/modelsan/sanitizers/physical.py` |
| **Reported as** | `physical-inertia-tensor-undecided` |
| **Severity** | low |
| **Declaration** | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/MultiBody/Parts/BodyBox.mo:111` |
| **Signature** | `physical:physical-inertia-tensor-undecided:par:517:25a0ff32` |
| **From run** | `docs/runs/data/STATIC_INTENT_DEFAULT.jsonl`, `tools/sweep/static_eval.py` over `tools/sweep/ALL.list`, default flags |
| **Status** | **candidate — no execution has decided it either way** |


## The claim

This component's inertia tensor could not be assembled from values this analysis can resolve, so **neither its validity nor its invalidity is claimed**.

It does **not** claim that anything is wrong. It is recorded because the six scalar declarations are excluded from the positivity rule either way, and a silent exclusion is indistinguishable from a missed defect.

## Why PhysicalSan fired

PhysicalSan binds each variable to a physical role from its `quantity`, unit and declaring class, then checks the domain invariant that role carries.

This one is an **aggregate** rule: its subject is the `symmetric_inertia_tensor` that `boxBody2` assembles from several declarations, not any one of them. The fields it covers are excluded from the scalar rule, so this finding is the only thing said about them.

```
matrix       [[I_11, I_21, I_31], [I_21, I_22, I_32], [I_31, I_32, I_33]] (not numerically known)
eigenvalues  not computed
verdict      unknown
reason       `boxBody2.I` is declared as a 3x3 tensor whose entries this analysis cannot evaluate, so neither its validity nor its invalidity is claimed
```

Positive semidefiniteness is decided over **all** principal minors with a scale-relative tolerance, not the leading ones: Sylvester's criterion over leading minors decides positive *definiteness*, and `[[0,0,0],[0,1,0],[0,0,-1]]` has leading minors 0, 0, 0 and an eigenvalue of -1. See [the method note](../../method/aggregate-and-signed-domains.md).


## Evidence

| key | value |
|---|---|
| `aggregate` | symmetric_inertia_tensor |
| `component` | boxBody2 |
| `declaring_class` | Modelica.Mechanics.MultiBody.Parts.BodyBox |
| `fields` | boxBody2.I |
| `matrix` | [[I_11, I_21, I_31], [I_21, I_22, I_32], [I_31, I_32, I_33]] (not numerically known) |
| `required` | boxBody2.I is positive semidefinite |
| `verdict` | unknown |
| `reason` | `boxBody2.I` is declared as a 3x3 tensor whose entries this analysis cannot evaluate, so neither its validity nor its invalidity is claimed |
| `note` | the tensor could not be assembled from values this analysis can resolve, so neither its validity nor its invalidity is claimed; the scalar fields are excluded from the positivity rule either way, because that rule is wrong about products of inertia |


## How to verify

**1. Reproduce this exact finding** (seconds):

```console
$ python3 tools/sweep/check_one.py Modelica.Mechanics.MultiBody.Examples.Elementary.DoublePendulumInitTip \
      --target boxBody2.I --sanitizer physical
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
$ sed -n '111p' "target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/MultiBody/Parts/BodyBox.mo"
```

That line is the declaration. Read its `min`: a declaration with no `min`, or
with `min=0`, permits the trigger value. Check the *type* too — a bound can be
inherited, and an inherited bound would refute the finding.

**3. See it in the IR, if the claim is about reach rather than a bound:**

```console
$ python3 tools/sweep/check_one.py Modelica.Mechanics.MultiBody.Examples.Elementary.DoublePendulumInitTip --keep-artifact /tmp/m.rbc \
      --sanitizer physical >/dev/null
$ ./target/debug/rumoca bitcode disasm /tmp/m.rbc | grep -n "boxBody2.I"
```

**4. Decide it by execution** — this is what would move it out of the candidate
tier, and nothing here has done it:

```console
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check --param boxBody2.I=0
```

The second command applies **the witness this finding names**, not an arbitrary
zero. A finding that claims a denominator vanishes has already been checked
arithmetically; what execution adds is whether the vanishing matters.

A clean baseline and a failing perturbation makes this **confirmed**. A failing
baseline makes it **undecidable** — the model does not run, so nothing can be
attributed to the parameter.


## What would disprove this

- The semantic binding is wrong: the `matched_by` block above says why this variable was given this physical role. If the quantity or the declaring class does not mean what the rule assumes, the finding does not apply.
- The value is excluded elsewhere — by an `assert`, by a guard, or by a bound on the *type* rather than the declaration.
- The variable is a documented sentinel.


## Where the fix goes

At the declaration, not in this model. Every model that reaches the same declaration is a separate file here; one edit closes all of them. Use the declaration line above to find the others:

```console
$ grep -rl '| `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/MultiBody/Parts/BodyBox.mo:111` |' docs/v2/bugs/
```

## How strong is this?

| Tier | Evidence |
|---|---|
| **Confirmed** | fails under **two independent tools**, and the model is clean at its declared values |
| -> **Candidate** | static analysis of the canonical DAE reached it; **no execution has decided it either way** |
| **Latent** | a declaration *permits* a physically impossible value; **nothing has been observed failing** |

This instance is in the **Candidate** tier.
