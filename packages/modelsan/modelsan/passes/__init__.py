"""Passes that change an artifact, rather than only reading one.

An LLVM pass inserts instructions; a pass here inserts equations. The power is
not less — a hybrid DAE with discrete state is Turing complete — but the shape
is declarative, and the artifact stays total so every analysis in this package
still terminates on the result.

The builder lives in the SDK, not here. It was written in this package first
and that was the wrong home: writing an artifact is part of the *format's*
contract, and a consumer with no interest in sanitizers should not have to
install one to produce a model.
"""

from rumoca_bitcode.builder import Builder, generated

from .energy import inject_port_energy

#: Marks everything a pass adds, so a reader can tell the instrument from the
#: model.
INSTRUMENTATION = "instrumentation"

__all__ = ["Builder", "INSTRUMENTATION", "generated", "inject_port_energy"]
