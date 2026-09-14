"""Turning a recorded trajectory into variable observations.

Backends produce trajectories in their own formats. This converts one into the
common vocabulary so no sanitizer parses a result file.
"""

from __future__ import annotations

from typing import Iterable

from .anchors import BackendAnchor, CanonicalAnchor, EntityKind
from .observations import ObservationStream, VariableObservation


def from_columns(
    times: Iterable[float],
    columns: dict[str, list[float]],
    backend: str,
    canonical: dict[str, int] | None = None,
) -> ObservationStream:
    """Build a stream from `{name: [values]}` aligned to `times`.

    `canonical` maps names to DAE ids and is supplied only by a backend that
    genuinely knows the mapping. A backend that does not — OpenModelica reports
    names — leaves it out, and the observation carries a backend anchor alone.
    Manufacturing an id here would make every downstream anchor a lie.
    """
    stream = ObservationStream()
    canonical = canonical or {}
    times = list(times)
    for name, values in columns.items():
        dae_id = canonical.get(name)
        anchor = (CanonicalAnchor(EntityKind.VARIABLE, dae_id, name)
                  if dae_id is not None else None)
        fallback = None if anchor else BackendAnchor(backend, name, EntityKind.VARIABLE)
        for index, value in enumerate(values):
            if index >= len(times):
                break
            stream.add(VariableObservation(
                time=times[index], canonical=anchor, backend=fallback, value=value))
    return stream
