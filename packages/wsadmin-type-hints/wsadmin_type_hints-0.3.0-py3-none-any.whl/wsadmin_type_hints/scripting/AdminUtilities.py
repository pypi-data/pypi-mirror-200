"""The `AdminUtilities` script library provides the script
    procedures that administer utilities settings.

    The `AdminUtilities` script library provides the following script procedures.
    To display detailed information about each script procedures, use the help command
    for the `AdminUtilities` script library, specifying the name of the script of interest
    as an argument.
"""
from typing import Any


def convertToList(*args: Any):
    """ Convert string to list. """
    ...

def configureAutoSave(*args: Any):
    """ Configure the configuration automation save. """
    ...

def debugNotice(*args: Any):
    """ Set debug notice. """
    ...

def getExceptionText(type: Any, value: Any, tb: Any) -> str:
    """ Get exception text. 

    Args:
        type (_type_): _description_
        value (_type_): _description_
        tb (_type_): _description_

    Returns:
        message(str): Exception message with exception type, exception value or traceback information

    Example:
        ```pycon
        >>> AdminUtilities.getExceptionText(typ, value, tb)
        ```
    """
    ...

def fail(msg: str):
    """ Prints a failure message.

    Args:
        msg (str): The message to print.
    
    Example:
        ```pycon
        >>> AdminUtilities.fail("TEST")

        FAILURE: 'TEST'

        ```
    """    
    ...

def fileSearch(*args: Any):
    """ Recrusive file search. """
    ...

def getResourceBundle(*args: Any):
    """ Get resource bundle. """
    ...

def getScriptLibraryFiles(*args: Any):
    """ Get the script library files. """
    ...

def getScriptLibraryList(*args: Any):
    """ Get the script library names of list. """
    ...

def getScriptLibraryPath(*args: Any):
    """ Get the script library path. """
    ...

def help(function: str = ""):
    """ Provide online help. 
    
    Receive help information for the specified `AdminUtilities` library function
        or provide help information on all of the `AdminUtilities` script library
        function if parameters are not passed.
    """
    ...

def infoNotice(*args: Any):
    """ Set information notice. """
    ...

def save(*args: Any):
    """ Save all configuration change. """
    ...

def setDebugNotices(*args: Any):
    """ Set debug notice. """
    ...

def setFailOnErrorDefault(*args: Any):
    """ Set failonerror default. """
    ...

def sleepDelay(secs: int):
    """ Set sleep delay. """
    ...

def warningNotice(*args: Any):
    """ Set warning notice. """
    ...
