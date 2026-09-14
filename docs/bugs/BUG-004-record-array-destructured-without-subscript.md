# BUG-004: flatten destructures an array of records without its subscript

| | |
|---|---|
| **Severity** | Medium — blocks a whole MSL sub-library; fails cleanly, not a crash |
| **Component** | `rumoca-phase-flatten` (surfaces as `ED008` from `rumoca-phase-dae`) |
| **Affects** | Any vectorised call passing an array of records to a function taking one record. In MSL this is every `Modelica.ComplexMath.*` call on a polyphase quantity. |
| **Found by** | ModelSan sweep of ModelicaTest, 2026-09-13 |
| **Status** | Reported, not fixed |

## Summary

When an array of records is passed to a function whose input is a single
record, flatten destructures the argument into its fields but drops the array
subscript. It emits a reference to `v.re` while declaring only `v[1].re`,
`v[2].re`, … — so the reference names a variable that does not exist.

DAE lowering then rejects the Flat model it was handed:

```
[ED008] unresolved Flat reference `v.re`
  help: Flat IR must carry a declared, fully resolved coordinate identity
```

The diagnostic is accurate and correctly placed. The defect is upstream: Flat
did not carry a fully resolved identity, which is the contract the help text
states.

## Reproducer

24 lines, no MSL dependency:

```modelica
package T
  record Cx
    Real re;
    Real im;
  end Cx;

  function cabs
    input Cx c;
    output Real y;
  algorithm
    y := sqrt(c.re * c.re + c.im * c.im);
  end cabs;

  model M
    parameter Integer m = 2;
    Cx v[m];
    Real a[m] = cabs(v);        // vectorised call: array of records -> scalar-record function
    Real x(start = 1);
  equation
    der(x) = -x;
    for i in 1:m loop
      v[i].re = x * i;
      v[i].im = 0;
    end for;
  end M;
end T;
```

```console
$ rumoca compile T.mo --model T.M
[ED008] unresolved Flat reference `v.re`
```

## The mismatch, shown directly

```console
$ rumoca compile T.mo --model T.M --emit flat-mo

# Flat DECLARES, element-wise:
v[1].re   v[1].im   v[2].re   v[2].im

# Flat REFERENCES, whole-array:
cabs(v.re, v.im)
```

Nothing declares `v.re`.

## The array dimension is the trigger

Removing it compiles cleanly:

```modelica
  Cx v;              // scalar record
  Real a = cabs(v);  // destructures to v.re, v.im — which Flat declares
```

So record destructuring for a function argument is correct for a scalar record
and wrong for an array of records. The vectorisation over `m` is applied to the
call but not to the field access the destructuring introduces.

## Where it bites in MSL

`Modelica.Electrical.QuasiStatic.Polyphase.Interfaces.OnePort`:

```modelica
  SI.ComplexVoltage v[m] "Complex voltage";
  SI.Voltage abs_v[m] = Modelica.ComplexMath.abs(v)
    "Magnitude of complex voltage";
```

`ComplexMath.abs` takes one `Complex`; `v` is `Complex[m]`. Flat emits
`Modelica.ComplexMath.abs(currentSource.v.re, currentSource.v.im)` and the
model is rejected.

`OnePort` is a base class for the whole
`Modelica.Electrical.QuasiStatic.Polyphase` package, so this single defect
blocks every model built on it. It accounted for 4 of 17 compile failures in a
40-model ModelicaTest pilot.

Confirmed on
`ModelicaTest.Electrical.QuasiStatic.Polyphase.SerialConnection`.

## Expected behaviour

Either destructure element-wise —

```
cabs(v[1].re, v[1].im), cabs(v[2].re, v[2].im)
```

— or keep the argument whole and let the array-of-record field access resolve
as an array-valued expression. Which is right depends on where Rumoca intends
vectorised calls to be expanded; the current output is neither.

## Provenance

- Fails on plain `rumoca compile`; no bitcode involved.
- The reproducer contains no `connect(...)`, so this branch's
  `rumoca-phase-flatten` connection change cannot execute.

## Note

This one is a rejection, not a crash, and the diagnostic names the exact
reference. That is the failure behaving as designed — SPEC_0031's
"unsupported or unproved semantics fail with a typed diagnostic at their first
owning phase". The complaint is not about the handling; it is that the
condition should not arise.
