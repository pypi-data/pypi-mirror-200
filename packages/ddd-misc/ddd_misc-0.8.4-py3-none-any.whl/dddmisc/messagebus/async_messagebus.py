import asyncio
import typing as t
from contextlib import suppress

from tenacity import AsyncRetrying, stop_after_attempt, wait_exponential, RetryError

from dddmisc import AbstractAsyncUnitOfWork, AbstractAsyncRepository, DDDEvent, DDDCommand
from dddmisc.messagebus.abstract import AbstractMessagebus, HandlerConfig, AbstractSignal, SignalType

EventType = t.TypeVar('EventType', bound=DDDEvent)
CommandType = t.TypeVar('CommandType', bound=DDDCommand)
UoWType = t.TypeVar('UoWType', bound=AbstractAsyncUnitOfWork)


class EventHandlerProtocol(t.Protocol):

    async def __call__(self, event: EventType, uow: UoWType) -> t.NoReturn: ...


class CommandHandlerProtocol(t.Protocol):

    async def __call__(self, command: CommandType, uow: UoWType) -> t.Any: ...


class AsyncSignal(AbstractSignal):

    async def notify(self, sender, signal: SignalType, *args, **kwargs):
        for handler in self._handlers[signal]:
            with suppress(BaseException):
                await handler(sender, signal, *args, **kwargs)


class AsyncMessageBus(AbstractMessagebus):
    _loop: asyncio.AbstractEventLoop

    def __init__(self,
                 uow_class: t.Optional[t.Type[AbstractAsyncUnitOfWork]] = None,
                 repository_class: t.Optional[t.Type[AbstractAsyncRepository]] = None,
                 engine=None, logger='ddd-misc', event_retrying: int = 5):
        super(AsyncMessageBus, self).__init__(uow_class, repository_class, engine, logger, event_retrying)
        self._tasks: t.Set[asyncio.Task] = set()
        self._is_run = False
        self._daemon_task: t.Optional[asyncio.Task] = None
        self._start_event: t.Optional[asyncio.Event] = None
        self._signals = AsyncSignal()

    def set_loop(self, loop: asyncio.AbstractEventLoop):
        self._loop = loop

    @property
    def loop(self):
        return self._loop

    async def start(self):
        await self._signals.notify(self, self.SignalTypes.PRE_START)
        self._start_event = asyncio.Event()
        self._daemon_task = self.loop.create_task(self._run_daemon())
        await self._start_event.wait()
        await self._signals.notify(self, self.SignalTypes.POST_START)

    async def stop(self, exception: Exception = None):
        await self._signals.notify(self, self.SignalTypes.PRE_STOP, exception)
        self._start_event.clear()
        if self._daemon_task and not self._daemon_task.done():
            await self._daemon_task
        while self._tasks:
            tasks = tuple(self._tasks)
            await asyncio.gather(*tasks, return_exceptions=True)
            self._tasks.difference_update(tasks)
        await self._signals.notify(self, self.SignalTypes.POST_STOP, exception)

    async def _run_daemon(self):
        self._start_event.set()
        while self._start_event.is_set():
            if self._tasks:
                done, pending = await asyncio.wait(self._tasks, timeout=0.001)
                self._tasks.difference_update(done)
            else:
                await asyncio.sleep(0.001)

    @t.overload
    def register(self,
                 message: t.Type[DDDEvent],
                 handler: EventHandlerProtocol,
                 *,
                 unit_of_work: t.Optional[t.Type[AbstractAsyncUnitOfWork]] = None,
                 repository: t.Optional[t.Type[AbstractAsyncRepository]] = None,
                 engine=None):
        ...

    @t.overload
    def register(self,
                 message: t.Type[DDDCommand],
                 handler: CommandHandlerProtocol,
                 *,
                 unit_of_work: t.Optional[t.Type[AbstractAsyncUnitOfWork]] = None,
                 repository: t.Optional[t.Type[AbstractAsyncRepository]] = None,
                 engine=None):
        ...

    def register(self, message,
                 handler, *,
                 unit_of_work=None,
                 repository=None,
                 engine=None):
        super(AsyncMessageBus, self).register(message, handler,
                                              unit_of_work=unit_of_work, repository=repository, engine=engine)

    @t.overload
    def handle(self, message: DDDEvent):
        ...

    @t.overload
    def handle(self, message: DDDCommand) -> t.Awaitable[t.Any]:
        ...

    def handle(self, message):
        if isinstance(message, DDDCommand):
            return self._handle_command(message)
        elif isinstance(message, DDDEvent):
            return self._handle_event(message)
        else:
            self._logger.error('Handle not valid message type %s in messagebus %s', message, self)
            raise TypeError(f'{message} was not and DDDEvent ot DDDCommand')

    async def _handle_command(self, command: DDDCommand):
        config = self.get_handlers(command)[0]
        uow = config.get_uow()
        try:
            response = await config.handler(command, uow)
            return response
        except:
            self._logger.exception('Failure publish command', extra={
                'command': repr(command),
                'handler': repr(config.handler),
            })
            raise
        finally:
            for event in uow.collect_events():
                await self._handle_event(event)

    async def _handle_event(self, event: DDDEvent):
        for handler in self.get_handlers(event):
            task = self.loop.create_task(self._execute_handler_event(handler, event))
            self._tasks.add(task)
            await asyncio.sleep(0)

    async def _execute_handler_event(self, config: HandlerConfig, event: DDDEvent):
        uow = config.get_uow()
        try:
            async for attempt in AsyncRetrying(stop=stop_after_attempt(self._event_retrying),
                                               wait=wait_exponential(min=1, max=15)):
                with attempt:
                    await config.handler(event, uow)

        except RetryError as retry_failure:
            self._logger.exception(
                'Failure publish event', extra={
                    'event': repr(event),
                    'handler': repr(config.handler),
                    'attempt_count': retry_failure.last_attempt.attempt_number,
                })
        finally:
            for ev in uow.collect_events():
                await self._handle_event(ev)
