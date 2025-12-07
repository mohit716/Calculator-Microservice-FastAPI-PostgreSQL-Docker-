from datetime import datetime
from pydantic import BaseModel, PositiveInt

class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]

external_data = {
    'id': '123',
    'signup_ts': '2019-06-01 12:22',
    'tastes': {
        'wine': 9,
        b'cheese': 7,
        'cabbage': '1',
    },
    }

user = User(**external_data)

print(user.id)
#> 123
print(user.model_dump())
"""
    'id': 123,
    'name': 'John Doe',
    'signup_ts': datetime.datetime(2019, 6, 1, 12, 22),
    'tastes': {'wine': 9, 'cheese': 7, 'cabbage': 1},
    },
"""



# If validation fails, Pydantic will raise an error with a breakdown of what was wrong:
# continuing  the above example...
class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]


external_data = {'id': 'not an int', 'tastes':{}}

try:
    user = User(**external_data)
except ValidationError as e:
    print(e.errors())
f"""
[
{
    'type': 'int_parsing',
    'loc': ('id',),
    'msg': 'Input should be a valid integer, got "not an int" instead',
    'input': 'not an int',
    'url': 'https://errors.pydantic.dev/2.10/v/int_parsing',
},


{
    'type': 'missing',
    'loc': ('tastes',),
    'msg': 'Field required',
    'input': None,
    'url': 'https://errors.pydantic.dev/2.10/v/missing',
},
]
"""


# links: https://docs.pydantic.dev/latest/#pydantic-examples
 #      :https://fastapi.tiangolo.com/tutorial/path-params/#standards-based-benefits-alternative-documentation


# good intuition of pydantic
"""
Instead of “unnatural,” think of Pydantic as:

A contract enforcer: You declare the contract (price must be float), and Pydantic enforces it.

A smart gatekeeper: It looks at the arguments, runs the hidden if/else checks, and either lets them through (coerced/validated) or blocks them with a ValidationError.
"""