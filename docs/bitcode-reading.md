# Reading a bitcode artifact

Rumoca writes its canonical DAE to a separate `.rbc` file. There are several
ways to read it back; which you want depends on whether you are reading,
editing, or processing.

| | LLVM | Rumoca | Round-trips |
|---|---|---|---|
| binary | `.bc` | `.rbc` CBOR | — |
| **textual IR** | `.ll` | **`.rbctxt`** (`bitcode emit-text` / `assemble`) | **byte-identical** |
| disassembly | — | `bitcode disasm` | no, listing only |
| serialization | — | `.rbc` JSON | byte-identical |

**Checked-in examples:** [`docs/examples/ir/`](examples/ir/README.md) has a
3-variable model and a real MSL circuit, each in both forms.

## Producing one

```bash
rumoca compile Model.mo --model M --emit-bitcode model.rbc          # CBOR (default)
rumoca compile Model.mo --model M --emit-bitcode model.rbc \
    --bitcode-format json                                           # same schema, JSON
rumoca compile Model.mo --model M --emit-bitcode model.rbc \
    --bitcode-no-sources                                            # smaller; drops source text
```

## `bitcode disasm` — the listing

The one to reach for when you want to *read* the model.

```bash
rumoca bitcode disasm model.rbc
rumoca bitcode disasm model.rbc --provenance     # annotate each equation with file:line
rumoca bitcode disasm model.rbc --expressions    # also print the flat expression table
rumoca bitcode disasm model.rbc --ids            # show expression ids
```

```text
; model Modelica.Electrical.Analog.Examples.ChuaCircuit

variables (60)
  [  0] state      L.i      unit=A quantity=ElectricCurrent from=...Basic.Inductor start=0
  [  6] parameter  L.L      unit=H quantity=Inductance     from=...Basic.Inductor binding=18
  [ 17] parameter  Ro.R     unit=Ohm quantity=Resistance   from=...Basic.Resistor binding=0.0125

equations (44)
  [  3]  0 = ((L.L * der(L.i)) - L.v)                        ; Inductor.mo:7
  [ 15]  0 = (G.G_actual - (G.G / (1 + (G.alpha * (G.T_heatPort - G.T_ref)))))
  [ 29]  0 = (Nr.i - (if (Nr.v < -Nr.Ve) then ((Nr.Gb * (Nr.v + Nr.Ve)) - (Nr.Ga * Nr.Ve))
                      else (if (Nr.v > Nr.Ve) then ((Nr.Gb * (Nr.v - Nr.Ve)) + (Nr.Ga * Nr.Ve))
                      else (Nr.Ga * Nr.v))))

events (2)
  [  0] assert(.., "Temperature outside scope of model!")
```

It is **not** Modelica and does not try to be. It is a listing of the canonical
DAE: residual form (`0 = …`), coordinates spelled `der(x)` and `pre(x)`,
everything parenthesised so no reader has to recall a precedence table, and an
`<unsupported: …>` marker printed rather than elided wherever the current bitcode schema could
not represent a node. A partial export should look partial.

## `bitcode emit-text` / `assemble` — the textual IR

The `.ll` to the `.rbc`: text you can read, edit, and assemble back into a
**byte-identical** artifact.

```bash
rumoca bitcode emit-text model.rbc -o model.rbctxt --sources
rumoca bitcode assemble  model.rbctxt -o model.rbc
```

```text
; rumoca bitcode, textual form
rbc 2
producer "rumoca 0.10.0"
model "Modelica.Electrical.Analog.Examples.ChuaCircuit"

$0 type real
#4 comp "L"
%6 var "L.L" $3 parameter parameter scalars 1 comp #4 unit "H"
   quantity "Inductance" class "...Basic.Inductor" tunable from_source
   start ^7 binding ^6 @src 4 145 160 4 13
^24 expr $0 lit real 0.0 @gen default_start 7 514 536 11 3
^96 expr $0 bin sub ^94 ^95 @src 4 196 208 7 3
eq 3 ^96 reads %1 %6 dreads %0 @src 4 196 208 7 3
```

