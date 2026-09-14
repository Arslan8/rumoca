"""Turning a recorded trajectory into variable observations.

Backends produce trajectories in their own formats. This converts one into the
common observation vocabulary so sanitizers never parse a result file.
"""

from __future__ import annotations

from typing import Iterable

from .observations import ObservationStream, VariableObservation


def from_columns(
    times: Iterable[float],
    columns: dict[str, list[float]],
    ids: dict[str, int] | None = None,
) -> ObservationStream:
    """Build a stream from `{name: [values]}` aligned to `times`.

    `ids` maps variable names to DAE ids where the backend can supply them. A
    backend that cannot (OpenModelica reports names, not Rumoca ids) leaves the
    id as -1, and sanitizers relying on ids will simply not fire — which is the
    correct outcome, rather than inventing an id that means nothing.
    """
    stream = ObservationStream()
    ids = ids or {}
    times = list(times)
    for name, values in columns.items():
        variable_id = ids.get(name, -1)
        for index, value in enumerate(values):
            if index >= len(times):
                break
            stream.add(VariableObservation(
                time=times[index],
                variable_id=variable_id,
                name=name,
                value=value,
            ))
    return stream
