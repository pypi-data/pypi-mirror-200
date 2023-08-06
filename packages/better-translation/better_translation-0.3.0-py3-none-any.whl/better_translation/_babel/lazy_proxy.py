from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator


class LazyProxy:
    """Class for proxy objects that delegate to a specified function to evaluate the actual object.

    >>> def greeting(name='world'):
    ...     return 'Hello, %s!' % name
    >>> lazy_greeting = LazyProxy(greeting, name='Joe')
    >>> print(lazy_greeting)
    Hello, Joe!
    >>> u'  ' + lazy_greeting
    u'  Hello, Joe!'
    >>> u'(%s)' % lazy_greeting
    u'(Hello, Joe!)'
    This can be used, for example, to implement lazy translation functions that
    delay the actual translation until the string is actually used. The
    rationale for such behavior is that the locale of the user may not always
    be available. In web applications, you only know the locale when processing
    a request.
    The proxy implementation attempts to be as complete as possible, so that
    the lazy objects should mostly work as expected, for example for sorting:
    >>> greetings = [
    ...     LazyProxy(greeting, 'world'),
    ...     LazyProxy(greeting, 'Joe'),
    ...     LazyProxy(greeting, 'universe'),
    ... ]
    >>> greetings.sort()
    >>> for greeting in greetings:
    ...     print(greeting)
    Hello, Joe!
    Hello, universe!
    Hello, world!.
    """

    __slots__ = [
        "_func",
        "_args",
        "_kwargs",
        "_value",
        "_is_cache_enabled",
        "_attribute_error",
    ]

    if TYPE_CHECKING:
        _func: Callable[..., Any]
        _args: tuple[Any, ...]
        _kwargs: dict[str, Any]
        _is_cache_enabled: bool
        _value: Any
        _attribute_error: AttributeError | None

    def __init__(
        self,
        func: Callable[..., Any],
        *args: Any,
        enable_cache: bool = True,
        **kwargs: Any,
    ) -> None:
        # Avoid triggering our own __setattr__ implementation
        object.__setattr__(self, "_func", func)
        object.__setattr__(self, "_args", args)
        object.__setattr__(self, "_kwargs", kwargs)
        object.__setattr__(self, "_is_cache_enabled", enable_cache)
        object.__setattr__(self, "_value", None)
        object.__setattr__(self, "_attribute_error", None)

    @property
    def value(self) -> Any:
        if self._value is None:
            try:
                value = self._func(*self._args, **self._kwargs)
            except AttributeError as error:
                object.__setattr__(self, "_attribute_error", error)
                raise

            if not self._is_cache_enabled:
                return value
            object.__setattr__(self, "_value", value)
        return self._value

    def __contains__(self, key: object) -> bool:
        return key in self.value

    def __bool__(self) -> bool:
        return bool(self.value)

    def __dir__(self) -> list[str]:
        return dir(self.value)

    def __iter__(self) -> Iterator[Any]:
        return iter(self.value)

    def __len__(self) -> int:
        return len(self.value)

    def __str__(self) -> str:
        return str(self.value)

    def __add__(self, other: object) -> Any:
        return self.value + other

    def __radd__(self, other: object) -> Any:
        return other + self.value

    def __mod__(self, other: object) -> Any:
        return self.value % other

    def __rmod__(self, other: object) -> Any:
        return other % self.value

    def __mul__(self, other: object) -> Any:
        return self.value * other

    def __rmul__(self, other: object) -> Any:
        return other * self.value

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.value(*args, **kwargs)

    def __lt__(self, other: object) -> bool:
        return self.value < other

    def __le__(self, other: object) -> bool:
        return self.value <= other

    def __eq__(self, other: object) -> bool:
        return self.value == other

    def __ne__(self, other: object) -> bool:
        return self.value != other

    def __gt__(self, other: object) -> bool:
        return self.value > other

    def __ge__(self, other: object) -> bool:
        return self.value >= other

    def __delattr__(self, name: str) -> None:
        delattr(self.value, name)

    def __getattr__(self, name: str) -> Any:
        if self._attribute_error is not None:
            raise self._attribute_error
        return getattr(self.value, name)

    def __setattr__(self, name: str, value: Any) -> None:
        setattr(self.value, name, value)

    def __delitem__(self, key: Any) -> None:
        del self.value[key]

    def __getitem__(self, key: Any) -> Any:
        return self.value[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        self.value[key] = value

    def __copy__(self) -> LazyProxy:
        return LazyProxy(
            self._func,
            enable_cache=self._is_cache_enabled,  # noqa: RUF004
            *self._args,  # noqa: B026
            **self._kwargs,
        )

    def __deepcopy__(self, memo: Any) -> LazyProxy:
        from copy import deepcopy

        return LazyProxy(
            deepcopy(self._func, memo),
            enable_cache=deepcopy(self._is_cache_enabled, memo),  # noqa: RUF004
            *deepcopy(self._args, memo),  # noqa: B026
            **deepcopy(self._kwargs, memo),
        )
