from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Any, Generic, Self

from aiogram.fsm.state import State
from typing_extensions import TypeVar

from better_fsm.data.manager import DataManager
from better_fsm.states.manager import (
    EXTENDED_STATE_MANAGER,
    INITED_STATES,
    ExtendedStateManager,
)
from better_fsm.utils.attrs import lazy_attribute

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable


DataTypeT = TypeVar("DataTypeT", bound=Any, default=Any)
NextStateT = TypeVar(
    "NextStateT",
    bound="ExtendedState | None",
    default="ExtendedState[Any, Any]",
)


class ExtendedState(State, Generic[DataTypeT, NextStateT]):
    def __init__(  # noqa: PLR0913
        self,
        data_manager: DataManager[DataTypeT]
        | type[DataManager[DataTypeT]] = DataManager[Any],
        next_state: Callable[[], NextStateT] | NextStateT | None = None,
        manager: ExtendedStateManager = EXTENDED_STATE_MANAGER,
        state: str | None = None,
        group_name: str | None = None,
        on_enter: Callable[[], Awaitable[None]] | None = None,
        on_exit: Callable[[], Awaitable[None]] | None = None,
    ) -> None:
        super().__init__(
            state=state,
            group_name=group_name,
        )

        self.manager = manager
        self._data_manager = data_manager

        if next_state is None:
            self._next_state_factory = partial(
                self.manager.get_next_state,
                current_state=self,
            )
        elif isinstance(next_state, ExtendedState):
            self._next_state_factory = lambda: next_state
        else:
            self._next_state_factory = next_state

        async def _do_nothing() -> None:
            pass

        self.on_enter = on_enter or _do_nothing
        self.on_exit = on_exit or _do_nothing

        INITED_STATES.append(self)

    async def set(self) -> Self:
        """Set current state equal to this state."""
        current_state = await self.get_current()
        if current_state is not None:
            await current_state.on_exit()

        await self.on_enter()
        return await self.manager.set(self)

    @lazy_attribute
    def data(self) -> DataManager[DataTypeT]:
        if isinstance(self._data_manager, DataManager):
            if not self._data_manager.has_key:
                self._data_manager.set_key(self.data_key)

            return self._data_manager

        return self._data_manager(key=self.data_key)

    @lazy_attribute
    def data_key(self) -> str:
        if (
            isinstance(self._data_manager, DataManager)
            and self._data_manager.has_key
        ):
            return self._data_manager.key

        if self.state is not None:
            return self.state.replace(":", "_")

        msg = "`data_key` is not provided"
        raise ValueError(msg)

    @lazy_attribute
    def next(self) -> NextStateT:
        next_state = self._next_state_factory()
        if next_state is None:
            msg = f"`next_state` is not provided for '{self.state}'"
            raise ValueError(msg)

        return next_state

    async def is_active(self) -> bool:
        """Check if current state is equal to this state."""
        return await self.manager.is_active(self)

    async def get_current(self) -> ExtendedState[Any, Any] | None:
        return await self.manager.get_current_state()

    if not TYPE_CHECKING:

        def __class_getitem__(
            cls,
            item: type[Any] | tuple[type[Any], ...],
        ) -> ExtendedState:
            """Allow to use with default type arguments."""
            if not isinstance(item, tuple):
                item = (item,)

            return super().__class_getitem__(item)
