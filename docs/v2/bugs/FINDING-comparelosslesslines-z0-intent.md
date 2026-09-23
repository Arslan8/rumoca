# FINDING-00551: `z0` in `CompareLosslessLines`

|  |  |
|---|---|
| **Tier** | **Candidate** — static only, not execution-confirmed |
| **Model** | `Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines` |
| **Reached as** | `z0` |
| **Found by** | **PhysicalSan** — `packages/modelsan/modelsan/sanitizers/physical.py`, rule `elec.resistance.positive` |
| **Reported as** | `physical-intent-question` |
| **Severity** | low |
| **Declaration** | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/Lines/CompareLosslessLines.mo:12` |
| **Signature** | `physical:physical-intent-question:var:5:6bd7604c` |
| **From run** | `docs/runs/data/STATIC_INTENT_DEFAULT.jsonl`, `tools/sweep/static_eval.py` over `tools/sweep/ALL.list`, default flags |
| **Status** | **candidate — no execution has decided it either way** |


## The claim

The value or the declaration is unusual for the **quantity** it declares, and nothing says what this component is — so this is a question for the author, not a claim about the model.

It does **not** claim that the value is wrong. `SI.Resistance` is declared by passive resistors, by negative-impedance converters, by linearised incremental models and by fault-injection inputs alike; without a component contract the analyzer does not know the intent, and this advisory asks rather than asserts.

## Why PhysicalSan fired

PhysicalSan binds each variable to a physical role from its `quantity`, unit and declaring class, then checks the domain invariant that role carries.

A physical rule is two separate facts: the **predicate**, and the **authority** for applying it to this object. An SI quantity supplies the first and not the second — `SI.Resistance` is declared by a passive resistor, by a negative-impedance converter, by a linearised incremental model and by a fault-injection input alike. This finding records which it had:

```
predicate     z0 > 0
premise       unknown
authority     quantity_or_unit
role          —
declaration   Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines.z0
```

**unknown** means no component contract and no user assumption says what this object is, so the rule is applied as a *question*: it is low severity, it is not counted as a defect, and it does not fail a run. Answer it by adding a component contract or a `[[contracts]]` entry naming the intended `sign_domain` — see [the method note](../../method/physical-intent-policy.md).

The question this finding asks:

> `z0` carries no bound that would exclude it, which is unusual for a resistance — but nothing declares what this component is, so the analyzer cannot tell whether it is intended. Is it? If so, declare it: add a component contract, or a `[[contracts]]` entry naming the intended `sign_domain`. If not, bound the declaration.

The rule it applied is `elec.resistance.positive`:

> a passive resistor dissipates energy; R <= 0 would make it a source, and R = 0 removes the equation that determines its current

Reference: MSL Electrical.Analog.Basic.Resistor.

It bound this variable to that rule on this evidence — this is the step to check first if you think the rule does not apply here:

```
{'quantity': 'Resistance', 'unit': 'Ohm', 'confidence': 'QUANTITY_AND_UNIT', 'premise_state': 'unknown', 'authority': 'quantity_or_unit', 'canonical_declaration': 'Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines.z0'}
```


## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.resistance.positive |
| `required` | z0 &gt; 0 |
| `declared_min` | None |
| `variable_role` | parameter |
| `observation` | permissive-declaration |
| `premise_state` | unknown |
| `authority` | quantity_or_unit |
| `canonical_declaration` | Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines.z0 |
| `question` | `z0` carries no bound that would exclude it, which is unusual for a resistance — but nothing declares what this component is, so the analyzer cannot tell whether it is intended. Is it? If so, declare it: add a component contract, or a `[[contracts]]` entry naming the intended `sign_domain`. If not, bound the declaration. |


## How to verify

**1. Reproduce this exact finding** (seconds):

```console
$ python3 tools/sweep/check_one.py Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines \
      --target z0 --sanitizer physical
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
$ sed -n '12p' "target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/Lines/CompareLosslessLines.mo"
```

That line is the declaration. Read its `min`: a declaration with no `min`, or
with `min=0`, permits the trigger value. Check the *type* too — a bound can be
inherited, and an inherited bound would refute the finding.

**3. See it in the IR, if the claim is about reach rather than a bound:**

```console
$ python3 tools/sweep/check_one.py Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines --keep-artifact /tmp/m.rbc \
      --sanitizer physical >/dev/null
$ ./target/debug/rumoca bitcode disasm /tmp/m.rbc | grep -n "z0"
```

**4. Decide it by execution** — this is what would move it out of the candidate
tier, and nothing here has done it:

```console
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check --param z0=0
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
$ grep -rl '| `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/Lines/CompareLosslessLines.mo:12` |' docs/v2/bugs/
```

## How strong is this?

| Tier | Evidence |
|---|---|
| **Confirmed** | fails under **two independent tools**, and the model is clean at its declared values |
| -> **Candidate** | static analysis of the canonical DAE reached it; **no execution has decided it either way** |
| **Latent** | a declaration *permits* a physically impossible value; **nothing has been observed failing** |

This instance is in the **Candidate** tier.
