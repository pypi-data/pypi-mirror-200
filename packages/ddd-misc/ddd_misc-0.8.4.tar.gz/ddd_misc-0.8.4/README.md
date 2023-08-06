# Domain-driven Design Misc

Пакет предоставляет базовые классы и утилиты для реализации проекта с событийно-ориентированной архитектурой
с использованием набора принципов DDD.

## Классы

**Классы объектов**
- `BaseAggregate` - базовый класс для создания агрегата домена
- `DDDEvent` - базовый класс для реализации событий домена
- `DDDCommand` - базовый класс для реализации команд домена
- `DDDStructure` - базовый класс для создания структур данных при описании команд и событий

Атрибуты классов `DDDEvent`, `DDDCommand` и `DDDSturcture` задаются с использованием `Field`-классов из пакета `dddmisc.fields`

- `get_message_class` - метод получения класса события или команды по его идентификатору из общего регистра
- `get_error_class` - метод получения класса исключения домена из общего регистра

**Класс репозиторий**

Репозиторий уровень абстракции отвечающий за сохранение и воссоздание состояния агрегата.

В пакете репозиторий представлен 2-мя абстрактными классами для синхронной и асинхронной реализации:
- `AbstractSyncRepository` - абстрактный класс для реализации синхронного репозитория
- `AbstractAsyncRepository` - абстрактный класс для реализации асинхронного репозитория

а также в пакете реализованы 2 декоратора `dddmisc.decorators.getter` и `dddmisc.decorators.agetter` для
декорирования методов репозитория для получения агрегата из базы данных.

**UnitOfWork**

Unit of work уровень абстракции отвечающий за обеспечения консистентности при сохранении состояния агрегата.
Unit of work является надстройкой над репозиторием.

В пакете UnitOfWork представлен 2-мя абстрактными классами для синхронной и асинхронной реализации:
- `AbstractSyncUnitOfWork` - абстрактный класс для реализации синхронного UnitOfWork
- `AbstractAsyncUnitOfWork` - абстрактный класс для реализации асинхронного UnitOfWork

**MessageBus**

В целях абстрагирования и унификации процесса доставки событий и команд до их обработчиков используется 
внутрення шина сообщений. Дополнительно внутренняя шина сообщений обеспечивает итеративный процесс доставки событий,
порожденных агрегатом в процессе исполнения обработчиков на предыдущей итерации.

В пакете внутрення шина сообщений представлена классами:
- `AsyncMessageBus` - реализации шины сообщений для использования в асинхронном коде
- `SyncMessageBus` - реализации шины сообщений для использования в синхронном коде

## tools

- `ThreadLoop` - класс реализующий запуск asyncio.EventLoop в отдельном потоке
- `Future` - класс аналог `asyncio.Future` для работы в многопоточном режиме
- `async_to_sync` - функция вызова асинхронной корутины из синхронного кода

### ThreadLoop
`ThreadLoop()`

_Свойства:_
- `loop` - EventLoop работающий внутри потока
- `done` - Флаг завершен ли поток

_Методы:_
- `def start()` - запускает поток блокируя передачу управления до завершения запуска EventLoop
- `def stop(timeout=None)` - останавливает работу потока блокируя перерачу управления до завершения процесса закрытия EventLoop
  - `timeout` - время ожидания процесса остановки
- `def call_thread_safe(coro: t.Callable[..., t.Awaitable], *args, **kwargs)`
  - `coro` - асинхронная функция которая должна быть исполнена во вложенном потоке
  - `*args, **kwargs` - параметры вызова корутины

### Future
`Future()`

_Свойства_
- `done` - Флаг завершения
- `result` - Результат установленный в класс
- `exception` - Исключение установленное к класс

_Методы:_
- `def set_result(value)` - метод установки результата в класс 
- `def set_exception(self, exception)` - метод установки исключения
- `def wait(*, timeout=None, raise_exception=True)` - метод ожидания future
  - `timeout` - время ожидания завершения Future
  - `raise_exception` - поднимает исключение в случае если установлено значение в `True`

### `async_to_sync`

`def async_to_sync(loop: asyncio.AbstractEventLoop, coro: t.Callable[..., t.Awaitable], *args, **kwargs)`
- `loop` - EventLoop в котором должна исполниться корутина
- `coro` - корутина
- `*args, **kwargs` - параметры вызова корутины


## Changelog

**0.8.4**
- Fixed behaviour of dump nullable fields

**0.8.3**
- fix error with dump nullable `fields.Structure`

**0.8.2**
- added `regex` attribute to `String` field

**0.8.1**
- fix error with `pytz` version

**0.8.0**
- add package `ddd_misc.tools`

**0.7.2**

_change:_

- convert `handler` method of `AsyncMessageBus` from async function to sync function return awaitable object
- change equals method for `DDDMessage` objects

**0.7.1**

_bugfix:_
- fix `pytz` dependency conflict


**0.7.0**
_changes:_
- В классах `BaseDDDException`, `DDDEvent`, `DDDCommnd` изменен тип поля `__timestamp__` c `float` на `datetime`
- Для классов `AbstractMessagebus` добавлены методы `subscribe`,`unsubscribe` и enum-атрибут `SignalTypes` для подписки и отписки на сигналы
- Для классов `DDDEvent`, `DDDCommnd` расширена сигнатура методов `load` и `loads` не обязательными атрибутами `reference` и `timestamp`

**0.6.5**

_changes:_
- `DDDMessage.__timestamp__` now is datetime value
- Remove specified dump and load methods from DDDMessage
- Remove fields `timestamp`, `domain` and `reference` from DDDException dump and load methods

**0.6.4**

_futures:_
- Make `AbstractAsyncUnitOfWork`, `AbstractSyncUnitOfWork` as Generic classes
- set `engine` as optional parameter for sync and async Messagebus
- fix hinting for `register` method of sync and async Messagebus

**0.6.1**

_future:_
- add `filter` method for `getter` and `agetter` decorators

**0.6.0**

_future:_
- Remove external messagebus from package.
- Remove DDDResponse from package. Now messagebus handle method return object returned from handler.
- Refactoring messagebus for set specified uow, repository and engine for handler.
- Add decorators for get methods of repository. Removed abstract method `_get_from_storage` from repository.


**0.5.4**

_future:_
- Execute events from commit aggregate changes when handler failed after commit
- Parallel exec handlers subscribed to once event in sync messagebus


**0.5.3**

_bugfix:_
- Make parallel execute event handlers in messagebus
- Change messagebus log format


**0.5.2**

_bugfix:_
- Fix error with nullable and default field attributes




