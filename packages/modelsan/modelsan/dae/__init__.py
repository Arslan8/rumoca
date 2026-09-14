"""Bindings over Rumoca's canonical DAE bitcode.

This package is **not** a second intermediate representation. Every object here
is a view onto the bitcode Rumoca produced, and every id it exposes is the id
the DAE assigned. There is no translation step, and there is nothing ModelSan
can express that the DAE cannot.

The single rule this package exists to enforce is that nothing above it knows
how the DAE is serialized. A sanitizer asks for `equation.residual`; it never
sees `raw["equations"][17]["residual"]`. If the encoding changes from CBOR to
something else, only `reader.py` and `writer.py` change.
"""

from rumoca_bitcode import (
    BinaryOp,
    BuiltinCall,
    Conditional,
    Expression,
    Literal,
    Model,
    UnaryOp,
    Unsupported,
    VariableRef,
)

from .reader import load
from .traversal import (
    denominators,
    equations_reading,
    expression_by_id,
    walk_expressions,
)
from .writer import save

__all__ = [
    "BinaryOp",
    "BuiltinCall",
    "Conditional",
    "Expression",
    "Literal",
    "Model",
    "UnaryOp",
    "Unsupported",
    "VariableRef",
    "denominators",
    "equations_reading",
    "expression_by_id",
    "load",
    "save",
    "walk_expressions",
]
