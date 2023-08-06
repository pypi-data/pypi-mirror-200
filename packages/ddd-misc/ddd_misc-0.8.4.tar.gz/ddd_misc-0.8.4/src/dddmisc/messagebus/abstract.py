import abc
import logging
import typing as t
from collections import defaultdict
from enum import Enum
from inspect import isclass

from dddmisc import DDDCommand, DDDEvent, AbstractAsyncUnitOfWork, AbstractSyncUnitOfWork, \
    AbstractSyncRepository, AbstractAsyncRepository

__all__ = ['AbstractMessagebus', 'HandlerConfig']

from dddmisc.messages import DDDMessage

from dddmisc.repository.repository import AbstractRepository
from dddmisc.unit_of_work import AbstractUnitOfWork


class HandlerConfig:

    def __init__(self, message: t.Union[DDDEvent, DDDCommand],
                 handler,
                 unit_of_work: t.Union[t.Type[AbstractSyncUnitOfWork], t.Type[AbstractAsyncUnitOfWork]],
                 repository: t.Union[t.Type[AbstractSyncRepository], t.Type[AbstractAsyncRepository]],
                 engine):
        if not isclass(message):
            message = type(message)
        self._message_type = message
        self._handler = handler
        self._unit_of_work_class = unit_of_work
        self._repository_class = repository
        self._engine = engine

    @property
    def handler(self):
        return self._handler

    @property
    def message_type(self) -> t.Type[t.Union[DDDEvent, DDDCommand]]:
        return self._message_type

    def get_uow(self):
        return self._unit_of_work_class(self._engine, repository_class=self._repository_class)

    def __eq__(self, other):
        return (isinstance(other, HandlerConfig)
                and other.handler is self.handler
                and other.message_type is self.message_type)

    def __hash__(self):
        return hash((self.handler, self.message_type))


class SignalType(Enum):
    PRE_START = 'PRE_START'
    POST_START = 'POST_START'
    PRE_STOP = 'PRE_STOP'
    POST_STOP = 'POST_STOP'


class AbstractSignal(abc.ABC):

    def __init__(self):
        self._handlers = defaultdict(set)

    def register(self, signal: SignalType, handler: t.Callable):
        self._handlers[signal].add(handler)

    def revoke(self, signal: SignalType, handler: t.Callable):
        self._handlers[signal].discard(handler)

    @abc.abstractmethod
    def notify(self, sender, signal:SignalType, *args, **kwargs):
        ...


class AbstractMessagebus(abc.ABC):

    SignalTypes = SignalType
    _signals: AbstractSignal

    def __init__(self, uow_class=None, repository_class=None, engine=None, logger='ddd-misc', event_retrying: int = 5):
        self._default_uow_class = uow_class
        self._default_engine = engine
        self._default_repository_class = repository_class
        self._EVENT_HANDLERS: t.Dict[t.Type[DDDEvent], t.Set[HandlerConfig]] = defaultdict(set)
        self._COMMAND_HANDLERS: t.Dict[t.Type[DDDCommand], HandlerConfig] = {}
        self._logger = logger if isinstance(logger, logging.Logger) else logging.getLogger(logger)
        self._event_retrying = event_retrying

    def register(self, message, handler, *, unit_of_work=None, repository=None, engine=None):
        unit_of_work, repository, engine = self._get_uow_config(unit_of_work, repository, engine)

        config = HandlerConfig(message, handler, unit_of_work, repository, engine)
        if issubclass(config.message_type, DDDEvent):
            self._EVENT_HANDLERS[config.message_type].add(config)
        elif issubclass(config.message_type, DDDCommand):
            self._COMMAND_HANDLERS[config.message_type] = config
        else:
            raise TypeError(f'message can be subclass or instance of DDDEvent or DDDCommand, not {message!r}')

    def _get_uow_config(self, unit_of_work, repository, engine):
        repository = repository or self._default_repository_class
        unit_of_work = unit_of_work or self._default_uow_class
        engine = engine or self._default_engine
        if repository is None:
            raise ValueError('Required set repository class for handler')
        elif not issubclass(repository, (AbstractSyncRepository, AbstractAsyncRepository, AbstractRepository)):
            raise TypeError('Repository class can be subclass of AbstractSyncRepository or AbstractAsyncRepository')
        if unit_of_work is None:
            raise ValueError('Required set unit of work class for handler')
        elif not issubclass(unit_of_work, (AbstractSyncUnitOfWork, AbstractAsyncUnitOfWork, AbstractUnitOfWork)):
            raise TypeError('Unit of work class can be subclass of AbstractSyncUnitOfWork or AbstractAsyncUnitOfWork')

        unit_of_work.validate_engine(engine)

        return unit_of_work, repository, engine

    def get_handlers(self, message) -> t.Tuple[HandlerConfig, ...]:
        if not isclass(message):
            message = type(message)
        if issubclass(message, DDDEvent):
            return tuple(self._EVENT_HANDLERS.get(message, ()))
        elif issubclass(message, DDDCommand):
            result = self._COMMAND_HANDLERS.get(message, None)
            if result:
                return result,
        else:
            raise TypeError(f'message can be subclass or instance of DDDEvent or DDDCommand, not {message!r}')
        raise RuntimeError(f'Not found registered handler for {message!r}')

    @abc.abstractmethod
    def handle(self, message: DDDMessage):
        raise NotImplementedError

    def subscribe(self, signal: SignalType, handler):
        self._signals.register(signal, handler)

    def unsubscribe(self, signal: SignalType, handler):
        self._signals.revoke(signal, handler)
