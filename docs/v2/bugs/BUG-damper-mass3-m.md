# BUG-007: `mass3.m` in `Damper`

|  |  |
|---|---|
| **Tier** | **Confirmed** — reproduced in two independent tools |
| **Model** | `Modelica.Mechanics.Translational.Examples.Damper` |
| **Trigger** | `mass3.m = 0` |
| **Found by** | **PhysicalSan** — `packages/modelsan/modelsan/sanitizers/physical.py`, rule `mech.mass.positive` |
| **Reported as** | `physical-bound-permits-zero` |
| **Declaration** | `Mass.mo:3` |
| **Confirmed by** | SolverSan under Rumoca, and independently under OpenModelica 1.27.0-dev |
| **Reach** | 18 models set this declaration |
| **From run** | `docs/runs/data/INSTANCES.json`, cross-confirmed against OpenModelica 1.27.0-dev; sanitizer attribution re-derived with `--keep-parameter-chains` |
| **Fix site** | [BUG-002: `Translational.Components.Mass.m` declares `min=0`, a value it cannot integrate](../../verified%20bugs/BUG-002-msl-zero-mass-within-declared-bound.md) |
| **Status** | Reported upstream, not fixed |


## The claim

`Modelica.Mechanics.Translational.Examples.Damper` runs cleanly at its declared values. Setting `mass3.m = 0` — a value the declaration permits — makes it fail, in Rumoca and in OpenModelica.

The defect is in the **declaration**, not in this model. This model is the witness.

## Why PhysicalSan fired

PhysicalSan binds each variable to a physical role from its `quantity`, unit and declaring class, then checks the domain invariant that role carries.

The rule it applied is `mech.mass.positive`:

> m*a = f determines acceleration only for m > 0; negative mass is not a physical body

Reference: MSL Mechanics.Translational.Components.Mass.

It bound this variable to that rule on this evidence — this is the step to check first if you think the rule does not apply here:

```
{'quantity': 'Mass', 'unit': 'kg', 'semantic_role': 'component.translational.mass', 'binding_source': 'component_type', 'confidence': 'QUANTITY_AND_UNIT', 'declaring_class': 'Modelica.Mechanics.Translational.Components.Mass', 'member': 'm'}
```


## Evidence

| key | value |
|---|---|
| `domain` | mechanical |
| `rule` | mech.mass.positive |
| `required` | mass3.m &gt; 0 |
| `declared_min` | 0.0 |
| `variable_role` | parameter |
| `note` | the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not |


## How to verify

Three checks, in increasing cost. All are run from the repository root.

**1. The sanitizer still reports it** (seconds):

```console
$ python3 tools/sweep/check_one.py Modelica.Mechanics.Translational.Examples.Damper \
      --target mass3.m --keep-parameter-chains
```


**2. The declaration really permits the value** (seconds):

```console
$ find target/msl target/corpus -name 'Mass.mo'
$ sed -n '3p' "$(find target/msl target/corpus -name 'Mass.mo' | head -1)"
```

This run recorded the basename only, so check the first command's output before
trusting the second: several MSL files share a basename, and the declaration is
in whichever one declares this component.

That line is the declaration. Read its `min`: a declaration with no `min`, or
with `min=0`, permits the trigger value. Check the *type* too — a bound can be
inherited, and an inherited bound would refute the finding.

**3. The model fails at that value, and only at that value** (a minute):

```console
$ ./target/debug/rumoca compile "target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/Translational/Examples/Damper.mo" --model Modelica.Mechanics.Translational.Examples.Damper \
      --source-root target/msl/ModelicaStandardLibrary-4.1.0 \
      --source-root target/corpus/ModelicaStandardLibrary-4.1.0 \
      --emit-bitcode /tmp/m.rbc
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check \
      --param mass3.m=0
```

The first simulation must succeed and the second must fail. If the first also
fails, the model is not a clean witness and this instance should be withdrawn.

**Independently, under OpenModelica** — this is what makes the instance
*confirmed* rather than a candidate, so it is the check that matters most:

```console
$ omc --version          # needs CC=gcc on this machine
$ omc <<'EOF'
loadModel(Modelica, {"4.1.0"});
simulate(Modelica.Mechanics.Translational.Examples.Damper, simflags="-override mass3.m=0");
EOF
```


## What would disprove this

- The baseline simulation also fails, so the trigger value is not what breaks it.
- The declaration turns out to carry a bound that excludes the trigger value after all (check the *type* as well as the declaration — a bound can be inherited).
- The value is a documented sentinel rather than a real setting. `Spice3.mo` encodes "unset" as `-1e40` and tests for it before use; see [sentinel-parameters](../../findings/sentinel-parameters.md).


## How strong is this?

| Tier | Evidence |
|---|---|
| -> **Confirmed** | fails under **two independent tools**, and the model is clean at its declared values |
| **Candidate** | static analysis of the canonical DAE reached it; **no execution has decided it either way** |
| **Latent** | a declaration *permits* a physically impossible value; **nothing has been observed failing** |

This instance is in the **Confirmed** tier.
