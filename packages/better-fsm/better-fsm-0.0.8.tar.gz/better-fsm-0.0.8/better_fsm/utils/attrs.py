from __future__ import annotations

from inspect import signature
from typing import TYPE_CHECKING, Any, Generic, TypeVar, overload

if TYPE_CHECKING:
    from collections.abc import Callable

T = TypeVar("T", bound=Any)


class lazy_attribute(Generic[T]):  # noqa: N801
    """Decorator that will turn a method in a lazy attribute.

    The first
    time the attribute is accessed its value will be computed using
    the decorated method and then cached.

    Example::
        class MyClass:

            @lazy_attribute
            def my_attribute(self):
                print("Computing")
                return 0

        obj = MyClass()
        obj.my_attribute
        obj.my_attribute

    Output::
        Computing
        0
        0
    """

    def __init__(self, func: Callable[[Any], T]) -> None:
        self._func = func
        self.__name__ = func.__name__

        self._func_signature = signature(func)

    @overload
    def __get__(self, obj: None, _: type[Any]) -> lazy_attribute[T]:
        ...

    @overload
    def __get__(self, obj: Any, _: type[Any]) -> T:
        ...

    def __get__(self, obj: Any | None, _: type[Any]) -> T | lazy_attribute[T]:
        if obj is None:
            return self

        value = self._func(obj)

        # Overwrite the attribute with the computed value.
        obj.__dict__[self.__name__] = value

        return value

    def __call__(self, obj: Any) -> T:
        """Call when the attribute is accessed from the class.

        Do not recommend using this, because it will compute the value every time.
        """
        return self._func(obj)

    def __repr__(self) -> str:
        return f"<lazy_attribute {self.__name__}, {self._func_signature}>"
