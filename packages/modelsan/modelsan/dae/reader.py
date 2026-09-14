"""Reading canonical DAE bitcode. One of the two places that knows the format."""

from __future__ import annotations

from pathlib import Path

from rumoca_bitcode import Model


def load(path: str | Path) -> Model:
    """Load a `.rbc` artifact.

    The encoding (CBOR or JSON) is detected from the bytes, so callers never
    choose one. That detection lives in the SDK codec, which is the boundary
    this function exists to keep sanitizers on the far side of.
    """
    return Model.load(str(path))
