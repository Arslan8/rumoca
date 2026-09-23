"""Python transport for the native linker; no second reference-remapping policy."""
from collections.abc import Mapping
from pathlib import Path
import tempfile

from . import Model, _cbor
from .compiler import invoke


def link(modules: Mapping[str, Model | str | Path], *, name: str = "LinkedModel",
         discard_execution: bool = False) -> Model:
    """Return a new equation model from an ordered namespace -> Model/path map.

    Namespaces are distinct simple identifiers, never inferred from filenames.
    Equations and boundary conditions are preserved; this does not connect ports.
    """
    if not isinstance(modules, Mapping) or not modules:
        raise ValueError("link requires a nonempty namespace -> Model/path mapping")
    with tempfile.TemporaryDirectory(prefix="rbc-link-") as directory:
        root = Path(directory)
        inputs = []
        for index, (namespace, module) in enumerate(modules.items()):
            if not isinstance(namespace, str) or "=" in namespace:
                raise ValueError("namespace must be a simple identifier")
            if isinstance(module, Model):
                path = root / f"input-{index}.rbc"
                # Do not refresh, renumber, save over, or mutate the input model.
                path.write_bytes(_cbor.dumps(module._document))
            else:
                path = Path(module).resolve()
            inputs.append(f"{namespace}={path}")
        output = root / "linked.rbc"
        invoke("bitcode", "link", *inputs, "--name", name, "-o", output,
               *(["--discard-execution"] if discard_execution else []))
        return Model.load(output)
