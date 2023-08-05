from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any, Generic, TypeVar, cast

from beartype import beartype
from memory_profiler import memory_usage
from typing_extensions import ParamSpec

_P = ParamSpec("_P")
_T = TypeVar("_T")


@beartype
@dataclass(frozen=True)
class Output(Generic[_T]):
    """A function output, and its memory usage."""

    value: _T
    memory: float


@beartype
def memory_profiled(func: Callable[_P, _T], /) -> Callable[_P, Output[_T]]:
    """Call a function, but also profile its maximum memory usage."""

    @wraps(func)
    def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> Output[_T]:
        memory, value = memory_usage(
            cast(Any, (func, args, kwargs)), max_usage=True, retval=True
        )
        return Output(value=value, memory=memory)

    return wrapped
