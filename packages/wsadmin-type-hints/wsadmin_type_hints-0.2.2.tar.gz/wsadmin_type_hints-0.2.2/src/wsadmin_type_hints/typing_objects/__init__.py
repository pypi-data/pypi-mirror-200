"""
This module is used internally by `wsadmin-type-hints` to define appropriate return types for some `wsadmin` methods.

!!! Warning "Please read before continuing"
    _**The classes and types present in this sub-module are NOT meant to be referenced in user scripts**_.

    These are only meant to be used internally by `wsadmin-type-hints`.

    The **actual return type** is the one they inherit from (_for example `RunningObjectName` inherits from `str`, 
        so the actual return type will be `str`_).

    This structure is needed to make the code more **pythonic** and **readable**.
    It also makes it clear just by glancing to the method signature **which** value must be passed,
        instead of remembering which `wsadmin` object method returns the correct Object name.
"""
