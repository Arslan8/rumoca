#!/usr/bin/env python3
"""Declaration-contradiction detector for Modelica source.

Every other ModelSan detector needs the model to compile, which limits it to
the fraction of a corpus the compiler supports. These checks read declarations
only, so they reach every file.

A declaration contradiction is a bug in the *model*: the component states a
constraint and then violates it itself. Nothing about the solver, the compiler
or the numerics is involved, which is why these are high-precision.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path

# Built-in and MSL constants that appear in bounds.
CONSTANTS = {
    "Modelica.Constants.eps": 2.220446049250313e-16,
    "Constants.eps": 2.220446049250313e-16,
    "Modelica.Constants.small": 1e-60,
    "Constants.small": 1e-60,
    "Modelica.Constants.inf": math.inf,
    "Constants.inf": math.inf,
    "Modelica.Constants.pi": math.pi,
    "Constants.pi": math.pi,
    "eps": 2.220446049250313e-16,
    "small": 1e-60,
    "inf": math.inf,
    "pi": math.pi,
}

# `parameter SI.Mass m(min=0, start=1) = 2 "desc";` and friends. The modifier
# group is captured whole and split later, because it nests.
DECL = re.compile(
    r"\b(?:(final|inner|outer|replaceable)\s+)*"
    r"(parameter|constant)?\s*"
    r"(?:input|output|flow|stream|discrete)?\s*"
    r"([A-Za-z_][\w.]*)\s+"          # type
    r"([A-Za-z_]\w*)\s*"             # name
    r"(?:\[[^\]]*\])?\s*"            # optional dimensions
    r"\(([^;]*?)\)"                  # modifiers
    r"\s*(=\s*([^;\"]+?))?\s*(?:\"|;)",
    re.S,
)


def numeric(text: str) -> float | None:
    """Value of a bound, when it is a literal or a known constant.

    Anything else — an expression, another parameter — is left alone. A checker
    that guesses here reports contradictions that are not there.
    """
    token = text.strip().rstrip(",")
    if not token:
        return None
    negative = token.startswith("-")
    if negative:
        token = token[1:].strip()
    value = None
    try:
        value = float(token)
    except ValueError:
        if token in CONSTANTS:
            value = CONSTANTS[token]
    if value is None:
        return None
    return -value if negative else value


def modifiers(text: str) -> dict[str, str]:
    """Split a modifier list at top level, ignoring nested parentheses."""
    found, depth, current = [], 0, ""
    for char in text:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        if char == "," and depth == 0:
            found.append(current)
            current = ""
        else:
            current += char
    found.append(current)

    out = {}
    for item in found:
        if "=" not in item:
            continue
        key, _, value = item.partition("=")
        key = key.strip()
        if key in ("min", "max", "start", "nominal", "fixed", "unit", "quantity"):
            out[key] = value.strip()
    return out


@dataclass
class Finding:
    kind: str
    file: str
    line: int
    name: str
    type_name: str
    detail: str
    severity: str = "medium"


@dataclass
class Declaration:
    name: str
    type_name: str
    line: int
    is_parameter: bool
    min: float | None = None
    max: float | None = None
    start: float | None = None
    nominal: float | None = None
    default: float | None = None
    raw: dict = field(default_factory=dict)


def declarations(text: str) -> list[Declaration]:
    out = []
    for match in DECL.finditer(text):
        variability, type_name, name, mods, default = (
            match.group(2), match.group(3), match.group(4),
            match.group(5), match.group(7),
        )
        if type_name in ("if", "for", "while", "when", "elsewhen", "connect", "return"):
            continue
        raw = modifiers(mods)
        out.append(Declaration(
            name=name,
            type_name=type_name,
            line=text[: match.start()].count("\n") + 1,
            is_parameter=variability == "parameter",
            min=numeric(raw.get("min", "")) if "min" in raw else None,
            max=numeric(raw.get("max", "")) if "max" in raw else None,
            start=numeric(raw.get("start", "")) if "start" in raw else None,
            nominal=numeric(raw.get("nominal", "")) if "nominal" in raw else None,
            default=numeric(default or ""),
            raw=raw,
        ))
    return out


def check(decl: Declaration, path: str) -> list[Finding]:
    """Contradictions between a declaration's own modifiers."""
    found = []
    here = dict(file=path, line=decl.line, name=decl.name, type_name=decl.type_name)

    if decl.min is not None and decl.max is not None and decl.min > decl.max:
        found.append(Finding(
            "min-exceeds-max", **here, severity="high",
            detail=f"min={decl.min:g} is greater than max={decl.max:g}; "
                   "no value satisfies the declaration",
        ))

    if decl.start is not None:
        if decl.min is not None and decl.start < decl.min:
            found.append(Finding(
                "start-below-min", **here,
                detail=f"start={decl.start:g} violates the same declaration's min={decl.min:g}",
            ))
        if decl.max is not None and decl.start > decl.max:
            found.append(Finding(
                "start-above-max", **here,
                detail=f"start={decl.start:g} violates the same declaration's max={decl.max:g}",
            ))

    if decl.default is not None:
        if decl.min is not None and decl.default < decl.min:
            found.append(Finding(
                "default-below-min", **here, severity="high",
                detail=f"declared default {decl.default:g} violates its own min={decl.min:g}",
            ))
        if decl.max is not None and decl.default > decl.max:
            found.append(Finding(
                "default-above-max", **here, severity="high",
                detail=f"declared default {decl.default:g} violates its own max={decl.max:g}",
            ))

    # MLS 4.8.6: nominal is a scaling magnitude; zero or negative is meaningless
    # and a solver dividing by it produces inf.
    if decl.nominal is not None and decl.nominal <= 0:
        found.append(Finding(
            "nonpositive-nominal", **here, severity="high",
            detail=f"nominal={decl.nominal:g} is not a usable scale factor",
        ))

    return found


