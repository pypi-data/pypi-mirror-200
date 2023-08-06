"""
`import` this module to gain intellisense on the 5 main `wsadmin.sh` Jython
language objects and all the scripts in the Jython scripting library.

Use it like this: 
```python
try:
    (AdminControl, AdminConfig, AdminApp, AdminTask, Help)
except NameError:
    from wsadmin_type_hints import AdminControl, AdminConfig, AdminApp, AdminTask, Help
```

!!! Warning
    Importing with a **wildcard import** is _generally discouraged_ and considered **bad practice**, so **avoid it if possible**.

    From my tests I've also found that intellisense **may** not work properly when modules are imported through a wildcard.
    In my case Visual Studio Code was not be able to provide suggestions for a module function.

    - **Works**:
        ```python
        try:
            (AdminControl, AdminConfig, AdminApp, AdminTask, Help)  # type: ignore
        except NameError:
            from wsadmin_type_hints import AdminConfig, AdminTask, AdminJMS
        ```

    - Also **works** (use parenthesis for _better readability_ through nesting):
        ```python
        try:
            (AdminControl, AdminConfig, AdminApp, AdminTask, Help)  # type: ignore
        except NameError:
            from wsadmin_type_hints import (
                AdminConfig, 
                AdminTask, 
                AdminJMS
            )
        ```

    - **_MAY_ not work**:
        ```python
        try:
            (AdminControl, AdminConfig, AdminApp, AdminTask, Help)  # type: ignore
        except NameError:
            from wsadmin_type_hints import *
        ```


This way it will be imported only in your development environment.
"""

# import sys
# if sys.version_info <= (3, 5):
#     # Specific minor version features can be easily checked with tuples.
# 	raise Exception("Your Python version does not satisfy the minimum requirements")

# Additional try/except to ensure that even if installed in a real environment,
# the original modules do not get overwritten.
try:
    (AdminControl, AdminConfig, AdminApp, AdminTask, Help) # pyright: ignore[reportUnboundVariable, reportUnusedExpression]
except NameError:
    # -----     Core wsadmin objects     -----
    from wsadmin_type_hints.core import *

    # -----   Jython Scripting library   -----
    from wsadmin_type_hints.scripting import *