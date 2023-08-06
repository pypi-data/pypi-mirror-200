from pydantic import BaseModel
from pydantic.generics import GenericModel

from .mixins import ExcludesNone


class TogramlModel(ExcludesNone, BaseModel):  # pragma: no cover
    """
    A base model that`s excludes :class:`None`
    """


class TogramlGenericModel(ExcludesNone, GenericModel):  # pragma: no cover
    """
    A base generic model that`s excludes :class:`None`
    """
