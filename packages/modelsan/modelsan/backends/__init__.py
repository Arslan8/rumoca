"""Execution backends. Everything tool-specific lives behind this boundary."""

from .base import Backend, ExecutionResult, Status
from .openmodelica import OpenModelicaBackend

__all__ = ["Backend", "ExecutionResult", "OpenModelicaBackend", "Status"]
