"""Reading user-supplied semantics from a file outside the Modelica source.

The brief's requirement is that a user can say what a model object means
without editing the model, so this reads a standalone file. Keeping it outside
the source is also what makes the mapping usable against a library the user
does not own.

    [semantics]
    "vehicle.chassis.v"        = "automotive.vehicle_speed"
    "vehicle.frontLeft.w"      = "automotive.wheel.angular_velocity"
    "vehicle.frontLeft.radius" = "automotive.wheel.radius"
    "battery.soc"              = "battery.state_of_charge"

    [physicalsan]
    profiles = ["automotive"]

A trailing `*` in a key matches a path prefix.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SemanticConfig:
    """One parsed semantics file."""

    mappings: dict[str, str] = field(default_factory=dict)
    profiles: tuple[str, ...] = ()
    origin: str = "<none>"

    @classmethod
    def load(cls, path: str | Path) -> "SemanticConfig":
        location = Path(path)
        data = tomllib.loads(location.read_text())
        return cls.from_dict(data, origin=str(location))

    @classmethod
    def from_dict(cls, data: dict, origin: str = "<inline>") -> "SemanticConfig":
        mappings = {str(k): str(v) for k, v in (data.get("semantics") or {}).items()}
        settings = data.get("physicalsan") or {}
        profiles = tuple(str(p) for p in (settings.get("profiles") or []))
        return cls(mappings=mappings, profiles=profiles, origin=origin)

    def __bool__(self) -> bool:
        return bool(self.mappings or self.profiles)
