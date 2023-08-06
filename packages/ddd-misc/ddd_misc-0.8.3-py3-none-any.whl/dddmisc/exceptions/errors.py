import typing as t
from .core import DDDExceptionMeta, BaseDDDException, DDDException


def get_error_class(key: str) -> t.Type[BaseDDDException]:
    collection = DDDExceptionMeta.get_exceptions_collection()
    if key in collection:
        return collection[key]
    raise UnregisteredMessageClass(key=key)


class BaseServiceError(DDDException, metaclass=DDDExceptionMeta):
    class Meta:
        domain = '__ddd_service__'
        is_baseclass = True


class BaseDomainError(DDDException, metaclass=DDDExceptionMeta):
    pass


class BaseParseMessageError(BaseServiceError):
    class Meta:
        is_baseclass = True


class UnregisteredErrorClass(BaseParseMessageError):
    class Meta:
        template = '91'


class UnregisteredMessageClass(BaseParseMessageError):

    def __init__(self, *args, key, **kwargs):
        super(UnregisteredMessageClass, self).__init__(*args, key=key, **kwargs)

    class Meta:
        template = 'Message class by "{key}" not found'


class JsonDecodeError(BaseParseMessageError):
    pass


class ValidationError(BaseParseMessageError):
    class Meta:
        template = 'Error validate data'

    def dump(self) -> dict:
        result = super(ValidationError, self).dump()
        result['data'] = {key: {'type': value.__class__.__name__, 'value': str(value)}
                          for key, value in result['data'].items()}
        return result


class InternalServiceError(BaseServiceError):
    class Meta:
        template = '01'

# TODO дописать классы исключений
