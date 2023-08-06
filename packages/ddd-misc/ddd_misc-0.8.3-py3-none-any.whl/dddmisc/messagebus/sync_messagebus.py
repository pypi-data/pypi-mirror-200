import logging
import threading
import typing as t
from contextlib import suppress
from queue import Queue, Empty

from tenacity import Retrying, stop_after_attempt, wait_exponential, RetryError

from dddmisc import DDDEvent, AbstractSyncUnitOfWork, AbstractSyncRepository, DDDCommand
from dddmisc.messagebus.abstract import AbstractMessagebus, HandlerConfig, AbstractSignal, SignalType

EventType = t.TypeVar('EventType', bound=DDDEvent)
CommandType = t.TypeVar('CommandType', bound=DDDCommand)
UoWType = t.TypeVar('UoWType', bound=AbstractSyncUnitOfWork)


class EventHandlerProtocol(t.Protocol):

    def __call__(self, event: EventType, uow: UoWType) -> t.NoReturn: ...


class CommandHandlerProtocol(t.Protocol):

    def __call__(self, command: CommandType, uow: UoWType) -> t.Any: ...


class EventThreadExecutor(threading.Thread):
    def __init__(self, event: DDDEvent, handler, executor, finish_callback: t.Callable):
        self.event = event
        self.executor = executor
        self.handler = handler
        self.callback = finish_callback
        super(EventThreadExecutor, self).__init__()

    def run(self) -> None:
        try:
            self.executor(self.event, self.handler)
        finally:
            self.callback()


class EventQueueObserve(threading.Thread):

    def __init__(self, events_queue: Queue, executor: t.Callable[[DDDEvent], None], logger: logging.Logger):
        self.events_queue = events_queue
        self.executor = executor
        self._run_flag = False
        self.logger = logger
        self.tasks = []
        super(EventQueueObserve, self).__init__(daemon=True)

    def run(self) -> None:
        is_empty = False
        self._run_flag = True
        while self._run_flag or not is_empty:
            try:
                event, handler = self.events_queue.get(block=True, timeout=0.0001)
                is_empty = False
                task = EventThreadExecutor(event, handler, self.executor, self.events_queue.task_done)
                self.tasks.append(task)
                task.start()
            except Empty:
                is_empty = True
                continue

    def stop(self, exception=None):
        self._run_flag = False
        self.events_queue.join()


class SyncSignal(AbstractSignal):

    def notify(self, sender, signal: SignalType, *args, **kwargs):
        for handler in self._handlers[signal]:
            with suppress(BaseException):
                handler(sender, signal, *args, **kwargs)


class MessageBus(AbstractMessagebus):

    def __init__(self,
                 uow_class: t.Optional[t.Type[AbstractSyncUnitOfWork]] = None,
                 repository_class: t.Optional[t.Type[AbstractSyncRepository]] = None,
                 engine=None, logger='ddd-misc', event_retrying: int = 5):
        super(MessageBus, self).__init__(uow_class, repository_class, engine, logger, event_retrying)
        self._signals = SyncSignal()
        self._events_queue = Queue()
        self._event_executor = EventQueueObserve(self._events_queue, self._exec_event, self._logger)

    def start(self):
        self._signals.notify(self, self.SignalTypes.PRE_START)
        self._event_executor.start()
        self._signals.notify(self, self.SignalTypes.POST_START)

    def stop(self, exception: Exception = None):
        self._signals.notify(self, self.SignalTypes.PRE_STOP, exception)
        self._event_executor.stop(exception)
        self._signals.notify(self, self.SignalTypes.POST_STOP, exception)

    @t.overload
    def register(self,
                 message: t.Type[DDDEvent],
                 handler: EventHandlerProtocol,
                 *,
                 unit_of_work: t.Optional[t.Type[AbstractSyncUnitOfWork]] = None,
                 repository: t.Optional[t.Type[AbstractSyncRepository]] = None,
                 engine=None):
        ...

    @t.overload
    def register(self,
                 message: t.Type[DDDCommand],
                 handler: CommandHandlerProtocol,
                 *,
                 unit_of_work: t.Optional[t.Type[AbstractSyncUnitOfWork]] = None,
                 repository: t.Optional[t.Type[AbstractSyncRepository]] = None,
                 engine=None):
        ...

    def register(self, message,
                 handler, *,
                 unit_of_work=None,
                 repository=None,
                 engine=None):
        super(MessageBus, self).register(message, handler,
                                         unit_of_work=unit_of_work, repository=repository, engine=engine)

    @t.overload
    def handle(self, message: DDDEvent) -> t.NoReturn:
        ...

    @t.overload
    def handle(self, message: DDDCommand) -> t.Any:
        ...

    def handle(self, message):
        if isinstance(message, DDDCommand):
            return self._handle_command(message)
        elif isinstance(message, DDDEvent):
            self._handle_event(message)
        else:
            self._logger.error('Handle not valid message type %s in messagebus %s', message, self)
            raise TypeError(f'{message} was not DDDEvent or DDDCommand')

    def _handle_command(self, command: DDDCommand) -> t.Any:
        config = self.get_handlers(command)[0]
        uow = config.get_uow()
        try:
            response = config.handler(command, uow)
            return response
        except Exception:
            self._logger.exception('Failure publish command', extra={
                'command': repr(command),
                'handler': repr(config.handler),
            })
            raise
        finally:
            for event in uow.collect_events():
                self._handle_event(event)

    def _handle_event(self, event: DDDEvent):
        for config in self.get_handlers(event):
            self._events_queue.put((event, config))

    def _exec_event(self, event: DDDEvent, config: HandlerConfig):
        uow = config.get_uow()
        try:
            for attempt in Retrying(stop=stop_after_attempt(self._event_retrying),
                                    wait=wait_exponential(min=1, max=15)):
                with attempt:
                    config.handler(event, uow)
        except RetryError as retry_failure:
            self._logger.exception(
                'Failure publish event', extra={
                    'event': repr(event),
                    'handler': repr(config.handler),
                    'attempt_count': retry_failure.last_attempt.attempt_number,
                })
        finally:
            for ev in uow.collect_events():
                self._handle_event(ev)
