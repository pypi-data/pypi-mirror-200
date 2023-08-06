from dataclasses import dataclass
from typing import Any, Optional, Dict, Type, Generic, Union
from typing import TypeVar, Callable

from pointy.marker import Marker

T = TypeVar("T")
TClass = Type[T]
TFactory = Union[
    Callable[[], T],
    Callable[[Any], T]
]

registry: Dict[Type, TFactory] = {}


@dataclass
class Field(Generic[T]):
    owner: Type
    name: str
    type: TClass

    @property
    def value(self) -> T:
        return getattr(self.owner, self.name)

    @property
    def is_marker(self) -> bool:
        return isinstance(self.value, Marker)


class SingletonFactory(Generic[T]):
    _factory_function: TFactory
    _instance: Optional[T] = None

    def __init__(self, factory_function: TFactory):
        self._factory_function = factory_function

    def get(self, *args, **kwargs) -> T:
        if self._instance is not None:
            return self._instance

        self._instance = self._factory_function(*args, **kwargs)

        return self._instance
