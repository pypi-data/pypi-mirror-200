from __future__ import annotations

from typing import Any, TypeVar, overload

from aiogram.fsm.state import StatesGroup

from better_fsm.mixins import FSMContextMixin
from better_fsm.states.state import ExtendedState

T = TypeVar("T")
G = TypeVar("G")


class AllDataMapping(dict[str, Any]):
    @overload
    def __getitem__(
        self,
        key: ExtendedState[T],
        *,
        deserialize: bool = True,
    ) -> T:
        ...

    @overload
    def __getitem__(
        self,
        key: str,
        *,
        deserialize: bool = True,
    ) -> Any:
        ...

    def __getitem__(
        self,
        key: str | ExtendedState[Any],
        *,
        deserialize: bool = True,
    ) -> Any:
        if isinstance(key, ExtendedState):
            return key.data.get_from_data(self, deserialize=deserialize)

        return super().__getitem__(key)

    @overload
    def get(
        self,
        key: ExtendedState[T],
        default: G,
        *,
        deserialize: bool = True,
    ) -> T | G:
        ...

    @overload
    def get(
        self,
        key: ExtendedState[T],
        default: None = None,
        *,
        deserialize: bool = True,
    ) -> T | None:
        ...

    @overload
    def get(
        self,
        key: str,
        default: None = None,
        *,
        deserialize: bool = True,
    ) -> Any | None:
        ...

    def get(
        self,
        key: str | ExtendedState[Any],
        default: G | None = None,
        *,
        deserialize: bool = True,
    ) -> Any | G:
        try:
            return self.__getitem__(key, deserialize=deserialize)
        except KeyError:
            return default

    def __contains__(self, key: str | ExtendedState[Any] | Any) -> bool:
        if isinstance(key, ExtendedState):
            key = key.data.key

        return super().__contains__(key)


class ExtendedStateGroup(StatesGroup, FSMContextMixin):
    @classmethod
    async def get_all_data(cls) -> AllDataMapping:
        data = await cls.fsm.get_data()
        return AllDataMapping(data)
