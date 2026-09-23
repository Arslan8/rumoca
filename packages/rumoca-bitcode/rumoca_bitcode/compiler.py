"""Installed compiler boundary; Rust owns all semantic validation rules."""
from __future__ import annotations
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def compiler():
    command = os.environ.get("RUMOCA") or shutil.which("rumoca")
    if command:
        return command
    raise RuntimeError("rumoca executable not found; install it or set RUMOCA")


def invoke(*args):
    result = subprocess.run([compiler(), *map(str, args)], capture_output=True, text=True)
    if result.returncode:
        raise ValueError(result.stderr.strip() or result.stdout.strip())
    return result.stdout


def check_model(model, *, strict=True, connections=False):
    with tempfile.TemporaryDirectory(prefix="rbc-check-") as directory:
        path = Path(directory) / "model.rbc"
        model.save(path)
        invoke("bitcode", "check", path, *(["--strict"] if strict else []),
               *(["--connections"] if connections else []))
        if strict and model._document.get("execution") is None:
            invoke("compile-bitcode", path)
