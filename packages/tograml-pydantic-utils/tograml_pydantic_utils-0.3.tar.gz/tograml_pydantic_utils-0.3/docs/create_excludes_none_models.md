At some point when you create
models you want them to exclude
unused fields - there are several ways to do this:

1. explicitly

```python
from __future__ import annotations

import typing

import pydantic


class Example(pydantic.BaseModel):
    field: typing.Optional[str] = None


model = Example()
model.dict(exclude={"field"})
# or
model.dict(exclude_defaults=True)
# or
model.dict(exclude_none=True)
```

2. Using `ExcludesNone` mixin

```python
from __future__ import annotations

import typing

import pydantic
import tograml_pydantic_utils


# class Example(tograml_pydantic_utils.TogramlModel)
class Example(tograml_pydantic_utils.ExcludesNone, pydantic.BaseModel):
    field: typing.Optional[str] = None

    
model = Example()
model.dict()
```

all of this will show the same result:
models converted to a dictionary will not
have `field` because it has the value `None`.
