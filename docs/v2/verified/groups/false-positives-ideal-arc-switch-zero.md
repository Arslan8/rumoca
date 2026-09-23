# False positives and explicit non-defects: `ideal-arc-switch-zero`

**2 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

The quenched off-state is i=Goff*v and the closed state is v=Ron*i; neither parameter is divided. Ron=0 is the ideal closed switch and Goff=0 the ideal open switch, consistent with the base ideal-switch family. A particular connected circuit can still become structurally singular.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0051](../false-positives/DECL-0051.md) | — | `Goff` | Source/semantic review | [DECL-idealswitchwitharc-goff-5.md](../../bugs/DECL-idealswitchwitharc-goff-5.md) |
| [DECL-0659](../false-positives/DECL-0659.md) | — | `Ron` | Source/semantic review | [DECL-idealswitchwitharc-ron-4.md](../../bugs/DECL-idealswitchwitharc-ron-4.md) |
