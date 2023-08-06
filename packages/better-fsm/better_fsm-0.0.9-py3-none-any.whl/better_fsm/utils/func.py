from __future__ import annotations

from asyncio import iscoroutinefunction
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, ParamSpec, TypeVar, cast

T = TypeVar("T")
P = ParamSpec("P")
F = TypeVar("F", bound=Callable[..., Any])


def is_coroutine_function(obj: Any) -> bool:
    if iscoroutinefunction(obj):
        return True
    if callable(obj) and iscoroutinefunction(obj.__call__):
        return True

    return False


async def call(
    func: Callable[P, T | Awaitable[T]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    """Call a function and return its result.

    If the function is a coroutine function, it will be awaited.
    """
    if is_coroutine_function(func):
        return await func(*args, **kwargs)  # type: ignore[return-value]

    return func(*args, **kwargs)  # type: ignore[return-value]


def make_async(
    func: Callable[P, T | Awaitable[T]],
) -> Callable[P, Awaitable[T]]:
    """Make a function async.

    If the function is already async, it will be returned as is.
    """
    if is_coroutine_function(func):
        return cast(Callable[P, Awaitable[T]], func)

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        return func(*args, **kwargs)  # type: ignore[return-value]

    return cast(Callable[P, Awaitable[T]], wrapper)
