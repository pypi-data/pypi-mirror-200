""" The AdminResources script library provides the script
    procedures that configure and administer mail, URL and resource provider settings.

    The AdminResources script library provides the following script procedures.
    To display detailed information about each script procedures, use the help command
    for the AdminResources script library, specifying the name of the script of interest
    as an argument.
    The script procedures that take the scope argument can be specified
    in the following formats (Cell, Node, Server, Cluster):
    for example, a cluster can be specified as:
            "Cell=myCell,Cluster=myCluster" or
            "/Cell:myCell/ServerCluster:myCluster/" or
            "myCluster(cells/myCell/clusters/myCluster|cluster.xml#Cluster_1)".
    A node can be specified as:
            "Cell=myCell,Node=myNode" or
            "/Cell:myCell/Node:myNode/" or
            "myNode(cells/myCell/nodes/myNode|node.xml#Node_1)"
    A server can be specified as:
            "Cell=myCell,Node=myNode,Server=myServer" or
            "/Cell:myCell/Node:myNode/Server:myServer/" or
            "myServer(cells/myCell/nodes/myNode/servers/myServer|server.xml#Server_1)"
    The script procedures that take the optional arguments can be specified
    with a list or string format:
    for example, otherAttributeList can be specified as:
            "description=my new resource, isolatedClassLoader=true" or
            [["description", "my new resource"], ["isolatedClassLoader", "true"]]
"""

from typing import Any


def createCompleteMailProvider(*args: Any) -> Any:
    """ Create a mail provider with protocol provider, mail session and custom property. """
    ...

def createCompleteMailProviderAtScope(*args: Any) -> Any:
    """ Create a mail provider with protocol provider, mail session and custom property at the scope. """
    ...

def createCompleteResourceEnvProvider(*args: Any) -> Any:
    """ Create a resource environment provider with resource environment referenceable, resource environment entry and custom property. """
    ...

def createCompleteResourceEnvProviderAtScope(*args: Any) -> Any:
    """ Create a resource environment provider with resource environment referenceable, resource environment entry and custom property at the scope. """
    ...

def createCompleteURLProvider(*args: Any) -> Any:
    """ Create an URL provider with URL and customer property. """
    ...

def createCompleteURLProviderAtScope(*args: Any) -> Any:
    """ Create an URL provider with URL and customer property at the scope. """
    ...

def createJAASAuthenticationAlias(*args: Any) -> Any:
    """ Create JAAS authentication alias. """
    ...

def createLibraryRef(*args: Any) -> Any:
    """ Create library reference. """
    ...

def createMailProvider(*args: Any) -> Any:
    """ Create a mail provider. """
    ...

def createMailProviderAtScope(*args: Any) -> Any:
    """ Create a mail provider at the scope. """
    ...

def createMailSession(*args: Any) -> Any:
    """ Create a mail session for mail provider. """
    ...

def createMailSessionAtScope(*args: Any) -> Any:
    """ Create a mail session for mail provider at the scope. """
    ...

def createProtocolProvider(*args: Any) -> Any:
    """ Create a protocol provider for the mail provider. """
    ...

def createProtocolProviderAtScope(*args: Any) -> Any:
    """ Create a protocol provider for the mail provider at the scope. """
    ...

def createResourceEnvEntries(*args: Any) -> Any:
    """ Create resource environment entry. """
    ...

def createResourceEnvEntriesAtScope(*args: Any) -> Any:
    """ Create resource environment entry at the scope. """
    ...

def createResourceEnvProvider(*args: Any) -> Any:
    """ Create a resource environment provider. """
    ...

def createResourceEnvProviderAtScope(*args: Any) -> Any:
    """ Create a resource environment provider at the scope. """
    ...

def createResourceEnvProviderRef(*args: Any) -> Any:
    """ Create resource environment provider referenceable. """
    ...

def createResourceEnvProviderRefAtScope(*args: Any) -> Any:
    """ Create resource environment provider referenceable at the scope. """
    ...

def createScheduler(*args: Any) -> Any:
    """ Create a scheduler resource. """
    ...

def createSchedulerAtScope(*args: Any) -> Any:
    """ Create a scheduler resource at the scope. """
    ...

def createSharedLibrary(*args: Any) -> Any:
    """ Create shared library. """
    ...

def createSharedLibraryAtScope(*args: Any) -> Any:
    """ Create shared library at the scope. """
    ...

def createURL(*args: Any) -> Any:
    """ Create new URL for url provider. """
    ...

def createURLAtScope(*args: Any) -> Any:
    """ Create new URL for url provider at the scope. """
    ...

def createURLProvider(*args: Any) -> Any:
    """ Create URL provider. """
    ...

def createURLProviderAtScope(*args: Any) -> Any:
    """ Create URL provider at the scope. """
    ...

def createWorkManager(*args: Any) -> Any:
    """ Create work manager. """
    ...

def createWorkManagerAtScope(*args: Any) -> Any:
    """ Create work manager at the scope. """
    ...

def help(*args: Any) -> Any:
    """ Provide AdminResources script library online help. """
    ...
