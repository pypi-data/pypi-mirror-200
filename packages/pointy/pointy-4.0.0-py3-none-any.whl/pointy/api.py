import inspect
from typing import Optional, get_type_hints, List, Callable, Union

import pointy.core as _core
from pointy.marker import Marker

Marker = Marker

ProvideDecorator = Union[
    Callable[[], Optional[_core.TClass]],
    Callable[[Optional[_core.TClass]], Optional[_core.TClass]]
]


def provide(
        the_type: Optional[_core.TClass] = None,
        factory: Optional[_core.TFactory] = None,
        singleton: Optional[bool] = False
) -> ProvideDecorator:
    def decorator(the_providing_type: Optional[_core.TClass] = None) -> Optional[_core.TClass]:
        registry_type = the_type or the_providing_type
        final_factory = factory or the_providing_type or the_type

        if singleton:
            final_factory = _core.SingletonFactory(final_factory).get

        _core.registry[registry_type] = final_factory

        return the_providing_type

    return decorator


def construct(the_type: _core.TClass, *args, **kwargs) -> _core.T:
    factory = _core.registry.get(the_type, None)
    if not callable(factory):
        raise RuntimeError(f"Invalid factory: {factory}")

    return factory(*args, **kwargs)


def _inject_class(target: _core.TClass) -> _core.TClass:
    og_new = getattr(target, "__new__")
    fields: List[_core.Field[Marker]] = list(
        filter(
            lambda f: f.is_marker,
            map(
                lambda t: _core.Field(target, *t),
                get_type_hints(target).items()
            )
        )
    )

    def injecting_new(cls, *args, **kwargs):
        instance = og_new(cls)

        instance_init = getattr(instance, "__init__", None)
        if callable(instance_init):
            instance_init(*args, **kwargs)

        for field in fields:
            marker = field.value
            if not isinstance(marker, Marker):
                raise RuntimeError(f"Not a marker: {marker} ({target})")

            setattr(instance, field.name, construct(field.type, *marker.args, **marker.kwargs))

        return instance

    setattr(target, "__new__", injecting_new)

    return target


def _inject_function(target: _core.TClass) -> _core.TClass:
    hints = get_type_hints(target)
    signature = inspect.signature(target)

    def wrapper(*args, **kwargs):
        for key, param in signature.parameters.items():
            if isinstance(param.default, Marker):
                marker = param.default

                kwargs[key] = construct(hints[key], *marker.args, **marker.kwargs)

        return target(*args, **kwargs)

    return wrapper


def inject(target: _core.TClass) -> _core.TClass:
    if inspect.isclass(target):
        return _inject_class(target)

    elif inspect.isfunction(target):
        return _inject_function(target)

    elif inspect.ismethod(target):
        return _inject_function(target)

    else:
        raise RuntimeError(f"Cannot inject on unsupported type {type(target)}")
