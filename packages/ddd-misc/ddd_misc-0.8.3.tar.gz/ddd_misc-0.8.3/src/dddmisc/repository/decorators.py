import functools
import typing as t

from dddmisc import BaseAggregate
from dddmisc.repository.repository import AbstractRepository

# P = t.ParamSpec('P')
R = t.TypeVar('R')


class SyncGetterProtocol(t.Protocol):

    def __call__(self: AbstractRepository, *args, **kwargs) -> BaseAggregate: ...


class AsyncGetterProtocol(t.Protocol):

    async def __call__(self: AbstractRepository, *args, **kwargs) -> BaseAggregate: ...


class FilterProtocol(t.Protocol):

    def __call__(self: AbstractRepository, aggregate: BaseAggregate, *args, **kwargs) -> bool: ...


class BaseGetter:
    _func: t.Union[SyncGetterProtocol, AsyncGetterProtocol]
    _filter_func: FilterProtocol

    def __get__(self, obj, _type=None):
        return functools.partial(self, obj)  # noqa

    def _get_from_repository_seen(self, repo, *args, **kwargs):
        if self._filter_func is None:
            raise RuntimeError(f'Required add filter for {self._func.__name__}')
        aggregate = next((aggregate for aggregate in repo._seen
                          if self._filter_func(repo, aggregate, *args, **kwargs)), None)
        return aggregate

    @staticmethod
    def _add_to_repository_seen(repo, aggregate):
        repo._seen.add(aggregate)

    def filter(self, func: FilterProtocol):
        self._filter_func = func
        return func


class getter(BaseGetter):  # noqa
    def __init__(self, func: SyncGetterProtocol):
        self._func = func
        self._filter_func: t.Optional[FilterProtocol] = None

    def __call__(self, *args, **kwargs):
        aggregate = self._get_from_repository_seen(*args, **kwargs)
        if aggregate:
            return aggregate
        aggregate = self._func(*args, **kwargs)
        self._add_to_repository_seen(args[0], aggregate)
        aggregate = self._get_from_repository_seen(*args, **kwargs)
        return aggregate


class agetter(BaseGetter):  # noqa
    def __init__(self, func: AsyncGetterProtocol):
        self._func = func
        self._filter_func: t.Optional[FilterProtocol] = None

    async def __call__(self, *args, **kwargs):
        aggregate = self._get_from_repository_seen(*args, **kwargs)
        if aggregate:
            return aggregate
        aggregate = await self._func(*args, **kwargs)
        self._add_to_repository_seen(args[0], aggregate)
        aggregate = self._get_from_repository_seen(*args, **kwargs)
        return aggregate
