from __future__ import annotations

from typing import List

import pydantic
import pytest


class Container(pydantic.BaseModel):
    contains: List[Item]


class Item(pydantic.BaseModel):
    name: str


@pytest.mark.xfail(raises=pydantic.errors.ConfigError)
def test_container_create_error() -> None:
    container = Container(contains=[Item(name="name")])
    assert container.contains == [Item(name="name")]


@pytest.mark.update_forward_refs(
    ("Container", "Item"),
    (Container, Item),
)
def test_container_create_successfully() -> None:
    container = Container(contains=[Item(name="name")])
    assert container.contains == [Item(name="name")]
