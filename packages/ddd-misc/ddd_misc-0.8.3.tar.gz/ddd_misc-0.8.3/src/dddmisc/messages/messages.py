import typing as t
import datetime as dt
from datetime import datetime
from uuid import uuid4, UUID

import pytz

from dddmisc.messages.core import BaseDDDMessage, DDDMessageMeta


class DDDMessage(BaseDDDMessage, metaclass=DDDMessageMeta):
    from . import fields
    __reference__ = fields.Uuid(nullable=True)
    __timestamp__ = fields.Datetime(nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._reference = uuid4()
        self._timestamp = dt.datetime.now(pytz.UTC)

    @property
    def __domain__(self) -> str:
        return self.__metadata__.domain

    def get_attr(self, item: str):
        if item == '__reference__':
            return self._reference
        elif item == '__timestamp__':
            return self._timestamp
        else:
            return super().get_attr(item)
        
    def _set_meta_attrs(self, reference, timestamp):
        if reference:
            self._reference = reference if isinstance(reference, UUID) else UUID(reference) 
        if timestamp:
            if isinstance(timestamp, datetime):
                self._timestamp = timestamp
            elif isinstance(timestamp, (float, int)):
                self._timestamp = datetime.fromtimestamp(timestamp, pytz.UTC)
            elif isinstance(timestamp, str):
                self._timestamp = datetime.fromisoformat(timestamp)
            if self._timestamp.tzinfo is None:
                self._timestamp = self._timestamp.replace(tzinfo=pytz.UTC)
            elif self._timestamp.tzinfo != pytz.UTC:
                self._timestamp = self._timestamp.astimezone(pytz.UTC)

    @classmethod
    def load(cls, data: dict, reference=None, timestamp=None):
        obj = super(DDDMessage, cls).load(data)
        obj._set_meta_attrs(reference, timestamp)  # noqa
        return obj
    
    @classmethod
    def loads(cls, data: t.Union[str, bytes], reference=None, timestamp=None):
        obj = super(DDDMessage, cls).loads(data)
        obj._set_meta_attrs(reference, timestamp)  # noqa
        return obj

    def __eq__(self, other):
        return type(other) == type(self) and self.__reference__ == other.__reference__
    
    def __hash__(self):
        return hash(f'{type(self).__name__}({self.__reference__})')


class DDDCommand(DDDMessage):
    pass


class DDDEvent(DDDMessage):
    
    pass
    

