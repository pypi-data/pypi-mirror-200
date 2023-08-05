# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wsadmin_type_hints', 'wsadmin_type_hints.typing_objects']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wsadmin-type-hints',
    'version': '0.2.2',
    'description': 'Provide type hints for `wsadmin` object methods',
    'long_description': '[![Documentation](https://github.com/LukeSavefrogs/wsadmin-type-hints/actions/workflows/documentation.yml/badge.svg)](https://lukesavefrogs.github.io/wsadmin-type-hints/)\n\n# `wsadmin-type-hints`\nPython package providing **type hints** for `wsadmin` **Jython** commands.\n\nThis **speeds up** the development of `wsadmin` **Jython** scripts inside an IDE since it provides intellisense on every method of the 5 main objects provided at runtime by the `wsadmin`:\n- `AdminControl`\n- `AdminConfig`\n- `AdminApp`\n- `AdminTask`\n- `Help`\n\n[📚 **Read the full documentation**](https://lukesavefrogs.github.io/wsadmin-type-hints/)\n\n## Features\n- **List all module commands** through intellisense:\n\n\t![List module commands](https://raw.githubusercontent.com/LukeSavefrogs/wsadmin-type-hints/main/docs/images/60817fad50b7491f2d03e29e93568bfb74dd0ce265319675f2fb83cad67a46fa.png "List all module commands")\n\n- Check **parameter and return types**, as well as a brief description of the command (using [Google syntax](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)):\n\n\t![Parameters](https://raw.githubusercontent.com/LukeSavefrogs/wsadmin-type-hints/main/docs/images/e84d4763b6a93d5950af4b85e9b43d04f8fda9b35a9c4d16ed0f52084dd27195.png "Parameter and return types")  \n\n## Quick start\n### Download\n- Using `pip`:\n\t```\n\tpip install wsadmin-type-hints\n\t```\n\n- Using `poetry`:\n\t```\n\tpoetry add wsadmin-type-hints --group dev \n\t```\n\n### Usage\nUse it like this:\n```python\ntry:\n    (AdminControl, AdminConfig, AdminApp, AdminTask, Help)\nexcept NameError:\n    from wsadmin_type_hints import *\nelse:\n    print("AdminControl is already defined, i\'m not needed here 😃")\n```\nThe `try..except` block is used to differentiate between the development and production environment.\n\n\n\n# Disclaimer\nThis is an unofficial package created for speeding up the development process and is not in any way affiliated with IBM®. All trademarks and registered trademarks are the property of their respective company owners.\n\nThe code does not include any implementation detail, and includes only the informations (such as parameter numbers, types and descriptions) publicly available on the official Websphere Application Server® documentation.\n',
    'author': 'Luca Salvarani',
    'author_email': 'lucasalvarani99@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://lukesavefrogs.github.io/wsadmin-type-hints/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<=3.11',
}


setup(**setup_kwargs)
