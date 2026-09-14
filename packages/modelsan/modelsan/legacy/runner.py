"""Drive Rumoca to test one parameter configuration.

ModelSan does not simulate anything itself. It asks Rumoca to, because a second
evaluator would be a second set of numerical behaviour to explain. Rumoca
already refuses a solve that goes non-finite and names the variable and span,
which is a better detector than anything reimplemented here.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


class RumocaNotFound(RuntimeError):
    pass


def find_rumoca(explicit: str | None = None) -> str:
    for candidate in (explicit, "rumoca", "./target/debug/rumoca", "./target/release/rumoca"):
        if not candidate:
            continue
        found = shutil.which(candidate) or (candidate if Path(candidate).is_file() else None)
        if found:
            return found
    raise RumocaNotFound(
        "cannot find the `rumoca` binary; pass --rumoca PATH or put it on $PATH"
    )


def resolve_span(model, message: str) -> str | None:
    """Turn `BytePos(271)` in a Rumoca message into `Orifice.mo:10:8`.

    Rumoca reports a raw span. Rather than re-deriving line and column from
    source text, this matches the offsets against the spans the artifact
    already carries, which were resolved at export time. An exact match is
    therefore exact; no match returns nothing rather than a guess.
    """
    import re

    found = re.search(r"start: BytePos\((\d+)\).*?end: BytePos\((\d+)\)", message)
    if not found:
        return None
    start, end = int(found.group(1)), int(found.group(2))

    for expression in model.expressions:
        span = expression.provenance.span
        if span.start == start and span.end == end:
            return str(span)
    for equation in model.equations:
        span = equation.source.span
        if span.start == start and span.end == end:
            return str(span)
    return None


@dataclass
class Outcome:
    """What happened for one configuration."""

    ok: bool
    findings: list
    stderr: str

    @property
    def kind(self) -> str | None:
        return self.findings[0].get("kind") if self.findings else None

    @property
    def detail(self) -> str:
        if not self.findings:
            return ""
        finding = self.findings[0]
        if finding.get("kind") == "simulation-failure":
            return finding.get("detail", "")
        return (
            f"{finding.get('variable')} = {finding.get('value')}"
            f" at t = {finding.get('time')}"
        )


def run(
    rumoca: str,
    artifact: Path,
    assignment: dict[str, float],
    *,
    t_end: float = 1.0,
    timeout: float = 60.0,
) -> Outcome:
    """Simulate one configuration and collect any property violation."""
    command = [
        rumoca,
        "compile-bitcode",
        str(artifact),
        "--simulate",
        "--check",
        "--t-end",
        str(t_end),
    ]
    for name, value in assignment.items():
        command += ["--param", f"{name}={value!r}"]

    try:
        completed = subprocess.run(
            command, capture_output=True, text=True, timeout=timeout, check=False
        )
    except subprocess.TimeoutExpired:
        # A configuration that hangs the solver is itself a finding: it is a
        # model that cannot be integrated, not a model that is fine.
        return Outcome(
            ok=False,
            findings=[{"kind": "timeout", "detail": f"no result within {timeout}s"}],
            stderr="",
        )

    findings = []
    if completed.stdout.strip():
        try:
            findings = json.loads(completed.stdout)
        except json.JSONDecodeError:
            findings = []

    # Exit 2 is the agreed "this configuration violates a property" signal.
    # Any other non-zero exit is a tooling problem, not a model finding, and is
    # reported rather than counted as a discovery.
    if completed.returncode not in (0, 2):
        return Outcome(
            ok=False,
            findings=[{"kind": "tool-error", "detail": completed.stderr.strip()[:400]}],
            stderr=completed.stderr,
        )

    return Outcome(ok=completed.returncode == 0, findings=findings, stderr=completed.stderr)


def export(rumoca: str, model_file: Path, model_name: str | None, out: Path,
           source_roots: list[str] | None = None) -> Path:
    """Compile a `.mo` to bitcode."""
    command = [rumoca, "compile", str(model_file), "--emit-bitcode", str(out)]
    if model_name:
        command += ["--model", model_name]
    for root in source_roots or []:
        command += ["--source-root", root]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0 or not out.exists():
        raise RuntimeError(
            f"rumoca could not compile {model_file}:\n{completed.stderr.strip()[:1200]}"
        )
    return out
