from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware

from better_fsm.context import fsm_context

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram.types import TelegramObject


class FSMContextMiddleware(BaseMiddleware):
    """Sets current fsm context to the context var."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        state = data.get("state")
        if state is None:
            logger.error("State is None, can't set the context")
            return await handler(event, data)

        token = fsm_context.set(state)
        result = await handler(event, data)
        fsm_context.reset(token)

        return result
