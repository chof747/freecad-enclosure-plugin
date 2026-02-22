"""Shared result and error models for command operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CommandError:
    code: str
    message: str


@dataclass(frozen=True)
class CommandResult:
    ok: bool
    payload: dict[str, Any] | None = None
    error: CommandError | None = None


def success(payload: dict[str, Any]) -> CommandResult:
    return CommandResult(ok=True, payload=payload)


def failure(code: str, message: str) -> CommandResult:
    return CommandResult(ok=False, error=CommandError(code=code, message=message))
