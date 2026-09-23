# TOOLBUG-011: bitcode v1 refused its own export of unary plus

| | |
|---|---|
| **Component** | Rumoca, `crates/rumoca-bitcode` |
| **Severity** | Medium — a model that simulated stopped simulating |
| **Status** | Fixed, 2026-09-14 |

## What went wrong

`unary_of` mapped two of the DAE's three unary operators:

```rust
fn unary_of(operator: dae::UnaryOperator) -> Option<RbcUnaryOp> {
    match operator {
        dae::UnaryOperator::Negate => Some(RbcUnaryOp::Negate),
        dae::UnaryOperator::Not    => Some(RbcUnaryOp::Not),
        _ => None,                       // Plus
    }
}
```

MLS §3.4 unary plus fell into the wildcard, so the export emitted an
`Unsupported` node and the artifact then failed its *own* import:

```
bitcode failed validation:
  - expression 1 is an unsupported node: unary operator not in bitcode v1
```

## Why it stayed hidden

Constant folding consumes unary plus before it reaches export. MSL writes it —
`Modelica.Electrical.Analog.Examples.InvertingAmp:4` declares
`parameter SI.Voltage Vps=+15` — but `+15` folds to `15` and the exporter never
sees it.

It surfaced only under `--no-fold-parameter-bindings`, and as a **simulation
regression rather than a compile error**: the model compiled in both modes and
simulated in only one.

```console
$ ... OpAmps.Comparator                      rc=0  Simulation complete: 501 time points
$ ... OpAmps.Comparator --no-fold-...        rc=1  bitcode failed validation
```

Two of 80 models sampled were affected. The corpus fold comparison reported
**zero compile regressions**, which was true and insufficient — it compared
compilation, and this breaks after it.

## A second, smaller defect

The diagnostic reads "unary operator not in bitcode v1", which parses two ways
and cost a wrong diagnosis: `not` *is* mapped, and the failing operator was
`Plus`. Reworded to "unary operator has no bitcode v1 encoding".

## Fix

`RbcUnaryOp::Plus` added, mapped on export and import. Encoding it as its
operand was considered and is not possible here: expressions are addressed by
index and each must occupy its own, so dropping the node would shift every
index after it.

## Regression

`crates/rumoca-bitcode/src/tests.rs::unary_plus_survives_a_round_trip` — a DAE
carrying unary plus must import and re-export with the node intact.
