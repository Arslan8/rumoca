"""Installed compiler boundary; Rust owns all semantic validation rules."""
from __future__ import annotations
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


#: The lowest compiler this package can speak to. Below it there is no
#: `bitcode` subcommand at all, so every call fails with an argument error
#: rather than anything a caller could diagnose.
MINIMUM_VERSION = (0, 10, 0)

#: Where a working copy keeps its build, newest profile first.
_IN_TREE = ("target/debug/rumoca", "target/release/rumoca")


def _repository_root():
    """The working copy this package lives in, if it lives in one."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "Cargo.toml").is_file() and (parent / "crates").is_dir():
            return parent
    return None


def candidates():
    """Every executable `compiler()` would consider, in order.

    `RUMOCA` first because an explicit choice beats a discovered one; then the
    working copy's own build, because that is the compiler whose source sits
    beside this package; then `PATH`.

    `PATH` used to come first, and on a machine with an old `cargo install`
    the suite silently ran against `rumoca 0.4.5` -- a version predating the
    `bitcode` subcommand -- and reported 30 failures against current code. A
    resolver that can pick a compiler older than the code under test does not
    produce test results, it produces a verdict about the wrong binary
    (TOOLBUG-026).
    """
    override = os.environ.get("RUMOCA")
    if override:
        yield override
        return
    root = _repository_root()
    if root is not None:
        for relative in _IN_TREE:
            path = root / relative
            if path.is_file():
                yield str(path)
    discovered = shutil.which("rumoca")
    if discovered:
        yield discovered


def version(executable):
    """`(major, minor, patch)` the executable reports, or None."""
    try:
        output = subprocess.run([executable, "--version"], capture_output=True,
                                text=True, timeout=30).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    for token in output.split():
        parts = token.split(".")
        if len(parts) == 3 and all(part.isdigit() for part in parts):
            return tuple(int(part) for part in parts)
    return None


def compiler():
    """The rumoca executable to run, refusing one that is too old.

    Refusing is the point. A compiler below `MINIMUM_VERSION` does not fail in
    a way a caller can read -- it rejects the subcommand and every downstream
    call reports its own unrelated error.
    """
    seen = []
    for command in candidates():
        found = version(command)
        if found is None or found >= MINIMUM_VERSION:
            return command
        seen.append((command, found))
    if seen:
        listing = "; ".join(
            f"{command} is {'.'.join(map(str, found))}" for command, found in seen)
        wanted = ".".join(map(str, MINIMUM_VERSION))
        raise RuntimeError(
            f"every rumoca found is older than {wanted}: {listing}. "
            f"Build the working copy (`cargo build`) or set RUMOCA.")
    raise RuntimeError("rumoca executable not found; install it or set RUMOCA")


def invoke(*args, executable=None, timeout=None):
    result = subprocess.run([executable or compiler(), *map(str, args)],
                            capture_output=True, text=True, timeout=timeout)
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
