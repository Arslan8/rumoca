"""A reported location has to name a file the reader can open.

Ten files in MSL are called `HollowCylinderAxialFlux.mo`. A finding that says
`HollowCylinderAxialFlux.mo:16` names four of them, and the published
verification step — search for the basename, take the first match, print line
16 — lands on `Icons/HollowCylinderAxialFlux.mo`, which is nine lines long.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from modelsan.findings.location import locate


@dataclass
class _Source:
    name: str

    @property
    def short_name(self) -> str:
        return os.path.basename(self.name)


@dataclass
class _Span:
    source: _Source
    line: int


@dataclass
class _Owner:
    span: _Span


def test_the_location_keeps_the_directory():
    where = locate(_Owner(_Span(_Source("target/msl/Shapes/Force/H.mo"), 16)))
    assert where[0].file == "target/msl/Shapes/Force/H.mo"
    assert where[0].line == 16


def test_an_absolute_path_inside_the_repository_is_made_relative():
    absolute = os.path.join(os.getcwd(), "target", "msl", "Units.mo")
    where = locate(_Owner(_Span(_Source(absolute), 3)))
    assert where[0].file == "target/msl/Units.mo"


def test_an_absolute_path_outside_the_repository_is_left_alone():
    where = locate(_Owner(_Span(_Source("/opt/msl/Units.mo"), 3)))
    assert where[0].file == "/opt/msl/Units.mo"


def test_no_span_reports_no_location():
    assert locate(_Owner(None)) == []
