"""
`import` this module to gain intellisense on the 5 main `wsadmin.sh` Jython language objects:

- [`AdminControl`](/reference/wsadmin_type_hints/core/AdminControl/)
- [`AdminConfig`](/reference/wsadmin_type_hints/core/AdminConfig/)
- [`AdminApp`](/reference/wsadmin_type_hints/core/AdminApp/)
- [`AdminTask`](/reference/wsadmin_type_hints/core/AdminTask/)
- [`Help`](/reference/wsadmin_type_hints/core/Help/)


Use it like this:
```python
try:
    (AdminControl, AdminConfig, AdminApp, AdminTask, Help)
except NameError:
    from wsadmin_type_hints import AdminControl, AdminConfig, AdminApp, AdminTask, Help
else:
    print("AdminControl is already defined, no shim needed")
```

This way it will be imported only in your development environment.
"""

__all__ = [
    "AdminApp",
    "AdminConfig",
    "AdminTask",
    "AdminControl",
    "Help",
]

# Additional try/except to ensure that even if installed in a real environment,
# the original modules do not get overwritten.
try:
    (AdminControl, AdminConfig, AdminApp, AdminTask, Help) # pyright: ignore[reportUnboundVariable, reportUnusedExpression]
except NameError:
    # ----- Interact with a configuration object    -----
    from . import AdminApp
    from . import AdminConfig
    from . import AdminTask


    # -----     Interact with a runtime object      -----
    from . import AdminControl


    # -----              Helper module              -----
    from . import Help