from __future__ import annotations

import json
from typing import Any, Dict, Optional

import pydantic
import pytest

from tograml_pydantic_utils.mixins import ExcludesNone


class Model(ExcludesNone, pydantic.BaseModel):
    field1: int
    field2: Optional[int] = None


@pytest.mark.parametrize(
    "model,excepted",
    (
        [Model(field1=1), {"field1": 1}],
        [Model(field1=1, field2=2), {"field1": 1, "field2": 2}],
    ),
)
def test_excludes_none_with_dict(model: Model, excepted: Dict[str, Any]) -> None:
    assert model.dict() == excepted


@pytest.mark.parametrize(
    "model,excepted",
    (
        [Model(field1=1), json.dumps({"field1": 1})],
        [Model(field1=1, field2=2), json.dumps({"field1": 1, "field2": 2})],
    ),
)
def test_excludes_none_with_json(model: Model, excepted: str) -> None:
    assert model.json() == excepted
