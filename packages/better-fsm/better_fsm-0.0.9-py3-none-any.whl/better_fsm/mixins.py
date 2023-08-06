from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from better_fsm.context import fsm_context

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext

T = TypeVar("T")


class FSMContextMixin:
    @classmethod
    @property
    def fsm(cls) -> FSMContext:
        """Returns current fsm context."""
        fsm = fsm_context.get(None)
        if fsm is None:
            msg = "`FSMContext` is not set. Use `FSMContextMiddleware`"
            raise ValueError(msg)

        return fsm
