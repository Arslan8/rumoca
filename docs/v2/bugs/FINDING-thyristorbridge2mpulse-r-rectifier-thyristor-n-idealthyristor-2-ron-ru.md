# FINDING-03615: `rectifier.thyristor_n.idealThyristor[2].Ron` in `ThyristorBridge2mPulse_R`

|  |  |
|---|---|
| **Tier** | **Candidate** — static only, not execution-confirmed |
| **Model** | `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_R` |
| **Reached as** | `rectifier.thyristor_n.idealThyristor[2].Ron` |
| **Found by** | **PhysicalSan** — `packages/modelsan/modelsan/sanitizers/physical.py`, rule `elec.resistance.positive` |
| **Reported as** | `physical-rule-does-not-apply` |
| **Severity** | low |
| **Declaration** | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Interfaces/IdealSemiconductor.mo:4` |
| **Signature** | `physical:physical-rule-does-not-apply:var:260:7e9c34b6` |
| **From run** | `docs/runs/data/STATIC_INTENT_DEFAULT.jsonl`, `tools/sweep/static_eval.py` over `tools/sweep/ALL.list`, default flags |
| **Status** | **candidate — no execution has decided it either way** |


## The claim

The component documents this quantity as taking the value it holds, so the rule derived from the si quantity alone does not bind it.

It does **not** claim that anything is wrong — this records a rule that was considered and correctly declined, with the contract that declined it.

## Why PhysicalSan fired

PhysicalSan binds each variable to a physical role from its `quantity`, unit and declaring class, then checks the domain invariant that role carries.

A physical rule is two separate facts: the **predicate**, and the **authority** for applying it to this object. An SI quantity supplies the first and not the second — `SI.Resistance` is declared by a passive resistor, by a negative-impedance converter, by a linearised incremental model and by a fault-injection input alike. This finding records which it had:

```
predicate     rectifier.thyristor_n.idealThyristor[2].Ron > 0
premise       refuted
authority     component_contract
role          —
declaration   —
```

**refuted** means an authoritative contract permits this value. The rule was considered and correctly declined; this record exists so that a rule not firing is distinguishable from a rule nobody wrote.

The shared zero contract that decided this, and how strongly it is held:

```
contract    Modelica.Electrical.Analog.Ideal.IdealThyristor.Ron: allowed (declared, from class_catalog) — an ideal switch family member; zero on-resistance is the documented ideal [matched by prefix, lower confidence]
behavior    allowed
confidence  declared
source      class_catalog
```

`confidence` is the field to read first. **proven** means the model's own equations establish it, **declared** means the component's catalog entry does, and **assumed** means a user contract supplied it and it is an input to the analysis rather than a result of it.

The rule it applied is `elec.resistance.positive`:

> a passive resistor dissipates energy; R <= 0 would make it a source, and R = 0 removes the equation that determines its current

Reference: MSL Electrical.Analog.Basic.Resistor.

It bound this variable to that rule on this evidence — this is the step to check first if you think the rule does not apply here:

```
{'quantity': 'Resistance', 'unit': 'Ohm', 'confidence': 'QUANTITY_AND_UNIT', 'premise_state': 'unknown', 'authority': 'quantity_or_unit', 'canonical_declaration': 'Modelica.Electrical.Analog.Ideal.IdealThyristor.Ron'}
```


## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.resistance.positive |
| `required` | rectifier.thyristor_n.idealThyristor[2].Ron &gt; 0 |
| `declared_min` | 0.0 |
| `variable_role` | parameter |
| `premise_state` | refuted |
| `authority` | component_contract |
| `contract` | Modelica.Electrical.Analog.Ideal.IdealThyristor.Ron: allowed (declared, from class_catalog) — an ideal switch family member; zero on-resistance is the documented ideal [matched by prefix, lower confidence] |
| `contract_behavior` | allowed |
| `contract_confidence` | declared |
| `contract_source` | class_catalog |
| `note` | the component documents this quantity as taking the value the rule forbids, so the rule derived from the quantity alone does not bind it |


## How to verify

**1. Reproduce this exact finding** (seconds):

```console
$ python3 tools/sweep/check_one.py Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_R \
      --target rectifier.thyristor_n.idealThyristor[2].Ron --sanitizer physical
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
$ sed -n '4p' "target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Interfaces/IdealSemiconductor.mo"
```

That line is the declaration. Read its `min`: a declaration with no `min`, or
with `min=0`, permits the trigger value. Check the *type* too — a bound can be
inherited, and an inherited bound would refute the finding.

**3. See it in the IR, if the claim is about reach rather than a bound:**

```console
$ python3 tools/sweep/check_one.py Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_R --keep-artifact /tmp/m.rbc \
      --sanitizer physical >/dev/null
$ ./target/debug/rumoca bitcode disasm /tmp/m.rbc | grep -n "rectifier.thyristor_n.idealThyristor[2].Ron"
```

**4. Decide it by execution** — this is what would move it out of the candidate
tier, and nothing here has done it:

```console
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check --param rectifier.thyristor_n.idealThyristor[2].Ron=0
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
$ grep -rl '| `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Interfaces/IdealSemiconductor.mo:4` |' docs/v2/bugs/
```

## How strong is this?

| Tier | Evidence |
|---|---|
| **Confirmed** | fails under **two independent tools**, and the model is clean at its declared values |
| -> **Candidate** | static analysis of the canonical DAE reached it; **no execution has decided it either way** |
| **Latent** | a declaration *permits* a physically impossible value; **nothing has been observed failing** |

This instance is in the **Candidate** tier.
