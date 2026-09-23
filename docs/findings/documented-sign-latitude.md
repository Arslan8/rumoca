# Components whose documentation permits what physics seems to forbid

Not a defect list. A correction to a premise this project was checking against,
and the reason four of its electrical rules were wrong.

## What MSL says

```html
<!-- Electrical/Analog/Basic/Resistor.mo -->
<p>The Resistance <em>R</em> is allowed to be positive, zero, or negative.</p>

<!-- Electrical/Analog/Basic/Conductor.mo -->
<p>The Conductance <em>G</em> is allowed to be positive, zero, or negative.</p>

<!-- Electrical/Analog/Basic/Capacitor.mo -->
<p>The Capacitance <em>C</em> is allowed to be positive or zero.</p>

<!-- Electrical/Analog/Basic/Inductor.mo -->
<p>The Inductance <em>L</em> is allowed to be positive, or zero.</p>
```

Seven files in `Electrical/` carry the "positive, zero, or negative" phrasing:
`Resistor.mo`, `Conductor.mo`, `Capacitor.mo`, `Inductor.mo`, their QuasiStatic
counterparts, and `Spice3.mo`.

## Why this matters

PhysicalSan asserted `R > 0` and `G > 0` on exactly these components, and the
semantic binding catalog marked them `component.passive.resistance` /
`component.passive.conductance` — the role that raises a finding to HIGH
severity on the grounds that the premise is *established*.

It was not established. It was contradicted, in writing, in the component.

A negative resistance in `Basic.Resistor` is a modelling choice the library
explicitly supports — small-signal and equivalent-circuit models need it — and
`v = R*i` is perfectly well-behaved at any sign. A checker reporting it is
arguing with the library, not with the user.

**114 of the corpus's 323 physical-invariant violations came from this**, all of
them `elec.conductance.positive`, all at `G = 0`.

## Where the bound does still hold

| | |
|---|---|
| `Translational.Components.Mass.m` | no documented latitude; `min=0` permits a value that degenerates `m*a = f` — [BUG-002](../verified%20bugs/BUG-002-msl-zero-mass-within-declared-bound.md) |
| `Rotational.Components.Inertia.J` | same — [BUG-018](../verified%20bugs/BUG-018-rotational-inertia-zero-within-declared-bound.md) |
| `Analog.Basic.Capacitor.C` | documented as permitting zero, and **fails at zero in both tools** — [BUG-013](../verified%20bugs/BUG-013-capacitor-zero-capacitance-topology-dependent.md) |
| `Analog.Basic.Inductor.L` | documented as permitting zero, and **fails at zero in both tools** — [BUG-010](../verified%20bugs/BUG-010-inductor-documents-zero-it-cannot-honour.md) |

The last two are the interesting asymmetry. For `C` and `L` the documentation
grants latitude the component cannot honour, and *that* is the finding —
established by execution in two independent tools, not by a physical argument.
For `R` and `G` the documentation grants latitude the component honours
perfectly well, and there is no finding at all.

## The general lesson

A physical invariant is a claim about a component, and the component's author
gets a say. Three sources can settle it, in increasing order of authority:

1. what the quantity measures — `Conductance`
2. what the class is — a passive shunt, or a negative-impedance converter
3. **what the component documents about itself**

This project had the first two and not the third, and the third overruled both.
Searching MSL for the documented case turns up no conductance that is stated to
be passive, which is why the regression test for that rule now uses a synthetic
vendor catalog: the mechanism is sound and the library has no instance of it.

## Fix applied

`component.unrestricted.resistance` and `component.unrestricted.conductance`
roles, catalogued for the four `Basic` classes and listed in the rules'
`excluded_roles`. The bound still fires on an uncatalogued resistance, at MEDIUM
severity, labelled as an assumption — a negative resistance in a component
nobody has characterised is still worth a look.
