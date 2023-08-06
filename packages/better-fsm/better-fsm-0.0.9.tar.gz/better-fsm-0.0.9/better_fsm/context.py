from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext

fsm_context: ContextVar[FSMContext] = ContextVar("fsm_context")
