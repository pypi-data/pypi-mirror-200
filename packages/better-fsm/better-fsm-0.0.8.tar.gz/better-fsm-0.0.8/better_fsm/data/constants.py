from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NotProvided:
    ...


NOT_PROVIDED = NotProvided()
"""A sentinel value to indicate that a default value was not provided."""
