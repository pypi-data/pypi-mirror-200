from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Optional, Union

if TYPE_CHECKING:
    try:
        from pydantic.typing import AbstractSetIntStr, DictStrAny, MappingIntStrAny
    except ImportError:
        from .types import Unresolved

        AbstractSetIntStr: Unresolved = Unresolved
        MappingIntStrAny: Unresolved = Unresolved
        DictStrAny: Unresolved = Unresolved


class ExcludesNone:
    """
    Mixin for declare models that excludes :class:`None`:

    >>> import typing
    >>> import pydantic
    >>> class MyModel(ExcludesNone, pydantic.BaseModel):
    ...     some_field: typing.Optional[int] = None
    >>> my_model_default = MyModel()
    >>> my_model = MyModel(some_field=1)
    >>> assert my_model.dict() == {"some_field": 1}
    >>> assert my_model_default.dict() == {}
    >>> assert my_model.dict() != my_model_default.dict()
    """

    def dict(
        self,
        *,
        include: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None,
        exclude: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> DictStrAny:
        exclude_none = True

        return super(ExcludesNone, self).dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

    def json(
        self,
        *,
        include: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None,
        exclude: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        encoder: Optional[Callable[[Any], Any]] = None,
        models_as_dict: bool = True,
        **dumps_kwargs: Any,
    ) -> str:
        exclude_none = True

        return super(ExcludesNone, self).json(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            encoder=encoder,
            models_as_dict=models_as_dict,
            **dumps_kwargs,
        )
