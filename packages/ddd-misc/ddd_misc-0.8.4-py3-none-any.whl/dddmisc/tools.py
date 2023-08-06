import asyncio
import threading
import typing as t


__all__ = ['ThreadLoop', 'Future', 'async_to_sync']


class ThreadLoop(threading.Thread):
    def __init__(self):
        self._loop: t.Optional[asyncio.AbstractEventLoop] = None
        self._stop_event: t.Optional[asyncio.Event] = None
        self._start_lock = threading.Lock()
        self._stop_lock = threading.Lock()
        self._start_lock.acquire(blocking=False)
        self._stop_lock.acquire(blocking=False)
        super(ThreadLoop, self).__init__()

    @property
    def loop(self):
        return self._loop

    @property
    def done(self):
        return not self.is_alive()

    def run(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._stop_event = asyncio.Event()
        self._loop.call_soon(self._start_lock.release)
        self._loop.run_until_complete(self._stop_event.wait())
        self._stop_lock.release()

    def start(self) -> None:
        super(ThreadLoop, self).start()
        self._start_lock.acquire(blocking=True)

    def stop(self, timeout=None):
        if self._loop:
            self._loop.call_soon_threadsafe(self._stop_event.set)
            self._stop_lock.acquire(blocking=True)
            self._loop.close()
            self.join(timeout)

    def call_thread_safe(self, coro: t.Callable[..., t.Awaitable], *args, **kwargs):
        return async_to_sync(self._loop, coro, *args, **kwargs)


class Future:

    def __init__(self):
        self._lock = threading.Lock()
        self._lock.acquire(blocking=False)
        self._result = None
        self._exception = None
        self._done = False

    @property
    def done(self):
        return self._done

    @property
    def result(self) -> t.Any:
        return self._result

    @property
    def exception(self) -> Exception:
        return self._exception

    def wait(self, *, timeout=-1, raise_exception=True):
        self._lock.acquire(blocking=True, timeout=timeout)
        try:
            if self._exception is not None:
                if raise_exception:
                    raise self._exception
                return self._exception
            else:
                return self._result
        finally:
            self._lock.release()

    def set_result(self, value):
        self._result = value
        self._lock.release()
        self._done = True

    def set_exception(self, exception):
        self._exception = exception
        self._lock.release()
        self._done = True


def async_to_sync(loop: asyncio.AbstractEventLoop, coro: t.Callable[..., t.Awaitable], *args, **kwargs):
    async def wrapper(fut: Future):
        try:
            result = await coro(*args, **kwargs)
            fut.set_result(result)
        except Exception as err:
            fut.set_exception(err)

    future = Future()
    loop.call_soon_threadsafe(loop.create_task, wrapper(future))
    return future.wait()

