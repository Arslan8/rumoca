"""Resolving a DAE provenance to a source location.

One function, because the eight sanitizers that report a location each had
their own copy and every copy had the same bug:

    SourceLocation(file=getattr(span, "source_name", "") or "?", ...)

`Span` has no `source_name`. It has `source`, a `Source` with `.short_name`, so
`getattr` fell through to the default on every call and **every location this
project has ever reported was `?`** — findings, site reports and all. The `or
"?"` made it look deliberate.

The replacement then reported `.short_name`, the basename, and ten files in MSL
are called `HollowCylinderAxialFlux.mo`. A report saying
`HollowCylinderAxialFlux.mo:16` and telling the reader to `sed -n 16p` the first
match sends them to `Icons/HollowCylinderAxialFlux.mo`, which has no line 16. A
location has to identify the file, so it carries the path.
"""

from __future__ import annotations

import os

from .finding import SourceLocation


def locate(owner) -> list[SourceLocation]:
    """The declaration site of `owner`, as a one-element list, or empty.

    `owner` may be anything carrying `.source.span` (a DAE variable, an
    invariant) or a provenance carrying `.span` directly; both shapes occur and
    the caller should not have to know which it holds.
    """
    span = getattr(owner, "span", None)
    if span is None:
        source = getattr(owner, "source", None)
        span = getattr(source, "span", None) if source is not None else None
    if span is None:
        return []

    origin = getattr(span, "source", None)
    name = getattr(origin, "name", None) or getattr(origin, "short_name", None)
    return [SourceLocation(file=_relative(name) if name else "?",
                           line=getattr(span, "line", 0) or 0)]


def _relative(name: str) -> str:
    """The path as a reader of this repository would type it.

    Rumoca records whichever path it was handed, so the same file arrives
    absolute from one entry point and relative from another. Reporting the
    absolute one embeds this machine's layout in every published finding.
    """
    if not os.path.isabs(name):
        return name
    try:
        inside = os.path.relpath(name, os.getcwd())
    except ValueError:            # different drive on Windows
        return name
    return name if inside.startswith(os.pardir) else inside
