# BUG-026: `idealGear.ratio` in `ElasticBearing`

|  |  |
|---|---|
| **Tier** | **Confirmed** — reproduced in two independent tools |
| **Model** | `Modelica.Mechanics.Rotational.Examples.ElasticBearing` |
| **Trigger** | `idealGear.ratio = 0` |
| **Found by** | **the parameter probe + SolverSan** — `packages/modelsan/modelsan/sanitizers/solver.py` |
| **Confirmed by** | SolverSan under Rumoca, and independently under OpenModelica 1.27.0-dev |
| **Reach** | 1 models set this declaration |
| **From run** | `docs/runs/data/INSTANCES.json`, cross-confirmed against OpenModelica 1.27.0-dev; sanitizer attribution re-derived with `--keep-parameter-chains` |
| **Fix site** | [BUG-015: `IdealGear.ratio` is an unbounded `Real` that decouples the gear at zero](../../verified%20bugs/BUG-015-idealgear-zero-ratio.md) |
| **Status** | Reported upstream, not fixed |


## The claim

`Modelica.Mechanics.Rotational.Examples.ElasticBearing` runs cleanly at its declared values. Setting `idealGear.ratio = 0` — a value the declaration permits — makes it fail, in Rumoca and in OpenModelica.

The defect is in the **declaration**, not in this model. This model is the witness.

## Why no static sanitizer names it

No static rule covers this one. It was found by perturbing parameters and watching the solver: the static checkers reason about one declaration at a time, and this failure is a relationship between two of them, which no `min` can express.

## How to verify

Three checks, in increasing cost. All are run from the repository root.

**1. No static sanitizer reports this one** (seconds) — that is the point of
it, and this command confirms it rather than reproducing anything:

```console
$ python3 tools/sweep/check_one.py Modelica.Mechanics.Rotational.Examples.ElasticBearing \
      --target idealGear.ratio --keep-parameter-chains
```

It should print **0 findings**. The failure below is real regardless; it is
what the static rules miss.


**2. The declaration really permits the value** (seconds):

The finding carries no declaration line, so there is nothing to open here.

**3. The model fails at that value, and only at that value** (a minute):

```console
$ ./target/debug/rumoca compile "target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/Rotational/Examples/ElasticBearing.mo" --model Modelica.Mechanics.Rotational.Examples.ElasticBearing \
      --source-root target/msl/ModelicaStandardLibrary-4.1.0 \
      --source-root target/corpus/ModelicaStandardLibrary-4.1.0 \
      --emit-bitcode /tmp/m.rbc
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check \
      --param idealGear.ratio=0
```

The first simulation must succeed and the second must fail. If the first also
fails, the model is not a clean witness and this instance should be withdrawn.

**Independently, under OpenModelica** — this is what makes the instance
*confirmed* rather than a candidate, so it is the check that matters most:

```console
$ omc --version          # needs CC=gcc on this machine
$ omc <<'EOF'
loadModel(Modelica, {"4.1.0"});
simulate(Modelica.Mechanics.Rotational.Examples.ElasticBearing, simflags="-override idealGear.ratio=0");
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
