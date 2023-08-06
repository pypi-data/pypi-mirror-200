# ♻️ pydwrap pydantic optional fields ♻️


pydwrap stores a **Option** object to implement unpacking of values if they are not **None**. The **BaseModel** object is also a little extended to work with the **Option** object.


[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pypi](https://img.shields.io/pypi/v/pydwrap.svg)](https://pypi.python.org/pypi/pydwrap)
[![versions](https://img.shields.io/pypi/pyversions/pydwrap.svg)](https://github.com/luwqz1/pydwrap)
[![license](https://img.shields.io/github/license/luwqz1/pydwrap.svg)](https://github.com/luwqz1/pydwrap/blob/main/LICENSE)


# ⭐️ A simple example ⭐️
```python
from pydwrap import BaseModel, Option

class User(BaseModel):
    name: Option[str]
    age: int

data = {
    "age": 20
}
user = User(**data)
#> User(name=Option(None), age=20)
print("Hello", user.name.unwrap(error_msg="What's your name?") + "!")
#> ValueError: What's your name?
```

# 📚 Documentation 📚
* In 🇷🇺 [**Russian**](https://github.com/luwqz1/pydwrap/blob/main/docs/RU.md) 🇷🇺
* In 🇺🇸 [**English**](https://github.com/luwqz1/pydwrap/blob/main/docs/EN.md) 🇺🇸