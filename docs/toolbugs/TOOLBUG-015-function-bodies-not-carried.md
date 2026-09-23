# TOOLBUG-015: bitcode carries function declarations but not their bodies

| | |
|---|---|
| **Component** | `rumoca-bitcode`, schema v1 |
| **Severity** | High — blocks round-trip on 32% of MSL, and blocked *all* consumer visibility into call arguments until the declarations were added |
| **Status** | Partly fixed. Declarations, call nodes and parameter coordinates are carried; bodies are not. |

## How it was measured

Every unsupported node in an artifact used to report the same string —
`coordinate kind not in bitcode v1` — which says something is missing without
saying what. Naming the kind (`export.rs::coordinate_kind_name`,
`operation_name`) and adding `rumoca bitcode check --strict` turned the
question into a census. Over all 491 models of `msl-full.list`:

| occurrences | models | kind |
|---:|---:|---|
| 3637 | 156 | coordinate kind `function_parameter` |
| 3621 | 156 | expression form `call` |
| 1022 | 44 | expression form `function_value` |
| 89 | 43 | expression form `string_conversion` |
| 50 | 25 | expression form `function_fold_parameter` |
| 50 | 25 | expression form `function_fold_output` |
| 32 | 3 | coordinate kind `delay` |
| 30 | 17 | coordinate kind `previous` |
| 10 | 7 | expression form `clock_transfer` |
| 3 | 3 | coordinate kind `clock_interval` |

Everything above the fold is one thing: **functions**. `call` and
`function_parameter` co-occur in exactly the same 156 models, because a call's
arguments bind the callee's parameters.

## What was fixed

`RbcFunction` carries the declaration — name, parameter names and types, result
types, the MLS §18.3 `Inline` request, and whether the body is an MLS §12.9
external one. `RbcExprNode::Call` carries the call site, including the `owner`
id that two projections of `(a, b) = f(x)` share, so a consumer knows that is
one evaluation and not two.

That is what a *reader* needs. Before it, a call exported as `Unsupported`, and
every expression underneath it became unreachable: nothing in the model referred
to the arguments, so no traversal found them.

```
Modelica.Mechanics.Rotational.Examples.First
  before: 1 unsupported node, 0 calls
  after:  0 unsupported nodes, 1 call
          Modelica.Math.sin(((((2 * (2 * asin(1.0))) * sine.f)
                               * (time - sine.startTime)) + sine.phase))
```

## What is not fixed

The **body**. A DAE function body is its own IR: SSA definitions with scopes,
loop transitions with carried values, conditional assignment, assertions, and
for an external function a foreign interface with ordered ABI arguments and
link facts. It is a larger piece of work than the rest of this schema together,
and a half-carried body is worse than an absent one.

So `RbcFunctionBody::ElidedModelica` records the absence explicitly — a consumer
cannot mistake an elided body for an empty one — and import refuses by name:

```
expression 214 calls `Modelica.Math.asin`, and bitcode v1 carries function
declarations but not their bodies
```

## Consequences, stated exactly

- **Consumers that read**: fixed. Every call site and every argument expression
  is reachable, in all 156 models.
- **Round-trip**: still blocked on those models, and on the 44 with
  `function_value` (body expressions live in the same shared arena).
- **Interval and dimension propagation *through* a call**: not possible. A pass
  must treat a call result as unknown, which is sound and imprecise.

## Remaining tail

`string_conversion`, `delay`, `previous`, `clock_transfer` and `clock_interval`
are each a distinct owner-side object the schema does not model. Together they
appear in fewer models than functions do, and none of them blocks a model that
functions do not already block.
