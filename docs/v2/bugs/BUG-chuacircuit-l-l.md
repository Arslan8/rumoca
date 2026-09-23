# BUG-012: `L.L` in `ChuaCircuit`

|  |  |
|---|---|
| **Tier** | **Confirmed** — reproduced in two independent tools |
| **Model** | `Modelica.Electrical.Analog.Examples.ChuaCircuit` |
| **Trigger** | `L.L = 0` |
| **Found by** | **PhysicalSan** — `packages/modelsan/modelsan/sanitizers/physical.py`, rule `elec.inductance.positive` |
| **Reported as** | `physical-domain-unenforced` |
| **Declaration** | `Inductor.mo:4` |
| **Confirmed by** | SolverSan under Rumoca, and independently under OpenModelica 1.27.0-dev |
| **Reach** | 8 models set this declaration |
| **From run** | `docs/runs/data/INSTANCES.json`, cross-confirmed against OpenModelica 1.27.0-dev; sanitizer attribution re-derived with `--keep-parameter-chains` |
| **Fix site** | [BUG-023: `ChuaCircuit.L.L` fails at `0`, a value its declaration permits](../../verified%20bugs/BUG-023-chuacircuit-l-l.md) |
| **Status** | Reported upstream, not fixed |


## The claim

`Modelica.Electrical.Analog.Examples.ChuaCircuit` runs cleanly at its declared values. Setting `L.L = 0` — a value the declaration permits — makes it fail, in Rumoca and in OpenModelica.

The defect is in the **declaration**, not in this model. This model is the witness.

## Why PhysicalSan fired

PhysicalSan binds each variable to a physical role from its `quantity`, unit and declaring class, then checks the domain invariant that role carries.

The rule it applied is `elec.inductance.positive`:

> stored energy is L*i^2/2; L = 0 turns the differential equation into a constraint on voltage

Reference: MSL Electrical.Analog.Basic.Inductor.

It bound this variable to that rule on this evidence — this is the step to check first if you think the rule does not apply here:

```
{'quantity': 'Inductance', 'unit': 'H', 'semantic_role': 'component.passive.inductance', 'binding_source': 'component_type', 'confidence': 'QUANTITY_AND_UNIT', 'declaring_class': 'Modelica.Electrical.Analog.Basic.Inductor', 'member': 'L'}
```


## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.inductance.positive |
| `required` | L.L &gt; 0 |
| `declared_min` | None |
| `variable_role` | parameter |
| `note` | nothing bounds this declaration, so it permits values physics forbids |


## How to verify

Three checks, in increasing cost. All are run from the repository root.

**1. The sanitizer still reports it** (seconds):

```console
$ python3 tools/sweep/check_one.py Modelica.Electrical.Analog.Examples.ChuaCircuit \
      --target L.L --keep-parameter-chains
```


**2. The declaration really permits the value** (seconds):

```console
$ find target/msl target/corpus -name 'Inductor.mo'
$ sed -n '4p' "$(find target/msl target/corpus -name 'Inductor.mo' | head -1)"
```

This run recorded the basename only, so check the first command's output before
trusting the second: several MSL files share a basename, and the declaration is
in whichever one declares this component.

That line is the declaration. Read its `min`: a declaration with no `min`, or
with `min=0`, permits the trigger value. Check the *type* too — a bound can be
inherited, and an inherited bound would refute the finding.

**3. The model fails at that value, and only at that value** (a minute):

```console
$ ./target/debug/rumoca compile "target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/ChuaCircuit.mo" --model Modelica.Electrical.Analog.Examples.ChuaCircuit \
      --source-root target/msl/ModelicaStandardLibrary-4.1.0 \
      --source-root target/corpus/ModelicaStandardLibrary-4.1.0 \
      --emit-bitcode /tmp/m.rbc
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check \
      --param L.L=0
```

The first simulation must succeed and the second must fail. If the first also
fails, the model is not a clean witness and this instance should be withdrawn.

**Independently, under OpenModelica** — this is what makes the instance
*confirmed* rather than a candidate, so it is the check that matters most:

```console
$ omc --version          # needs CC=gcc on this machine
$ omc <<'EOF'
loadModel(Modelica, {"4.1.0"});
simulate(Modelica.Electrical.Analog.Examples.ChuaCircuit, simflags="-override L.L=0");
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
