# How Rumoca represents initialization

Milestone 1 of InitSan: what an initialization analysis can actually read, and
what it cannot. Written before building anything, because the answer changes
the design — one construct is lost in lowering, and two of the framework pieces
InitSan was to be built on do not exist.

Probed with a model exercising every initialization construct at once
(`docs/examples/init/InitProbe.mo`), compiled and read back from the artifact.

## What survives into RBC

| Construct | Representation | Usable |
|---|---|---|
| `start` | `RbcVariable.start`, an expression | yes |
| `fixed` | `RbcVariable.fixed: Option<bool>` | **yes, and this is the important one** |
| `min` / `max` | `RbcVariable.min` / `.max` | yes, *since* [TOOLBUG-013](../toolbugs/TOOLBUG-013-type-level-bounds-dropped.md) |
| parameter value | `RbcVariable.binding` | yes |
| derived parameter | binding, folded or symbolic | yes, see `--no-fold-parameter-bindings` |
| initial equation | `RbcModel.initial_equations`, residual form | yes |
| discrete initial value | `start` + `fixed` on a `discrete_real` / `discrete_value` | yes |
| `initial()` **as a condition** | `RbcConditionNode::Initial` | yes |

The `fixed` attribute arrives as a three-state `Option<bool>`, which is exactly
what §6 of the brief requires and is worth stating plainly:

```
xFixed       state   fixed=True   start=5     -> an initial constraint
xGuess       state   fixed=False  start=7     -> a guess, no constraint
xFromInitEq  state   fixed=None   start=0.0   -> unspecified; the 0.0 is a default
```

`xFromInitEq` is the case that defeats naive `start` checking. Its start reads
`0.0` and it is actually initialized to `-1` by an initial equation. Any
analysis that reads `start` and stops has the wrong number.

## What does not survive

### `initial()` inside an expression

```modelica
usesInitial = if initial() then 1.0 else 0.0;
```

reaches the artifact as

```text
[  5]  0 = (usesInitial - (if <unsupported: coordinate kind not in bitcode v1> then 1 else 0))
```

The DAE lowers `initial()` to `Coordinate::Condition(id)`, and
`export.rs::coordinate_of` maps 12 of the DAE's 17 coordinate kinds and drops
the rest through a `_ => return None` wildcard. Also unmapped: `ClockInterval`,
`Delay`, `Previous`, `Terminal`, `Binder`, `FunctionParameter`.

This matters specifically for InitSan: a model whose initialization branches on
`initial()` has a hole precisely where the analysis needs to look. The
conditions table already carries `{"kind": "initial"}`, so the fix is to map the
coordinate to it rather than to invent anything.

### Initial algorithms

```modelica
initial algorithm
  usesInitial := if initial() then 1.0 else 0.0;
```

is **refused**, not dropped:

```
[ED013] unsupported initial algorithm in canonical DAE: initial algorithm target
`usesInitial` has role Algebraic; the initialization system owns an
algorithm-determined coordinate only as a `parameter` declared `fixed = false`
or as a discrete-time coordinate
```

A loud refusal is the right behaviour and needs no fix. It does bound InitSan's
reach: initialization expressed through an algorithm on an algebraic will not
reach the artifact at all, so InitSan cannot see it and should not pretend to.

## Two framework pieces the brief assumes do not exist

Checked rather than assumed, because building on them would have failed late:

| Assumed | Reality |
|---|---|
| `DomainSan` | exists, `sanitizers/domain.py` |
| Semantic Binder | exists, `semantics/` |
| Predicate engine, three-valued | exists — `Predicate.holds()` returns `True`/`False`/`None` |
| **`RelationSan`** | **does not exist.** No such class anywhere. |
| **Interval / range propagation** | **does not exist.** `range.py` is a *runtime* bound checker, not interval arithmetic. There is no `Interval` type. |

So §9 ("Reuse RelationSan") and §10 ("Reuse the existing interval/range-analysis
engine") describe infrastructure that has to be built, not reused. The relational
*shape* does exist in one place — `DivisorSan`'s `relational` case, which finds
`a - b` divisors — but it is not a general predicate facility.

## An InitSan already exists, and it is the one the brief rejects

`sanitizers/initialization.py` does exactly what §26 says not to do: a `start`
versus `min`/`max` check, plus an equation/unknown count comparison. It has no
notion of initial equations, no environment, and no propagation.

It should be extended rather than replaced — its runtime half (phase-tagged
initialization failures) is sound and is not in scope here.

## What this implies for the design

1. **The `fixed` three-state is the foundation.** `True` is a constraint,
   `False` is a guess, `None` is unspecified. Conflating them is the single
   most likely source of false positives, and the existing InitSan conflates
   them.
2. **Initial equations are first-class and already present**, in residual form.
   An environment can be populated from them directly.
3. **`Interval` and a relational predicate facility must be built.** They are
   the two genuinely new pieces.
4. **Map `Coordinate::Condition`** before relying on `initial()`.
5. **Initial algorithms bound the reach** and should be reported as a coverage
   gap, not silently treated as absent.

---

# StructureSan: which categories are reachable

Determined the same way — by probing, before relying on it.

Rumoca refuses to construct a DAE from an unbalanced model:

```
Under (1 equation, 2 unknowns)   -> unbalanced model: balance = -1, refused
Over  (2 equations, 1 unknown)   -> unbalanced model: balance = +1, refused
```

So a whole family of §25's categories cannot be reached through the normal
compile path, because the compiler already catches them — and more strictly,
by refusing rather than reporting:

| Category | Reachable via RBC? |
|---|---|
| `UNMATCHED_VARIABLE` (global under-constraint) | **no** — refused at DAE construction |
| `UNMATCHED_EQUATION` (global over-constraint) | **no** — same |
| `STATE_WITHOUT_DERIVATIVE_CONSTRAINT` | **rarely** — a variable with no `der()` is classified algebraic, not left a dangling state |
| `DUPLICATE_EQUATION` | **yes**, when the model is still balanced |
| `CONTRADICTORY_CONSTRAINT` | **yes**, same condition |
| `ISOLATED_COMPONENT` | yes — balance says nothing about reachability |
| `DEGENERATE_PARAMETER_STRUCTURE` | yes — a parameter collapsing a constraint keeps the count |
| initialization structure | yes — initial equations are carried separately |

This is not a reason to drop the matching machinery. A *balanced* system can
still be structurally singular — equal counts with the wrong incidence — and
that is exactly what the compiler's count check cannot see and a matching can.
But it does mean the yield concentrates in the balanced-but-wrong cases, and
the headline categories in §25 are largely already covered by an existing,
stricter check.

Worth stating plainly rather than shipping a pass whose main categories can
never fire.
