"""Registration, so adding a sanitizer touches nothing else.

No central switch statement decides what runs. A sanitizer is registered, its
capabilities are discovered by protocol, and the driver asks the registry for
whichever capability it is about to use.
"""

from __future__ import annotations

from ..sanitizers.base import (
    DifferentialOracle,
    FuzzHintProvider,
    InstrumentationRequester,
    RuntimeObserver,
    StaticAnalyzer,
)


class SanitizerRegistry:
    def __init__(self) -> None:
        self._sanitizers: dict[str, object] = {}
        self._enabled: dict[str, bool] = {}

    def register(self, sanitizer, enabled: bool = True) -> None:
        name = getattr(sanitizer, "name", None)
        if not name:
            raise ValueError(f"{sanitizer!r} has no name")
        self._sanitizers[name] = sanitizer
        self._enabled[name] = enabled

    def enable(self, name: str, enabled: bool = True) -> None:
        if name in self._sanitizers:
            self._enabled[name] = enabled

    def configure(self, settings: dict) -> None:
        """Apply `{name: {"enabled": bool, ...}}` from external configuration."""
        for name, options in (settings or {}).items():
            if isinstance(options, dict) and "enabled" in options:
                self.enable(name, bool(options["enabled"]))
            elif isinstance(options, bool):
                self.enable(name, options)

    def active(self) -> list:
        return [s for name, s in self._sanitizers.items() if self._enabled.get(name)]

    def static_analyzers(self) -> list[StaticAnalyzer]:
        return [s for s in self.active() if isinstance(s, StaticAnalyzer)]

    def runtime_observers(self) -> list[RuntimeObserver]:
        return [s for s in self.active() if isinstance(s, RuntimeObserver)]

    def instrumentation_requesters(self) -> list[InstrumentationRequester]:
        return [s for s in self.active() if isinstance(s, InstrumentationRequester)]

    def hint_providers(self) -> list[FuzzHintProvider]:
        return [s for s in self.active() if isinstance(s, FuzzHintProvider)]

    def differential_oracles(self) -> list[DifferentialOracle]:
        return [s for s in self.active() if isinstance(s, DifferentialOracle)]

    def __len__(self) -> int:
        return len(self._sanitizers)

    def names(self) -> list[str]:
        return sorted(self._sanitizers)
