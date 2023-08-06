from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, Optional, Union


if TYPE_CHECKING:
    try:
        from pydantic import BaseModel
    except ImportError:
        from .types import Unresolved

        BaseModel: Unresolved = Unresolved


UPDATE_FORWARD_REFS = "update_forward_refs"


def update_forward_refs_helper(
    __all__: Iterable[str], __models__: Dict[str, Union[Any, BaseModel]]
) -> None:
    """
    Update forward references for given pydantic models.

    :param __all__: model names for updating
    :param __models__: all models
    :return: :class:`None`
    """

    for __entity_name__ in __all__:
        __entity__ = __models__.get(
            __entity_name__, None
        )  # type: Optional[Union[Any, BaseModel]]
        if not hasattr(__entity__, UPDATE_FORWARD_REFS):  # pragma: no cover
            continue
        __update_forwards_refs__: Callable[..., Any] = getattr(__entity__, UPDATE_FORWARD_REFS)
        __update_forwards_refs__(
            **{k: v for k, v in __models__.items() if k in __all__},
            **{"Optional": Optional},
        )
