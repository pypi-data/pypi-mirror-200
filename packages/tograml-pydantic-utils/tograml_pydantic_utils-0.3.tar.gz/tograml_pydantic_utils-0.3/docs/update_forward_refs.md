You do not need to manually write for each model:
`update_forward_refs`, the function will do this
for you - `update_forward_refs_helper`:

```python
from __future__ import annotations

from typing import List

import pydantic
import tograml_pydantic_utils


class Container(pydantic.BaseModel):
    contains: List[Item]


class Item(pydantic.BaseModel):
    name: str


try:
    container = Container(contains=[Item(name="item")])
except pydantic.errors.ConfigError:
    print("Please, update forward refs")

tograml_pydantic_utils.update_forward_refs_helper(
    ("Container", "Item",),
    globals(),
)
try:
    container = Container(contains=[Item(name="item")])
except pydantic.errors.ConfigError:
    print("Never raised")
else:
    print("No error raised")
```
