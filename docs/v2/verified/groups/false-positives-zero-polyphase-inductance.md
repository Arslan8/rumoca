# False positives and explicit non-defects: `zero-polyphase-inductance`

**1 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

The polyphase component passes each L element to Basic.Inductor. That scalar component explicitly documents positive or zero inductance and uses L*der(i)=v. A universal positive-only finding contradicts the delegated contract.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0181](../false-positives/DECL-0181.md) | — | `L` | Source/semantic review | [DECL-inductor-l-4-2.md](../../bugs/DECL-inductor-l-4-2.md) |
