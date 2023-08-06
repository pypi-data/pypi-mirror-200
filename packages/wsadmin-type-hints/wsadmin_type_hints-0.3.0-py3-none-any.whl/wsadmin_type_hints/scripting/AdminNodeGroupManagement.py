""" The AdminNodeGroupManagement script library provides script
    procedures that configure and administer node group settings.

    The AdminNodeGroupManagement script library provides the following script procedures.
    To display detailed information about each script procedure, use the help command for
    the AdminNodeGroupManagement script library, specifying the name of the script of interest
    as an argument.
"""

from typing import Any

    
def addNodeGroupMember(*args: Any) -> Any:
    """ Add a node to a node group that exists in your configuration. """
    ...

def checkIfNodeExists(*args: Any) -> Any:
    """ Display whether the node of interest exists in a specific node group. """
    ...

def checkIfNodeGroupExists(*args: Any) -> Any:
    """ Display whether a specific node group exists in your configuration. """
    ...

def createNodeGroup(*args: Any) -> Any:
    """ Create a new node group in your configuration. """
    ...

def createNodeGroupProperty(*args: Any) -> Any:
    """ Assigns custom properties to the node group of interest. """
    ...

def deleteNodeGroup(*args: Any) -> Any:
    """ Delete a node group from your configuration. """
    ...

def deleteNodeGroupMember(*args: Any) -> Any:
    """ Remove a node from a specific node group in your configuration. """
    ...

def deleteNodeGroupProperty(*args: Any) -> Any:
    """ Remove a specific custom property from a node group. """
    ...

def help(*args: Any) -> Any:
    """ Display the script procedures that the AdminNodeGroupManagement script library supports.
    
    To display detailed help for a specific script, specify the name of the script of interest.
    """
    ...

def listNodeGroupMembers(*args: Any) -> Any:
    """ List the name of each node that is configured within a specific node group. """
    ...

def listNodeGroupProperties(*args: Any) -> Any:
    """ List the custom properties that are configured within a specific node group. """
    ...

def listNodeGroups(*args: Any) -> Any:
    """ Display the node groups that exist in your configuration.
    
    If you specify the name of a specific node, the script returns the name of the node group to which the node belongs.
    """
    ...

def modifyNodeGroup(*args: Any) -> Any:
    """ Modify the short name and description of a node group. """
    ...

def modifyNodeGroupProperty(*args: Any) -> Any:
    """ Modify the value of a custom property assigned to a node group. """
    ...