def scan_file(path: Path, root: Path) -> list[Finding]:
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return []
    relative = str(path.relative_to(root))
    return [f for decl in declarations(text) for f in check(decl, relative)]


def scan(root: Path) -> list[Finding]:
    return [f for mo in sorted(root.rglob("*.mo")) for f in scan_file(mo, root)]


# ── Usage-vs-declaration checks ──────────────────────────────────────────────
#
# The findings so far (BUG-002, 003, 005, 006) are one family: a parameter
# whose declared domain admits a value its own equations cannot survive. The
# census in docs/findings/min0-census.md covered parameters that declare
# `min=0`. This covers the larger set that declare no lower bound at all.

PARAM_ANY = re.compile(
    r"\bparameter\s+([A-Za-z_][\w.]*)\s+([A-Za-z_]\w*)\s*"
    r"(?:\[[^\]]*\])?\s*(?:\(([^;]*?)\))?\s*(?:=|\"|;)",
    re.S,
)


def divides_by(body: str, name: str) -> bool:
    """`name` appears as a denominator."""
    return bool(re.search(r"/\s*\(?\s*" + re.escape(name) + r"\b", body))


def guards(body: str, name: str) -> bool:
    """The model excludes the degenerate value itself.

    MSL has two correct idioms besides tightening the bound: a structural
    branch (`if G > 0 then ... else V_m.re = 0`) and a guarded expression
    (`if rising > 0 then amplitude/rising else 0`). Neither is a defect.
    """
    n = re.escape(name)
    return bool(
        re.search(r"\b" + n + r"\s*(>|<>|>=)\s*0", body)
        or re.search(r"abs\s*\(\s*" + n + r"\s*\)\s*>", body)
    )


def unbounded_divisors(text: str, path: str) -> list[Finding]:
    """Parameters used as a divisor whose declaration does not exclude zero."""
    index = text.find("equation")
    body = text[index:] if index >= 0 else ""
    if not body:
        return []

    found = []
    for match in PARAM_ANY.finditer(text):
        type_name, name, mods = match.group(1), match.group(2), match.group(3) or ""
        if not divides_by(body, name) or guards(body, name):
            continue
        low = numeric(modifiers(mods).get("min", "")) if "min" in modifiers(mods) else None
        if low is not None and low > 0:
            continue  # correctly bounded away from zero
        found.append(Finding(
            "unbounded-divisor",
            file=path,
            line=text[: match.start()].count("\n") + 1,
            name=name,
            type_name=type_name,
            detail=(
                f"used as a divisor; declared lower bound is "
                + ("absent" if low is None else f"min={low:g}")
                + ", so zero is a permitted value and no guard excludes it"
            ),
            severity="medium",
        ))
    return found


def scan_usage(root: Path) -> list[Finding]:
    out = []
    for mo in sorted(root.rglob("*.mo")):
        try:
            text = mo.read_text(errors="replace")
        except OSError:
            continue
        out += unbounded_divisors(text, str(mo.relative_to(root)))
    return out
