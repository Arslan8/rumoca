"""Validate dense backend traces before turning cells into observations."""

from __future__ import annotations

import csv
from dataclasses import dataclass
import math
from pathlib import Path


@dataclass
class CsvSamples:
    """Rectangular numeric samples; timestamp order is a separate obligation."""

    times: list[float]
    columns: dict[str, list[float]]


class UnorderedTraceError(ValueError):
    """Valid measured values with unusable temporal ordering, never a Trace."""

    def __init__(self, samples: CsvSamples, row: int):
        super().__init__(f"decreasing time at row {row}")
        self.samples = samples


def _read_samples(path: Path) -> CsvSamples:
    if not path.exists():
        return CsvSamples([], {})
    columns: dict[str, list[float]] = {}
    with path.open(newline="") as handle:
        reader = csv.reader(handle, strict=True)
        header = next(reader, None)
        if not header:
            raise ValueError("empty CSV")
        names = [name.strip() for name in header]
        if "time" not in names or any(not name for name in names) or len(set(names)) != len(names):
            raise ValueError("CSV requires time and unique nonempty column names")
        for name in names:
            columns[name] = []
        for line, row in enumerate(reader, 2):
            if len(row) != len(names):
                raise ValueError(f"CSV row {line} has {len(row)} cells, expected {len(names)}")
            for name, cell in zip(names, row):
                try:
                    columns[name].append(float(cell))
                except ValueError as error:
                    raise ValueError(f"invalid numeric cell at row {line}, column {name}") from error
            time = columns["time"][-1]
            if not math.isfinite(time):
                raise ValueError(f"nonfinite time at row {line}")
    return CsvSamples(columns.pop("time", []), columns)


def read_csv_trace(path: Path) -> tuple[list[float], dict[str, list[float]]]:
    """Allow event-side duplicate times and real NaNs, never repair evidence.

    Validate all cells before exposing values from an unordered result. A later
    malformed row must not be hidden by an earlier timestamp-order failure.
    """
    samples = _read_samples(path)
    for index in range(1, len(samples.times)):
        if samples.times[index] < samples.times[index-1]:
            raise UnorderedTraceError(samples, index+2)
    return samples.times, samples.columns
