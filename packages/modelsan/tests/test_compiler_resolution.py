"""Which rumoca the tools run, and refusing one too old to answer.

TOOLBUG-026. Three times in one day a stale executable produced a *verdict*:
a campaign read 11/11 cases as blocked against a binary seven minutes older
than the CLI it needed, a published evaluation recorded a detection as
impossible against a superseded build, and this suite reported 30 failures
because `shutil.which` found a `rumoca 0.4.5` in `~/.cargo/bin` that predates
the `bitcode` subcommand entirely.

None of those looked like configuration errors. They looked like results.
"""
from __future__ import annotations

import os
import stat
import sys
import tempfile
from pathlib import Path

import pytest

sys.path[:0] = [str(Path(__file__).resolve().parents[2] / "rumoca-bitcode")]

from rumoca_bitcode import compiler as boundary          # noqa: E402

ROOT = Path(__file__).resolve().parents[3]


def fake_rumoca(directory: Path, reported: str) -> Path:
    """An executable that answers `--version` and nothing else."""
    path = directory / "rumoca"
    path.write_text(f'#!/bin/sh\necho "rumoca {reported}"\n')
    path.chmod(path.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return path


@pytest.fixture
def without_override(monkeypatch):
    monkeypatch.delenv("RUMOCA", raising=False)


def test_the_working_copy_build_is_preferred_over_one_on_the_path(
        without_override, monkeypatch):
    """The exact failure: an old `cargo install` shadowing the build under test."""
    with tempfile.TemporaryDirectory() as directory:
        stale = fake_rumoca(Path(directory), "0.4.5")
        monkeypatch.setenv("PATH", str(stale.parent))
        chosen = Path(boundary.compiler())
        assert chosen != stale, "a PATH binary must not shadow the working copy"
        assert chosen.is_relative_to(ROOT / "target"), chosen


def test_an_explicit_override_still_wins(monkeypatch):
    with tempfile.TemporaryDirectory() as directory:
        chosen = fake_rumoca(Path(directory), "9.9.9")
        monkeypatch.setenv("RUMOCA", str(chosen))
        assert boundary.compiler() == str(chosen)


def test_a_compiler_below_the_minimum_is_refused_by_name_and_version(
        without_override, monkeypatch):
    """Refusing beats proceeding: 0.4.5 has no `bitcode` subcommand, so every
    later call fails with its own unrelated argument error and nothing names
    the cause."""
    with tempfile.TemporaryDirectory() as directory:
        stale = fake_rumoca(Path(directory), "0.4.5")
        monkeypatch.setenv("PATH", str(stale.parent))
        monkeypatch.setattr(boundary, "_repository_root", lambda: None)
        with pytest.raises(RuntimeError) as raised:
            boundary.compiler()
        message = str(raised.value)
        assert "0.4.5" in message and "0.10.0" in message
        assert str(stale) in message


def test_an_executable_that_reports_no_version_is_not_refused(
        without_override, monkeypatch):
    """A wrapper or a dev build may not print a parseable version. Unknown is
    not the same as too old, and refusing it would break a working setup."""
    with tempfile.TemporaryDirectory() as directory:
        odd = Path(directory) / "rumoca"
        odd.write_text("#!/bin/sh\necho 'custom build'\n")
        odd.chmod(odd.stat().st_mode | stat.S_IEXEC)
        monkeypatch.setenv("PATH", str(odd.parent))
        monkeypatch.setattr(boundary, "_repository_root", lambda: None)
        assert boundary.compiler() == str(odd)


def test_the_version_probe_reads_the_usual_output():
    assert boundary.version(boundary.compiler()) >= boundary.MINIMUM_VERSION
