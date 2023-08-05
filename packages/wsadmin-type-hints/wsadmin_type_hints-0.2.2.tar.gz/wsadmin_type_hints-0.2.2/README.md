[![Documentation](https://github.com/LukeSavefrogs/wsadmin-type-hints/actions/workflows/documentation.yml/badge.svg)](https://lukesavefrogs.github.io/wsadmin-type-hints/)

# `wsadmin-type-hints`
Python package providing **type hints** for `wsadmin` **Jython** commands.

This **speeds up** the development of `wsadmin` **Jython** scripts inside an IDE since it provides intellisense on every method of the 5 main objects provided at runtime by the `wsadmin`:
- `AdminControl`
- `AdminConfig`
- `AdminApp`
- `AdminTask`
- `Help`

[📚 **Read the full documentation**](https://lukesavefrogs.github.io/wsadmin-type-hints/)

## Features
- **List all module commands** through intellisense:

	![List module commands](https://raw.githubusercontent.com/LukeSavefrogs/wsadmin-type-hints/main/docs/images/60817fad50b7491f2d03e29e93568bfb74dd0ce265319675f2fb83cad67a46fa.png "List all module commands")

- Check **parameter and return types**, as well as a brief description of the command (using [Google syntax](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)):

	![Parameters](https://raw.githubusercontent.com/LukeSavefrogs/wsadmin-type-hints/main/docs/images/e84d4763b6a93d5950af4b85e9b43d04f8fda9b35a9c4d16ed0f52084dd27195.png "Parameter and return types")  

## Quick start
### Download
- Using `pip`:
	```
	pip install wsadmin-type-hints
	```

- Using `poetry`:
	```
	poetry add wsadmin-type-hints --group dev 
	```

### Usage
Use it like this:
```python
try:
    (AdminControl, AdminConfig, AdminApp, AdminTask, Help)
except NameError:
    from wsadmin_type_hints import *
else:
    print("AdminControl is already defined, i'm not needed here 😃")
```
The `try..except` block is used to differentiate between the development and production environment.



# Disclaimer
This is an unofficial package created for speeding up the development process and is not in any way affiliated with IBM®. All trademarks and registered trademarks are the property of their respective company owners.

The code does not include any implementation detail, and includes only the informations (such as parameter numbers, types and descriptions) publicly available on the official Websphere Application Server® documentation.