**Every id is written explicitly.** Expressions are a flat table addressed by
index, and re-deriving indices on parse would renumber a model containing
duplicate nodes — a real artifact has two separate `0` literals at ids 22 and
23. The ids are data, not presentation.

**Nothing is dropped silently.** The one omission is source *text*, which is
opt-in via `--sources` because it is most of the bytes and none of the
semantics. A round-trip with `--sources` is byte-exact; without it, everything
but that text survives. Both are pinned by tests.

**Assembling validates.** This is the form people hand-edit, so it is the one
most likely to be internally inconsistent. `assemble` runs the full validator
before writing — a dangling expression id or an equation reading an undeclared
variable is named at assemble time, not deferred.

Hand-editing works as you would expect:

```bash
sed 's/^\^24 expr \$0 lit integer 18/^24 expr $0 lit real 42.5/' model.rbctxt > edited.rbctxt
rumoca bitcode assemble edited.rbctxt -o edited.rbc
rumoca compile-bitcode edited.rbc --simulate --check --t-end 0.1
# Simulation complete: 101 time points, 44 variables
```

Errors name the line:

```
line 4: unknown scalar `nonsense`
```

### Why not `convert --format text`?

`convert` transcodes raw bytes, so a field this build does not know survives
it. The textual form goes through the typed schema and cannot make that
promise. Keeping them separate keeps `convert`'s guarantee honest.

## `bitcode dump` — the serialization

```bash
rumoca bitcode dump model.rbc
```

The whole artifact as JSON, whatever encoding it used on disk. This is the
format to *process*, not to read: expressions are stored flat and address their
operands by index, like a constant pool, so an equation reads

```json
{"id": 0, "residual": 83, "reads": [3, 5]}
```

and answering "what equation is that" means resolving 83 and everything under
it. For the 60-variable circuit above, `dump` is **256 KB** and `disasm` is
**11 KB**.

## `bitcode inspect` — the one-screen summary

```bash
rumoca bitcode inspect model.rbc
```

Counts by role, equations, expressions, events, components, and the connection
list. What you want before deciding whether to read further.

## `bitcode check`, `convert`, `round-trip`

```bash
rumoca bitcode check model.rbc                       # validate without rebuilding a model
rumoca bitcode convert model.rbc out.json --format json
rumoca bitcode round-trip model.rbc                  # import, re-export, compare
```

`round-trip` is the one that catches export defects: it proved
[TOOLBUG-011](toolbugs/TOOLBUG-011-bitcode-cannot-encode-unary-plus.md), where
an artifact failed its own import because unary plus had no v1 encoding.

## From Python

```python
import sys; sys.path[:0] = ["packages/rumoca-bitcode"]
from rumoca_bitcode import Model

model = Model.load("model.rbc")            # CBOR or JSON, auto-detected
for variable in model.variables:
    if variable.is_parameter:
        print(variable.name, variable.unit, variable.physical_quantity,
              variable.declaring_class, variable.binding)

for equation in model.equations:
    print(f"0 = {equation.residual!r}")    # __repr__ renders infix
```

The Python nodes carry the same `__repr__` the disassembler uses, so
`repr(expression)` gives the same infix rendering. `Variable.declaring_class`
is the fully qualified Modelica class that declared it, which the DAE itself
does not carry — see
[physical-sanitizers.md](architecture/physical-sanitizers.md#semantic-binding-what-an-object-represents).

## Compiling one back

```bash
rumoca compile-bitcode model.rbc --simulate --check --t-end 0.5
rumoca compile-bitcode model.rbc --simulate --param mass1.m=0
```

Import replays the construction operations, so every DAE invariant is enforced
on the way in: an artifact that violates one is refused rather than loaded.

## Tests

`crates/rumoca/tests/suite_core/bitcode_disasm.rs` — the residual resolves to
infix rather than an index, parameter bindings appear on the declaration line,
and the expression table and provenance are opt-in.
