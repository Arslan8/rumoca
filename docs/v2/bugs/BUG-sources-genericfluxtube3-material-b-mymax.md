# BUG-022: `genericFluxTube3.material.B_myMax` in `Sources`

|  |  |
|---|---|
| **Tier** | **Confirmed** — reproduced in two independent tools |
| **Model** | `ModelicaTest.Magnetic.FluxTubes.Sources` |
| **Trigger** | `genericFluxTube3.material.B_myMax = 0` |
| **Found by** | **DivisorSan** — `packages/modelsan/modelsan/sanitizers/divisor.py` |
| **Reported as** | `divisor-reachable-zero` |
| **Declaration** | `FixedShape.mo:31` |
| **Confirmed by** | SolverSan under Rumoca, and independently under OpenModelica 1.27.0-dev |
| **Reach** | 1 models set this declaration |
| **From run** | `docs/runs/data/INSTANCES.json`, cross-confirmed against OpenModelica 1.27.0-dev; sanitizer attribution re-derived with `--keep-parameter-chains` |
| **Fix site** | [BUG-011: `SoftMagnetic.BaseData.B_myMax` is an unguarded divisor with no declared bound](../../verified%20bugs/BUG-011-fluxtubes-b-mymax-unguarded-divisor.md) |
| **Status** | Reported upstream, not fixed |


## The claim

`ModelicaTest.Magnetic.FluxTubes.Sources` runs cleanly at its declared values. Setting `genericFluxTube3.material.B_myMax = 0` — a value the declaration permits — makes it fail, in Rumoca and in OpenModelica.

The defect is in the **declaration**, not in this model. This model is the witness.

## Why DivisorSan fired

DivisorSan proposes an assignment for each division's **complete denominator**, substitutes it and evaluates: a finding exists only when the denominator actually comes out zero, under values the declarations, assertions and branch conditions all permit.

The assignment it found, and the arithmetic that verifies it:

```
denominator            genericFluxTube3.material.B_myMax
witness                genericFluxTube3.material.B_myMax = 0
  found by             set to zero
denominator at witness 0.0
at declared values     1.0
path condition         always evaluated
constraints consulted  genericFluxTube3.material.B_myMax: unbounded
```

The last four lines are the check. A denominator that does not evaluate to zero under the witness is not a finding, and this pass previously reported many that did not.

`constraints consulted` is where a disagreement usually lands. A symbol is only offered as a witness when its declaration permits the value: a `constant` never is, a `final` declaration is not unless its binding reads something adjustable, and `protected` is visibility rather than immutability. The contract behind that decision is carried in the artifact per symbol, so it can be read rather than inferred.


## Evidence

| key | value |
|---|---|
| `denominator` | genericFluxTube3.material.B_myMax |
| `witness` | genericFluxTube3.material.B_myMax = 0 |
| `witness_rationale` | set to zero |
| `denominator_at_witness` | 0.0 |
| `denominator_at_declared_values` | 1.0 |
| `path_condition` | always evaluated |
| `constraints` | genericFluxTube3.material.B_myMax: unbounded |
| `note` | a permitted assignment drives the complete denominator to zero, and nothing on the path excludes it |


## How to verify

Three checks, in increasing cost. All are run from the repository root.

**1. The sanitizer still reports it** (seconds):

```console
$ python3 tools/sweep/check_one.py ModelicaTest.Magnetic.FluxTubes.Sources \
      --target genericFluxTube3.material.B_myMax --keep-parameter-chains
```


**2. The declaration really permits the value** (seconds):

```console
$ find target/msl target/corpus -name 'FixedShape.mo'
$ sed -n '31p' "$(find target/msl target/corpus -name 'FixedShape.mo' | head -1)"
```

This run recorded the basename only, so check the first command's output before
trusting the second: several MSL files share a basename, and the declaration is
in whichever one declares this component.

That line is the declaration. Read its `min`: a declaration with no `min`, or
with `min=0`, permits the trigger value. Check the *type* too — a bound can be
inherited, and an inherited bound would refute the finding.

**3. The model fails at that value, and only at that value** (a minute):

```console
$ ./target/debug/rumoca compile "target/corpus/ModelicaStandardLibrary-4.1.0/ModelicaTest/Magnetic/FluxTubes.mo" --model ModelicaTest.Magnetic.FluxTubes.Sources \
      --source-root target/msl/ModelicaStandardLibrary-4.1.0 \
      --source-root target/corpus/ModelicaStandardLibrary-4.1.0 \
      --emit-bitcode /tmp/m.rbc
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check \
      --param genericFluxTube3.material.B_myMax=0
```

The first simulation must succeed and the second must fail. If the first also
fails, the model is not a clean witness and this instance should be withdrawn.

**Independently, under OpenModelica** — this is what makes the instance
*confirmed* rather than a candidate, so it is the check that matters most:

```console
$ omc --version          # needs CC=gcc on this machine
$ omc <<'EOF'
loadModel(Modelica, {"4.1.0"});
simulate(ModelicaTest.Magnetic.FluxTubes.Sources, simflags="-override genericFluxTube3.material.B_myMax=0");
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
