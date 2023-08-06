""" The AdminNodeManagement script library provides the script
    procedures that configure and administer node group settings.

    The AdminNodeManagement script library provides the following script procedures.
    To display detailed information about each script procedures, use the help command for
    the AdminNodeManagement script library, specifying the name of the script of interest
    as an argument.
"""

from typing import Any


def configureDiscoveryProtocolOnNode(*args: Any) -> Any:
    """ Configure the node discovery protocol. """
    ...

def doesNodeExist(*args: Any) -> Any:
    """ Check if node exist in the cell. """
    ...

def isNodeRunning(*args: Any) -> Any:
    """ Check if node is running. """
    ...

def listNodes(*args: Any) -> Any:
    """ List available nodes in the cell. """
    ...

def restartActiveNodes(*args: Any) -> Any:
    """ Restart all running nodes in the cell. """
    ...

def restartNodeAgent(*args: Any) -> Any:
    """ Restart all running processes in the specified node. """
    ...

def stopNode(*args: Any) -> Any:
    """ Stop all the proceses in the specified node, including nodeagent and application servers. """
    ...

def stopNodeAgent(*args: Any) -> Any:
    """ Stop the nodeagent process in the specified node. """
    ...

def syncActiveNodes(*args: Any) -> Any:
    """ Synchronize all running nodes repository with the cell repository. """
    ...

def syncNode(*args: Any) -> Any:
    """ Synchronize the specified node repository with the cell repository. """
    ...

def help(*args: Any) -> Any:
    """ Provide AdminNodeManagement script library online help. """
    ...
