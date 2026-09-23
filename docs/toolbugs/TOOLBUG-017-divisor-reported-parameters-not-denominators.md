# TOOLBUG-017: DivisorSan reported parameters, not denominators

| | |
|---|---|
| **Component** | `packages/modelsan/modelsan/sanitizers/divisor.py` |
| **Severity** | High — the dominant false-positive class in the static tier |
| **Found by** | Independent review of the published reports, 2026-09-16 |
| **Status** | Fixed. Rewritten around verified witnesses; 9 regression cases in `tests/test_divisor_witness.py`. |

## The defect

The pass reported **every parameter appearing anywhere inside a denominator**,
on the reasoning that a parameter which can be zero can zero the expression
containing it. That reasoning is false, and the code said so plainly:

```python
for variable in divisor.variables():          # every parameter under the `/`
    if not variable.is_parameter:
        continue
    ...
    found.append(DivisorRisk(parameter=parameter, ...))
```

Nothing evaluated the denominator. Nothing checked that the proposed value was
permitted. Nothing looked at the branch the division sat in.

## What it produced

| Report | Denominator | The claim | Why it is wrong |
|---|---|---|---|
| FINDING-03714 | `1 + c_b*B_N + B_N^n` | `c_b` can be zero | at `c_b = 0` the denominator is `1 + B_N^n` |
| FINDING-00185 | `1 + alpha*(T - T_ref)` | `alpha` can be zero | at `alpha = 0` the denominator is `1`; also asserted `>= eps` |
| FINDING-01566 | `2*pi*fsNominal` | `pi` can be zero | `pi` is `constant`, and cannot be set at all |
| FINDING-00002 | `duration` | `duration` can be zero | at `duration = 0` the `Ramp` takes its step branch and the division is unreachable |
| FINDING-04783 | `k*Ni` | `k` can be zero | `assert(abs(k) >= small)`, and `Ni(min=100*eps)` |
| BUG-004 | — | `L` reaches a division | `L*der(i) = v` has no division; the DAE's `der(i) = v/L` is the compiler's |

`pi` is the clearest of them. The SDK's `Variable.is_parameter` is true for
`role == "constant"` as well as `role == "parameter"`, so every occurrence of
`Modelica.Constants.pi` in a denominator — and there are many — was a settable
knob that could be driven to zero.

## The fix

The pass now *proves* what it claims. For each division it proposes a concrete
assignment, substitutes it, and evaluates the complete denominator. **If the
result is not zero there is no finding.** Everything else narrows which
assignments may be proposed:

- **Bounds**, from the declaration and from the type, compared *relatively*.
  An absolute tolerance of `1e-12` treats `min=2.22e-14` as admitting zero, and
  it did.
- **Assertions.** `assert(d >= eps)` over the denominator marks the site
  guarded; `assert(abs(k) >= small)` puts a magnitude floor on `k`, which a
  single interval cannot express and which MSL uses to mean "non-zero".
- **Settability.** A constant is never a witness. A variable is not a knob, but
  a variable *defined* by parameters is followed to them — which is how
  `p_s/(vps - vns)` resolves to the supply-voltage parameters.
- **Path conditions.** A witness that makes the enclosing branch unreachable is
  not a witness. `Ramp` needs symbolic reasoning here, not evaluation: at
  `duration = 0` the path requires `time >= startTime` and `time < startTime`
  at once, and `time` has no value. The feasibility check works on intervals
  over free symbols.
- **Provenance.** `source` versus `generated` is carried by every object in the
  artifact, so a division the compiler introduced is labelled rather than
  blamed on the modeller.

## New finding kinds

Guarded sites are reported under their own kinds rather than discarded. A
reader is better served by "this division is protected, here is what protects
it" than by silence, and a guard that turns out to be insufficient is itself a
finding.

| Kind | Meaning |
|---|---|
| `divisor-reachable-zero` | verified witness, source division, reachable, unguarded |
| `divisor-zero-when-parameters-equal` | the witness is an equality, not a zero |
| `divisor-guarded-by-assertion` | the model asserts this denominator away from zero |
| `divisor-unreachable-under-witness` | the witness closes the branch containing the division |
| `divisor-introduced-by-translation` | the compiler produced this division, not the source |
| `divisor-zero-at-declared-values` | already zero before anything is changed; the baseline is broken |

## Two defects found while fixing it

**`start` was read as a value.** `_declared_value` fell back to `start` for any
variable. For a parameter the binding is the value, but for a *variable*
`start` is an initial guess for the solver. Reading it as a value gave
`opAmp.vps` the value 0, which made `vps - vns` appear already zero and
**suppressed BUG-024** — a confirmed defect.

**`walk_expressions` yields every node as a root.** A nested `if` therefore
arrived twice: once as a child carrying its parent's path condition, and once
as a root carrying only its own. The `Ramp` division was reported under both,
and the second copy looked unguarded. `root_expressions` now yields top-level
expressions only.

## Every cited case is a test

`packages/modelsan/tests/test_divisor_witness.py` holds one test per case the
review named, each referencing the report ID it refutes, plus a general test
that no finding is emitted without a verified witness and a stated path
condition. All nine pass.
