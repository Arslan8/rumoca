# FINDING-00084: `l1` in `CauerLowPassAnalog`

|  |  |
|---|---|
| **Tier** | **Candidate** — static only, not execution-confirmed |
| **Model** | `Modelica.Electrical.Analog.Examples.CauerLowPassAnalog` |
| **Reached as** | `l1` |
| **Found by** | **PhysicalSan** — `packages/modelsan/modelsan/sanitizers/physical.py`, rule `elec.inductance.positive` |
| **Reported as** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Declaration** | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/CauerLowPassAnalog.mo:5` |
| **Signature** | `physical:physical-domain-unenforced:var:0:939d3a9e` |
| **From run** | `docs/runs/data/STATIC_INTENT_DEFAULT.jsonl`, `tools/sweep/static_eval.py` over `tools/sweep/ALL.list`, default flags |
| **Status** | **candidate — no execution has decided it either way** |


## The claim

Nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones.

It does **not** claim that any model actually sets such a value.

## Why PhysicalSan fired

PhysicalSan binds each variable to a physical role from its `quantity`, unit and declaring class, then checks the domain invariant that role carries.

A physical rule is two separate facts: the **predicate**, and the **authority** for applying it to this object. An SI quantity supplies the first and not the second — `SI.Resistance` is declared by a passive resistor, by a negative-impedance converter, by a linearised incremental model and by a fault-injection input alike. This finding records which it had:

```
predicate     l1 > 0
premise       established
authority     source_arithmetic
role          —
declaration   Modelica.Electrical.Analog.Examples.CauerLowPassAnalog.l1
```

**established** means a component contract or a user assumption says this object is the component the rule is about, so the predicate is enforced rather than suggested.

The rule it applied is `elec.inductance.positive`:

> stored energy is L*i^2/2; L = 0 turns the differential equation into a constraint on voltage

Reference: MSL Electrical.Analog.Basic.Inductor.

It bound this variable to that rule on this evidence — this is the step to check first if you think the rule does not apply here:

```
{'quantity': 'Inductance', 'unit': 'H', 'confidence': 'QUANTITY_AND_UNIT', 'premise_state': 'unknown', 'authority': 'quantity_or_unit', 'canonical_declaration': 'Modelica.Electrical.Analog.Examples.CauerLowPassAnalog.l1'}
```


## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.inductance.positive |
| `required` | l1 &gt; 0 |
| `declared_min` | None |
| `variable_role` | parameter |
| `premise_state` | established |
| `authority` | source_arithmetic |
| `canonical_declaration` | Modelica.Electrical.Analog.Examples.CauerLowPassAnalog.l1 |
| `contract_source` | equation |
| `premise_reason` | a source equation divides by this parameter, so the value is excluded by arithmetic rather than by intent |
| `note` | nothing bounds this declaration, so it permits values the component&#x27;s own contract forbids |


## How to verify

**1. Reproduce this exact finding** (seconds):

```console
$ python3 tools/sweep/check_one.py Modelica.Electrical.Analog.Examples.CauerLowPassAnalog \
      --target l1 --sanitizer physical
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
$ sed -n '5p' "target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/CauerLowPassAnalog.mo"
```

That line is the declaration. Read its `min`: a declaration with no `min`, or
with `min=0`, permits the trigger value. Check the *type* too — a bound can be
inherited, and an inherited bound would refute the finding.

**3. See it in the IR, if the claim is about reach rather than a bound:**

```console
$ python3 tools/sweep/check_one.py Modelica.Electrical.Analog.Examples.CauerLowPassAnalog --keep-artifact /tmp/m.rbc \
      --sanitizer physical >/dev/null
$ ./target/debug/rumoca bitcode disasm /tmp/m.rbc | grep -n "l1"
```

**4. Decide it by execution** — this is what would move it out of the candidate
tier, and nothing here has done it:

```console
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check --param l1=0
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
$ grep -rl '| `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/CauerLowPassAnalog.mo:5` |' docs/v2/bugs/
```

## How strong is this?

| Tier | Evidence |
|---|---|
| **Confirmed** | fails under **two independent tools**, and the model is clean at its declared values |
| -> **Candidate** | static analysis of the canonical DAE reached it; **no execution has decided it either way** |
| **Latent** | a declaration *permits* a physically impossible value; **nothing has been observed failing** |

This instance is in the **Candidate** tier.
