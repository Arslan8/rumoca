"""Writing canonical DAE bitcode back out.

A transformation that cannot be serialized is not a transformation of the model,
it is a local edit to a Python object. Instrumentation passes go through here so
that what runs is what was analysed.
"""

from __future__ import annotations

from pathlib import Path

from rumoca_bitcode import Model


def save(model: Model, path: str | Path) -> Path:
    """Serialize `model` and return where it was written.

    Rumoca re-validates on import and rebuilds by *replaying* construction
    operations, so an artifact this produces is checked against the same 70
    construction invariants an original compile was. A pass that corrupts the
    model fails at load rather than at simulation.
    """
    destination = Path(path)
    model.save(str(destination))
    return destination
