# False positives and explicit non-defects: `zero-machine-inertia`

**2 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

Jr and Js are passed directly to Rotational.Components.Inertia. That component uses J*a=sum(tau), so J=0 produces an algebraic torque balance rather than an intrinsic reciprocal. Js is relevant only when the stator rotates. A particular drive train can have incompatible starts or constraints, but the declaration alone does not establish that both machine inertias must be strictly positive.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0316](../false-positives/DECL-0316.md) | — | `Jr` | Source/semantic review | [DECL-partialbasicmachine-jr-5.md](../../bugs/DECL-partialbasicmachine-jr-5.md) |
| [DECL-0317](../false-positives/DECL-0317.md) | — | `Js` | Source/semantic review | [DECL-partialbasicmachine-js-8.md](../../bugs/DECL-partialbasicmachine-js-8.md) |
