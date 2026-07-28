"""Tests for self-termination command detector — MacOS, Linux, Windows"""

from __future__ import annotations

import pytest

from code_puppy.plugins.self_termination_guardrail.detector import (
    TerminationCommandMatch,
    detect_self_termination_command,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _hits(cmd: str) -> TerminationCommandMatch | None:
    """Wrap with a shell operator so _is_real_command passes."""
    return detect_self_termination_command(f"&& {cmd}")


def _miss(cmd: str) -> bool:
    """Return True when the command is NOT flagged."""
    return detect_self_termination_command(f"&& {cmd}") is None


# ===========================================================================
# MacOS and Linux
# ===========================================================================


class TestPkillCommand:
    """pkill -flag protected_name"""

    @pytest.mark.parametrize(
        "cmd",
        [
            "pkill python3",
            "pkill code-puppy",
            "pkill code-puppy-venv",
            "pkill -9 login",
            "pkill -n Terminal",
            "pkill -U uid -- -zsh"
        ],
    )
    def test_matches(self, cmd: str) -> None:
        result = _hits(cmd)
        assert result is not None


class TestKillallCommand:
    """killall -flag protected_name"""

    @pytest.mark.parametrize(
        "cmd",
        [
            "killall python",
            "killall -9 bash",
            "killall zsh",
            "killall -x python3"
        ],
    )
    def test_matches(self, cmd: str) -> None:
        result = _hits(cmd)
        assert result is not None


# ===========================================================================
# Windows
# ===========================================================================


class TestTaskkillCommand:
    """taskkill -flag protected_name"""

    @pytest.mark.parametrize(
        "cmd",
        [
            "taskkill /IM python.exe",
            "taskkill /IM cmd.exe",
            "taskkill /F /IM WindowsTerminal.exe"
        ],
    )
    def test_matches(self, cmd: str) -> None:
        result = _hits(cmd)
        assert result is not None


class TestStopProcessCommand:
    """Stop-Process -flag protected_name"""

    @pytest.mark.parametrize(
        "cmd",
        [
            "Stop-Process -Name 'OpenConsole.exe'",
            "Stop-Process -Name 'conhost.exe' -Force"
            "spps -Name 'python3.exe'",
        ],
    )
    def test_matches(self, cmd: str) -> None:
        result = _hits(cmd)
        assert result is not None


# ===========================================================================
# False-positive guard
# ===========================================================================


class TestFalsePositives:
    """Commands that must NOT be flagged."""

    @pytest.mark.parametrize(
        "cmd",
        [
            "pkill notepad"
            "killall -9 'Google Chrome'"
            "echo 'Stop-Process -Name python'"
        ],
    )
    def test_safe_commands(self, cmd: str) -> None:
        assert _miss(cmd), f"False positive: {cmd!r} was flagged"