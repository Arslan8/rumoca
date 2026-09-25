"""Synchronized canonical member samples for network laws.

Never align unrelated trajectories by array index or recover identity by name.
Nonfinite values belong to NumericSan; they are not conservation evidence.
"""
import math

from ..runtime.anchors import EntityKind
from ..runtime.observations import VariableObservation


class Samples:
    def __init__(self, stream, identifiers):
        self.values = {identifier: {} for identifier in identifiers}
        self.reason = ""
        for observation in stream.of(VariableObservation):
            anchor = observation.canonical
            if anchor is None or anchor.kind is not EntityKind.VARIABLE:
                continue
            points = self.values.get(anchor.dae_id)
            if points is None:
                continue
            t, value = observation.time, observation.value
            if (not isinstance(t, (int, float)) or not isinstance(value, (int, float))
                    or not math.isfinite(t) or not math.isfinite(value)):
                self.reason = "nonfinite or missing member sample"
                continue
            if t in points:
                self.reason = "duplicate member publication time"
            points[t] = value
        self.times = sorted({t for points in self.values.values() for t in points})
        if not self.times or any(set(points) != set(self.times) for points in self.values.values()):
            self.reason = "missing or unsynchronized connector member observations"

    def series(self, identifier):
        points = self.values.get(identifier)
        return None if self.reason or points is None else [points[t] for t in self.times]
