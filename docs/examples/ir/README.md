# Worked IR examples

Real output, checked in so you can read it without running anything.

| File | What |
|---|---|
| [`Decay.mo`](Decay.mo) | the source: one state, two parameters, one divisor |
| [`Decay.rbctxt`](Decay.rbctxt) | its **textual IR** — 36 lines, the whole model |
| [`Decay.listing.txt`](Decay.listing.txt) | its **disasm listing** — 11 lines |
| [`ChuaCircuit.rbctxt`](ChuaCircuit.rbctxt) | a real MSL circuit, 37 KB |
| [`ChuaCircuit.listing.txt`](ChuaCircuit.listing.txt) | the same, as a listing, 12 KB |

## The two forms, on the same model

`Decay.listing.txt` — for reading. The expression graph is resolved into infix:

```text
variables (3)
  [  0] parameter  k      from=Decay start=2.5     binding=2.5
  [  1] parameter  tau    from=Decay start=(1 / k) binding=(1 / k)
  [  2] state      x      from=Decay start=1

equations (1)
  [  0]  0 = (der(x) - -(x / tau))   ; Decay.mo:6
```

`Decay.rbctxt` — for editing. Every node addressed, every id explicit:

```text
%1 var "tau" $0 parameter parameter scalars 1 class "Decay" tunable
   from_source start ^7 binding ^4 @src 0 111 119 3 13

^9  expr $0 coord der %2        @src 0 175 181 6 3
^10 expr $0 coord state %2      @src 0 185 186 6 13
^11 expr $0 coord param %1      @src 0 189 192 6 17
^12 expr $0 bin div ^10 ^11     @src 0 185 192 6 13
^13 expr $0 un negate ^12       @src 0 184 192 6 12
^14 expr $0 bin sub ^9 ^13      @src 0 175 181 6 3

eq 0 ^14 reads %1 %2 dreads %2  @src 0 175 192 6 3
```

Read the equation bottom-up and it is the listing's line: `^14` is
`der(x) - (-(x / tau))`.

## Two things this example happens to show

**`tau = 1/k` survived.** The source says `1 / k` and the IR says `bin div ^5
^6` where `^6` is `coord param %0`. Rumoca folds a derived parameter into its
value when that value is an exact integer, and `1/2.5 = 0.4` is not — see
[bitcode-reading.md](../../bitcode-reading.md) and
`--no-fold-parameter-bindings` for when it does.

**`^0` and `^1` are both `lit real 2.5`.** Duplicate nodes, not shared. That is
why the textual form writes ids explicitly instead of re-deriving them on parse:
renumbering would silently merge these two and produce a different artifact.

## Producing them yourself

```bash
rumoca compile Model.mo --model M --emit-bitcode m.rbc

rumoca bitcode disasm    m.rbc --provenance        # the listing
rumoca bitcode emit-text m.rbc -o m.rbctxt         # the textual IR
rumoca bitcode assemble  m.rbctxt -o m2.rbc        # and back
```

`--sources` on `emit-text` embeds the source text, which is what makes the
round-trip byte-exact; without it everything but that text survives.
