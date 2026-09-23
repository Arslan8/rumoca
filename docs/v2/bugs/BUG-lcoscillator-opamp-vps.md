# BUG-024: `opAmp.Vps` in `LCOscillator`

|  |  |
|---|---|
| **Tier** | **Confirmed** — reproduced in two independent tools |
| **Model** | `Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator` |
| **Trigger** | `opAmp.Vps = -15` |
| **Found by** | **DivisorSan** — `packages/modelsan/modelsan/sanitizers/divisor.py` |
| **Reported as** | `divisor-zero-when-parameters-equal` |
| **Declaration** | `IdealizedOpAmpLimited.mo:21` |
| **Confirmed by** | SolverSan under Rumoca, and independently under OpenModelica 1.27.0-dev |
| **Reach** | 1 models set this declaration |
| **From run** | `docs/runs/data/INSTANCES.json`, cross-confirmed against OpenModelica 1.27.0-dev; sanitizer attribution re-derived with `--keep-parameter-chains` |
| **Fix site** | [BUG-035: `LCOscillator.opAmp.Vps` fails at `-15`, a value its declaration permits](../../verified%20bugs/BUG-035-lcoscillator-opamp-vps.md) |
| **Status** | Reported upstream, not fixed |


## The claim

`Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator` runs cleanly at its declared values. Setting `opAmp.Vps = -15` — a value the declaration permits — makes it fail, in Rumoca and in OpenModelica.

The defect is in the **declaration**, not in this model. This model is the witness.

## Why DivisorSan fired

DivisorSan proposes an assignment for each division's **complete denominator**, substitutes it and evaluates: a finding exists only when the denominator actually comes out zero, under values the declarations, assertions and branch conditions all permit.

The assignment it found, and the arithmetic that verifies it:

```
denominator            (opAmp.vps - opAmp.vns)
witness                opAmp.Vps = -15
  found by             set equal to opAmp.Vns
denominator at witness 0.0
at declared values     30.0
path condition         always evaluated
constraints consulted  opAmp.Vps: unbounded
```

The last four lines are the check. A denominator that does not evaluate to zero under the witness is not a finding, and this pass previously reported many that did not.

`constraints consulted` is where a disagreement usually lands. A symbol is only offered as a witness when its declaration permits the value: a `constant` never is, a `final` declaration is not unless its binding reads something adjustable, and `protected` is visibility rather than immutability. The contract behind that decision is carried in the artifact per symbol, so it can be read rather than inferred.


## Evidence

| key | value |
|---|---|
| `denominator` | (opAmp.vps - opAmp.vns) |
| `witness` | opAmp.Vps = -15 |
| `witness_rationale` | set equal to opAmp.Vns |
| `denominator_at_witness` | 0.0 |
| `denominator_at_declared_values` | 30.0 |
| `path_condition` | always evaluated |
| `constraints` | opAmp.Vps: unbounded |
| `note` | the denominator is a difference, so it vanishes when the two sides are equal; no `min` on either can express a constraint between two parameters and an assertion is the only mechanism |


## How to verify

Three checks, in increasing cost. All are run from the repository root.

**1. The sanitizer still reports it** (seconds):

```console
$ python3 tools/sweep/check_one.py Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator \
      --target opAmp.Vps --keep-parameter-chains
```


**2. The declaration really permits the value** (seconds):

```console
$ find target/msl target/corpus -name 'IdealizedOpAmpLimited.mo'
$ sed -n '21p' "$(find target/msl target/corpus -name 'IdealizedOpAmpLimited.mo' | head -1)"
```

This run recorded the basename only, so check the first command's output before
trusting the second: several MSL files share a basename, and the declaration is
in whichever one declares this component.

That line is the declaration. Read its `min`: a declaration with no `min`, or
with `min=0`, permits the trigger value. Check the *type* too — a bound can be
inherited, and an inherited bound would refute the finding.

**3. The model fails at that value, and only at that value** (a minute):

```console
$ ./target/debug/rumoca compile "target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/LCOscillator.mo" --model Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator \
      --source-root target/msl/ModelicaStandardLibrary-4.1.0 \
      --source-root target/corpus/ModelicaStandardLibrary-4.1.0 \
      --emit-bitcode /tmp/m.rbc
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check
$ ./target/debug/rumoca compile-bitcode /tmp/m.rbc --simulate --check \
      --param opAmp.Vps=-15
```

The first simulation must succeed and the second must fail. If the first also
fails, the model is not a clean witness and this instance should be withdrawn.

**Independently, under OpenModelica** — this is what makes the instance
*confirmed* rather than a candidate, so it is the check that matters most:

```console
$ omc --version          # needs CC=gcc on this machine
$ omc <<'EOF'
loadModel(Modelica, {"4.1.0"});
simulate(Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator, simflags="-override opAmp.Vps=-15");
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
