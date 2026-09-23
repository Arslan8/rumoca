# Sentinel-encoded parameters: 74 declarations that lie about their domain

Not a defect. A documented workaround for a gap in the language, which happens
to be indistinguishable from the defect class this project reports — and is
therefore worth writing down before someone files 12 issues against it.

## The pattern

`Modelica.Electrical.Spice3` needs to know whether the user set a parameter.
Modelica has no way to ask, so the library encodes "unset" in the value:

> In SPICE3 it is important to know whether a parameter was set by the user or
> not [...] Since in Modelica there is no possibility to check that, a
> circumvention was chosen. The relevant parameters get an unrealistic value
> (-1e40) as their default value.
>
> — `Electrical/Spice3.mo:157`

```modelica
parameter SI.Resistance RSH = -1e40 "Sheet resistance";
parameter SI.Length     L   = -1e40 "Length of the resistor";
parameter SI.Current    ISC = -1e40;
```

and consumed as:

```modelica
dev.m_dICVDSIsGiven := if (IC_VDS > -1e40) then 1 else 0;
dev.m_dICVDS        := if (IC_VDS > -1e40) then IC_VDS else 0;
```

## Scale

| | |
|---|---|
| `-1e40` declarations | **74** |
| files containing them | **1** (`Electrical/Spice3.mo`) |
| on quantities that cannot physically be negative | **12** |

The 12 are a negative sheet resistance, negative lengths, negative widths, a
negative oxide thickness, negative currents and negative drain/source ohmic
resistances — every one of them a value PhysicalSan is built to report:

```
4593  parameter SI.Transconductance KP=-1e40
4599  parameter SI.Resistance RD=-1e40 "Drain ohmic resistance, default 0"
4600  parameter SI.Resistance RS=-1e40 "Source ohmic resistance, default 0"
4623  parameter SI.Length TOX=-1e40 "Oxide thickness, default 1e-7"
5011  parameter SI.Current ISE = -1e40
5014  parameter SI.Current ISC = -1e40
5192  parameter SI.Resistance RD=-1e40 "Drain ohmic resistance, default 0"
5193  parameter SI.Resistance RS=-1e40 "Source ohmic resistance, default 0"
5328  parameter SI.Resistance R= -1e40
5331  parameter SI.Length L = -1e40 "Length of the resistor"
5332  parameter SI.Length W = -1e40
5397  parameter SI.Resistance RSH = -1e40 "Sheet resistance"
5414  parameter SI.Length  W = -1e40
```

## Why it is not filed as a defect

The library says what it is doing and why, at the top of the file. The values
are never used as physical quantities — every consumer tests against the
sentinel first. Reporting these would be reporting a deliberate, documented
design decision.

## Why it is worth recording anyway

**It is a false-positive class of the same shape as Chua's diode.** Both are
cases where the declared quantity is genuinely `Resistance` or `Conductance`,
the value is genuinely negative, and the model is genuinely correct. The
[semantic binding layer](../architecture/physical-sanitizers.md#semantic-binding-what-an-object-represents)
exists for exactly this, and the Spice3 classes are the natural next entries in
its catalog.

**It is unverified in-tool.** Rumoca cannot compile
`Spice3.Semiconductors.R_Semiconductor`, so the false positive is latent rather
than observed. It is recorded here as a source-level finding, not as a
reproduced one — the distinction matters and is easy to lose.

**It is an argument about the language, not the library.** MSL is working around
the absence of an optional-parameter concept by borrowing values out of the
physical domain. Any static checker that reads declared values will collide with
it, and the collision is not the library's fault or the checker's.

## Status

Not filed upstream. No fix is being proposed to MSL: the workaround is sound
given the language. The action is on ModelSan's side, and is to catalog the
Spice3 classes so their sentinel parameters bind to an
`component.sentinel_encoded` role that the physical rules stand down on — the
same mechanism already used for `NonlinearResistor`.
