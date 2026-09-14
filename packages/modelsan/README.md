# ModelSan

Finds parameter configurations under which a *valid* Modelica model behaves
incorrectly.

ModelSan is not a linter. Whether a model is syntactically valid is the
compiler's job, and Rumoca does it. ModelSan looks for the bugs that only
appear after flattening, or only under particular parameter values.

```bash
modelsan examples/modelsan/Tank.mo --model-name Tank
```

```text
[+] Parsed model Tank
    2 equations, 4 variables, 2 parameters

[+] 2 operation(s) with a mathematical domain condition
  divide: requires resistance != 0
      equation E0 at Tank.mo:7:3
      expression   (level / resistance)
      constrained  resistance
      parameters   resistance
      why          division by zero yields inf or nan

[!] ModelSan found a failure

Type:            simulation-failure
Trigger:         resistance = 0
Minimal config:  resistance = 0
```

## How it works

```text
Modelica -> rumoca -> .rbc -> ModelSan -> parameter candidates
                                   |              |
                                   |              v
                                   |          rumoca --simulate --check
                                   v              |
                             domain analysis      v
                                            violation + counterexample
```

ModelSan never simulates anything itself. It asks Rumoca to, because a second
evaluator would be a second set of numerical behaviour to explain. Rumoca
already refuses a solve that goes non-finite and names the offending variable,
which is a better detector than anything reimplemented here.

## What it detects today

| Detector | Kind | Finds |
|---|---|---|
| Mathematical domain | static + runtime | `/ 0`, `sqrt` of a negative, `log` of a non-positive, `asin`/`acos` outside `[-1, 1]`, `mod`/`rem` by zero |
| Declared range | runtime | a variable leaving its own `min`/`max` |
| Non-finite value | runtime | `nan` or `inf` anywhere in a trajectory |

Every one of these is a property the *model itself* declares. ModelSan infers
no physics: a violation means the model contradicted something its author
wrote down.

## Why boundary values, not random ones

Random floats rarely break a physical model. The values that break them sit
exactly on a boundary — zero, the declared `min`, one epsilon past `max` — or
make two previously independent parameters equal, which is where singularities
live. The generator is ordered by how likely a value is to expose something,
and the search stops at the first failure.

Every failure is then minimised: overrides are dropped one at a time and the
drop is kept if the failure survives. A report naming one parameter is worth
far more than one naming six.

## Limits

- Parameter search only. Initial conditions and input trajectories are not
  explored yet.
- Bounds that are expressions rather than literals are skipped, not evaluated —
  doing so would duplicate the compiler's evaluator, less correctly.
- No singularity detection. Detecting a Jacobian that loses rank when `a == b`
  needs the equation-level Jacobian, which bitcode does not yet carry.
- Coverage follows bitcode's: a model using functions, records or arrays
  exports with `unsupported` nodes, and ModelSan says so before reporting
  anything else.

## Install

```bash
pip install -e packages/rumoca-bitcode -e packages/modelsan
```

or

```bash
export PYTHONPATH=packages/rumoca-bitcode:packages/modelsan
python3 -m modelsan.cli model.mo --model-name M --rumoca ./target/debug/rumoca
```
