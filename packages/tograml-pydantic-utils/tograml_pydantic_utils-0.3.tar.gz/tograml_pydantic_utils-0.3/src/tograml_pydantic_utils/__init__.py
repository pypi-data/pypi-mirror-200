try:
    from .pydantic import TogramlModel, TogramlGenericModel
except ImportError:
    from ._logger import logger

    logger.info(
        "Pydantic not installed, to use TogramlModel and TogramlGenericModel - make sure is pydantic installed: "
        "pip install pydantic or "
        "pip install tograml-pydantic-utils[pydantic]"
    )

    __pydantic_all__ = [

    ]

else:
    __pydantic_all__ = [
        "TogramlModel",
        "TogramlGenericModel",
    ]

from .mixins import ExcludesNone
from .update_forward_refs_helper import update_forward_refs_helper

__version__ = "0.3"
__all__ = (
    "ExcludesNone",
    "update_forward_refs_helper",
    *__pydantic_all__,
)
