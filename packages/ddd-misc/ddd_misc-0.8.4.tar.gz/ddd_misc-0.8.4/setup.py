# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dddmisc',
 'dddmisc.exceptions',
 'dddmisc.messagebus',
 'dddmisc.messages',
 'dddmisc.repository']

package_data = \
{'': ['*']}

install_requires = \
['pytz', 'tenacity>=8.0.1,<9.0.0', 'yarl>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'ddd-misc',
    'version': '0.8.4',
    'description': 'Python EDA & DDD utilites',
    'long_description': '# Domain-driven Design Misc\n\nПакет предоставляет базовые классы и утилиты для реализации проекта с событийно-ориентированной архитектурой\nс использованием набора принципов DDD.\n\n## Классы\n\n**Классы объектов**\n- `BaseAggregate` - базовый класс для создания агрегата домена\n- `DDDEvent` - базовый класс для реализации событий домена\n- `DDDCommand` - базовый класс для реализации команд домена\n- `DDDStructure` - базовый класс для создания структур данных при описании команд и событий\n\nАтрибуты классов `DDDEvent`, `DDDCommand` и `DDDSturcture` задаются с использованием `Field`-классов из пакета `dddmisc.fields`\n\n- `get_message_class` - метод получения класса события или команды по его идентификатору из общего регистра\n- `get_error_class` - метод получения класса исключения домена из общего регистра\n\n**Класс репозиторий**\n\nРепозиторий уровень абстракции отвечающий за сохранение и воссоздание состояния агрегата.\n\nВ пакете репозиторий представлен 2-мя абстрактными классами для синхронной и асинхронной реализации:\n- `AbstractSyncRepository` - абстрактный класс для реализации синхронного репозитория\n- `AbstractAsyncRepository` - абстрактный класс для реализации асинхронного репозитория\n\nа также в пакете реализованы 2 декоратора `dddmisc.decorators.getter` и `dddmisc.decorators.agetter` для\nдекорирования методов репозитория для получения агрегата из базы данных.\n\n**UnitOfWork**\n\nUnit of work уровень абстракции отвечающий за обеспечения консистентности при сохранении состояния агрегата.\nUnit of work является надстройкой над репозиторием.\n\nВ пакете UnitOfWork представлен 2-мя абстрактными классами для синхронной и асинхронной реализации:\n- `AbstractSyncUnitOfWork` - абстрактный класс для реализации синхронного UnitOfWork\n- `AbstractAsyncUnitOfWork` - абстрактный класс для реализации асинхронного UnitOfWork\n\n**MessageBus**\n\nВ целях абстрагирования и унификации процесса доставки событий и команд до их обработчиков используется \nвнутрення шина сообщений. Дополнительно внутренняя шина сообщений обеспечивает итеративный процесс доставки событий,\nпорожденных агрегатом в процессе исполнения обработчиков на предыдущей итерации.\n\nВ пакете внутрення шина сообщений представлена классами:\n- `AsyncMessageBus` - реализации шины сообщений для использования в асинхронном коде\n- `SyncMessageBus` - реализации шины сообщений для использования в синхронном коде\n\n## tools\n\n- `ThreadLoop` - класс реализующий запуск asyncio.EventLoop в отдельном потоке\n- `Future` - класс аналог `asyncio.Future` для работы в многопоточном режиме\n- `async_to_sync` - функция вызова асинхронной корутины из синхронного кода\n\n### ThreadLoop\n`ThreadLoop()`\n\n_Свойства:_\n- `loop` - EventLoop работающий внутри потока\n- `done` - Флаг завершен ли поток\n\n_Методы:_\n- `def start()` - запускает поток блокируя передачу управления до завершения запуска EventLoop\n- `def stop(timeout=None)` - останавливает работу потока блокируя перерачу управления до завершения процесса закрытия EventLoop\n  - `timeout` - время ожидания процесса остановки\n- `def call_thread_safe(coro: t.Callable[..., t.Awaitable], *args, **kwargs)`\n  - `coro` - асинхронная функция которая должна быть исполнена во вложенном потоке\n  - `*args, **kwargs` - параметры вызова корутины\n\n### Future\n`Future()`\n\n_Свойства_\n- `done` - Флаг завершения\n- `result` - Результат установленный в класс\n- `exception` - Исключение установленное к класс\n\n_Методы:_\n- `def set_result(value)` - метод установки результата в класс \n- `def set_exception(self, exception)` - метод установки исключения\n- `def wait(*, timeout=None, raise_exception=True)` - метод ожидания future\n  - `timeout` - время ожидания завершения Future\n  - `raise_exception` - поднимает исключение в случае если установлено значение в `True`\n\n### `async_to_sync`\n\n`def async_to_sync(loop: asyncio.AbstractEventLoop, coro: t.Callable[..., t.Awaitable], *args, **kwargs)`\n- `loop` - EventLoop в котором должна исполниться корутина\n- `coro` - корутина\n- `*args, **kwargs` - параметры вызова корутины\n\n\n## Changelog\n\n**0.8.4**\n- Fixed behaviour of dump nullable fields\n\n**0.8.3**\n- fix error with dump nullable `fields.Structure`\n\n**0.8.2**\n- added `regex` attribute to `String` field\n\n**0.8.1**\n- fix error with `pytz` version\n\n**0.8.0**\n- add package `ddd_misc.tools`\n\n**0.7.2**\n\n_change:_\n\n- convert `handler` method of `AsyncMessageBus` from async function to sync function return awaitable object\n- change equals method for `DDDMessage` objects\n\n**0.7.1**\n\n_bugfix:_\n- fix `pytz` dependency conflict\n\n\n**0.7.0**\n_changes:_\n- В классах `BaseDDDException`, `DDDEvent`, `DDDCommnd` изменен тип поля `__timestamp__` c `float` на `datetime`\n- Для классов `AbstractMessagebus` добавлены методы `subscribe`,`unsubscribe` и enum-атрибут `SignalTypes` для подписки и отписки на сигналы\n- Для классов `DDDEvent`, `DDDCommnd` расширена сигнатура методов `load` и `loads` не обязательными атрибутами `reference` и `timestamp`\n\n**0.6.5**\n\n_changes:_\n- `DDDMessage.__timestamp__` now is datetime value\n- Remove specified dump and load methods from DDDMessage\n- Remove fields `timestamp`, `domain` and `reference` from DDDException dump and load methods\n\n**0.6.4**\n\n_futures:_\n- Make `AbstractAsyncUnitOfWork`, `AbstractSyncUnitOfWork` as Generic classes\n- set `engine` as optional parameter for sync and async Messagebus\n- fix hinting for `register` method of sync and async Messagebus\n\n**0.6.1**\n\n_future:_\n- add `filter` method for `getter` and `agetter` decorators\n\n**0.6.0**\n\n_future:_\n- Remove external messagebus from package.\n- Remove DDDResponse from package. Now messagebus handle method return object returned from handler.\n- Refactoring messagebus for set specified uow, repository and engine for handler.\n- Add decorators for get methods of repository. Removed abstract method `_get_from_storage` from repository.\n\n\n**0.5.4**\n\n_future:_\n- Execute events from commit aggregate changes when handler failed after commit\n- Parallel exec handlers subscribed to once event in sync messagebus\n\n\n**0.5.3**\n\n_bugfix:_\n- Make parallel execute event handlers in messagebus\n- Change messagebus log format\n\n\n**0.5.2**\n\n_bugfix:_\n- Fix error with nullable and default field attributes\n\n\n\n\n',
    'author': 'Vladislav Vorobyov',
    'author_email': 'vladislav.vorobyov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
