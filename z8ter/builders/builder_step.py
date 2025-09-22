"""A single build operation to be applied in the AppBuilder pipeline.

Attributes:
    name: Unique identifier for the step. Used for dependency checks.
    func: Callable that mutates the shared build context.
    requires: Names of prior steps that must have been applied.
    idempotent: If True, re-applying the same step is a no-op.
    kwargs: Extra data merged into context before calling `func`.

"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

BuilderFunc = Callable[[dict[str, Any]], None]


@dataclass
class BuilderStep:
    """Model representing a single build operation."""

    name: str
    func: BuilderFunc
    requires: list[str] = field(default_factory=list)
    idempotent: bool = False
    kwargs: dict[str, Any] = field(default_factory=dict)
