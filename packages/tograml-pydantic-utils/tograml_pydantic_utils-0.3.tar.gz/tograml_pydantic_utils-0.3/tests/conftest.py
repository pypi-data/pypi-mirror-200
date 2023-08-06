from __future__ import annotations

try:
    import pydantic
except ImportError:
    print("To run tests make sure pydantic is installed!")  # noqa
    exit(1)


import pytest

from tograml_pydantic_utils.update_forward_refs_helper import update_forward_refs_helper

MARK = "update_forward_refs"


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers", f"{MARK}(args): mark test to update forward refs in pydantic models"
    )


def pytest_runtest_setup(item: pytest.Item) -> None:
    mark = item.get_closest_marker(MARK)
    if mark and mark.args:
        __all__, __models__ = mark.args[0], mark.args[1]
        update_forward_refs_helper(
            __all__,
            dict(zip(__all__, __models__)),
        )
