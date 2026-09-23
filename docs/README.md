# ModelSan documentation

| | |
|---|---|
| [**v2/bugs/**](v2/bugs/README.md) | **One file per instance, all three tiers.** Each names the sanitizer that found it and carries the commands to check it. Start here. |
| [findings/](findings/) | Bugs in **target programs** — Modelica models and libraries. The results. |
| [bitcode-reference.md](bitcode-reference.md) | Every type in the artifact format, generated from `schema.rs` and checked for staleness. The narrative is in [SPEC_RUMOCA_BITCODE.md](SPEC_RUMOCA_BITCODE.md). |
| [bitcode-linking.md](bitcode-linking.md) | Combine independent artifacts with the native linker or Python SDK; wiring and execution safety rules. |
| [combining-models.md](combining-models.md) | Start-to-finish tutorial: build two models, link and connect their ports, run equation/execution passes, then simulate. |
| [connector-validation.md](connector-validation.md) | Native connection-law checks, raw-artifact regression cases, and incomplete-interface refusal. |
| [method/](method/) | How a candidate becomes a finding, and what each verification stage removed. |
| [toolbugs/](toolbugs/) | Defects in the instruments (Rumoca, `rumoca-bitcode`) and what they cost in coverage. Not results. |
| [verified bugs/](verified%20bugs/) | All confirmed reports, including fixed regressions, with verification level and current status. |

The split matters: a crash in AddressSanitizer is not a finding about the
program under test. Tool defects are recorded because each one caps how much of
a corpus the detectors can see, not because they count.
