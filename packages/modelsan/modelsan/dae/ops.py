"""The DAE's operator vocabulary, named once.

These strings come from `RbcBinaryOp` in the bitcode schema, serialized
snake_case. They are defined here rather than inline in each sanitizer because
getting one wrong is silent: a sanitizer matching `"Mul"` against `"multiply"`
finds nothing and looks like a clean result, which is precisely the failure the
capability planner exists to prevent elsewhere.
"""

from __future__ import annotations

ADD = "add"
SUBTRACT = "subtract"
MULTIPLY = "multiply"
DIVIDE = "divide"
POWER = "power"

ARITHMETIC = frozenset({ADD, SUBTRACT, MULTIPLY, DIVIDE, POWER})

#: Relations, which are what an event or a conditional switches on.
RELATIONS = frozenset({"equal", "not_equal", "less", "less_equal",
                       "greater", "greater_equal"})

LOGICAL = frozenset({"and", "or"})

#: Every operator the schema defines. Used by the self-check below.
ALL = ARITHMETIC | RELATIONS | LOGICAL
