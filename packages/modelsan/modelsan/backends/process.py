"""Bound external backend process trees while preserving their diagnostics."""

from __future__ import annotations

import os
from pathlib import Path
import signal
import subprocess


def _kill_process_group(process: subprocess.Popen) -> None:
    try:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
    except ProcessLookupError:
        pass


def execute(command: list[str], work: Path, timeout: float, *,
            env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    """A timeout kills the compiler/simulator and its children, then drains output."""
    process = subprocess.Popen(command, cwd=work, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, env=env,
                               start_new_session=os.name == "posix")
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as error:
        _kill_process_group(process)
        stdout, stderr = process.communicate()
        raise subprocess.TimeoutExpired(command, timeout, output=stdout,
                                        stderr=stderr) from error
    except BaseException:
        _kill_process_group(process)
        process.communicate()
        raise
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
