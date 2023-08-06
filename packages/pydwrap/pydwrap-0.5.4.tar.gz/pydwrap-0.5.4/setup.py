# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydwrap']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'pydwrap',
    'version': '0.5.4',
    'description': 'pydwrap stores a Option object to implement unpacking of values if they are not None. The BaseModel object is also a little extended to work with the Option object.',
    'long_description': '# ♻️ pydwrap pydantic optional fields ♻️\n\n\npydwrap stores a **Option** object to implement unpacking of values if they are not **None**. The **BaseModel** object is also a little extended to work with the **Option** object.\n\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pypi](https://img.shields.io/pypi/v/pydwrap.svg)](https://pypi.python.org/pypi/pydwrap)\n[![versions](https://img.shields.io/pypi/pyversions/pydwrap.svg)](https://github.com/luwqz1/pydwrap)\n[![license](https://img.shields.io/github/license/luwqz1/pydwrap.svg)](https://github.com/luwqz1/pydwrap/blob/main/LICENSE)\n\n\n# ⭐️ A simple example ⭐️\n```python\nfrom pydwrap import BaseModel, Option\n\nclass User(BaseModel):\n    name: Option[str]\n    age: int\n\ndata = {\n    "age": 20\n}\nuser = User(**data)\n#> User(name=Option(None), age=20)\nprint("Hello", user.name.unwrap(error_msg="What\'s your name?") + "!")\n#> ValueError: What\'s your name?\n```\n\n# 📚 Documentation 📚\n* In 🇷🇺 [**Russian**](https://github.com/luwqz1/pydwrap/blob/main/docs/RU.md) 🇷🇺\n* In 🇺🇸 [**English**](https://github.com/luwqz1/pydwrap/blob/main/docs/EN.md) 🇺🇸',
    'author': 'Georgy howl',
    'author_email': 'howluwqz1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/luwqz1/pydwrap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
