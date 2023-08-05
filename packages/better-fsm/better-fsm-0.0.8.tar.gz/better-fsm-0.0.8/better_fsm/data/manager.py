from __future__ import annotations

from asyncio import Lock
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Generic, TypeAlias, TypeVar, overload

from better_fsm.data.constants import NOT_PROVIDED, NotProvided
from better_fsm.data.exceptions import (
    EMPTY_KEY_ERROR,
    KEY_ALREADY_SET_ERROR,
    KeyDoesNotExistError,
)
from better_fsm.mixins import FSMContextMixin
from better_fsm.utils.attrs import lazy_attribute

T = TypeVar("T")

JSONABLE: TypeAlias = Any

Serializer = Callable[[T], JSONABLE]
Deserializer = Callable[[JSONABLE], T]


Default: TypeAlias = T | NotProvided


@dataclass(slots=True)
class DataManager(Generic[T], FSMContextMixin):
    serializer: Serializer[T] | None = None
    deserializer: Deserializer[T] | None = None

    _key: str | None = field(init=False, repr=False, compare=False)

    def __init__(
        self,
        key: str | None = None,
        serializer: Serializer[T] | None = None,
        deserializer: Deserializer[T] | None = None,
    ) -> None:
        self._key = key
        self.serializer = serializer
        self.deserializer = deserializer

    @property
    def has_key(self) -> bool:
        return self._key is not None

    @lazy_attribute
    def key(self) -> str:
        if self._key is None:
            raise EMPTY_KEY_ERROR

        return self._key

    def set_key(self, key: str) -> None:
        """Set key for the data manager.

        Allowed only if the key is not set yet.
        """
        if self._key is not None:
            raise KEY_ALREADY_SET_ERROR

        object.__setattr__(self, "_key", key)

    @overload
    async def get(
        self,
        default: Default[T] = NOT_PROVIDED,
        *,
        deserialize: bool = True,
    ) -> T:
        ...

    @overload
    async def get(
        self,
        default: None,
        *,
        deserialize: bool = True,
    ) -> T | None:
        ...

    async def get(
        self,
        default: Default[T] = NOT_PROVIDED,
        *,
        deserialize: bool = True,
    ) -> T | None:
        data = await self.fsm.get_data()
        return self.get_from_data(data, default, deserialize=deserialize)

    @overload
    def get_from_data(
        self,
        data: dict[str, Any],
        default: Default[T] = NOT_PROVIDED,
        *,
        deserialize: bool = True,
    ) -> T:
        ...

    @overload
    def get_from_data(
        self,
        data: dict[str, Any],
        default: None,
        *,
        deserialize: bool = True,
    ) -> T | None:
        ...

    def get_from_data(
        self,
        data: dict[str, Any],
        default: Default[T] | None = NOT_PROVIDED,
        *,
        deserialize: bool = True,
    ) -> T | None:
        value = data.get(self.key)
        if value is not None:
            if self.deserializer is not None and deserialize:
                return self.deserializer(value)

            return value

        if default is NOT_PROVIDED:
            msg = f"Key `{self.key}` does not exist in current FSMContext"
            raise KeyDoesNotExistError(msg)

        return default  # type: ignore[return-value]

    async def set(self, value: T) -> None:
        if self.serializer is not None:
            await self.fsm.update_data({self.key: self.serializer(value)})
        else:
            await self.fsm.update_data({self.key: value})

    async def delete(self) -> None:
        data = await self.fsm.get_data()
        data.pop(self.key, None)
        await self.fsm.set_data(data)


@dataclass(slots=True)
class ListDataManager(DataManager[list[T]]):
    def __init__(
        self,
        key: str | None = None,
        serializer: Serializer[list[T]] | None = None,
        deserializer: Deserializer[list[T]] | None = None,
    ) -> None:
        self._key = key
        self.serializer = serializer
        self.deserializer = deserializer

    async def append(self, value: T) -> None:
        async with Lock():
            sequence = await self.get(default=[])
            sequence.append(value)
            await self.set(sequence)
