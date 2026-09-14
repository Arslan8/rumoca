# ModelSan documentation

| | |
|---|---|
| [findings/](findings/) | Bugs in **target programs** — Modelica models and libraries. The results. |
| [method/](method/) | How a candidate becomes a finding, and what each verification stage removed. |
| [toolbugs/](toolbugs/) | Defects in the instruments (Rumoca, `rumoca-bitcode`) and what they cost in coverage. Not results. |

The split matters: a crash in AddressSanitizer is not a finding about the
program under test. Tool defects are recorded because each one caps how much of
a corpus the detectors can see, not because they count.
