# TOOLBUG-021: every published location named a file the reader might not find

| | |
|---|---|
| **Component** | `modelsan.findings.location.locate` |
| **Severity** | Medium — it broke the verification step in published reports, not the analysis |
| **Found by** | Adjudicating a fresh `physical-domain-unenforced` sample, 2026-09-16 |
| **Status** | Fixed. Locations carry the repository-relative path; four cases in `tests/test_location.py`. |

## The defect

Findings reported `HollowCylinderAxialFlux.mo:16`. Four files in MSL are called
`HollowCylinderAxialFlux.mo` and ten if the icon and quasi-static packages are
counted, and the published report told the reader to run

```console
$ sed -n '16p' "$(find target/msl target/corpus -name 'HollowCylinderAxialFlux.mo' | head -1)"
```

which opens `Magnetic/FluxTubes/Icons/HollowCylinderAxialFlux.mo`. That file is
nine lines long, so the command printed nothing, and the step the report calls
"the check that decides whether it is right" produced no output at all.

The declaration the finding was actually about is in
`Magnetic/FluxTubes/Shapes/Force/HollowCylinderAxialFlux.mo:16`:

```modelica
parameter SI.Area A=pi*(r_o^2 - r_i^2)
```

The bitcode always carried the full path — `Source.name` holds whatever Rumoca
was handed. `locate()` read `Source.short_name`, the basename, and the
information was discarded one call before it was published.

## Why it survived

This is the second defect in the same four lines. The first reported `?` for
every location, in every finding this project ever produced, because `Span` has
no `source_name` and the code read one with a `getattr` default. Fixing that
made the locations *look* right, and a plausible-looking basename passes
inspection in a way `?` does not.

A basename is right for a heading. It is not a location, and a report whose
verification step sends the reader to the wrong file is worse than one that
admits it does not know.

## The fix

`locate()` reports `Source.name`, made relative to the repository root when the
compiler recorded an absolute path, so a published finding carries no trace of
the machine it was produced on. The generator emits `sed -n '16p' '<path>'`
directly, and keeps the old search — with the ambiguity stated in the report —
for findings from runs made before this change.

## Effect

Every location in `docs/v2/bugs/` and `docs/declaration-sites/` is now a path a
reader can open. The analysis is unchanged: no finding was added, removed, or
re-decided by this, because nothing reasoned about the location.
