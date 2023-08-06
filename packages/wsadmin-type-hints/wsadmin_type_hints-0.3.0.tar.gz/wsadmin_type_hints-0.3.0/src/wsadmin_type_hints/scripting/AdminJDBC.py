"""The `AdminJDBC` script library provides the script
    procedures that configure and query Java Database Connectivity (JDBC) provider and data source settings.

    The `AdminJDBC` script library provides the following script procedures.
    To display detailed information about each script procedures, use the help command
    for the `AdminJDBC` script library, specifying the name of the script of interest
    as an argument.
    The script procedures that take the scope argument can be specified
    in following formats (Cell, Node, Server, Cluster):
    for example, a cluster can be specified as:
            "Cell=myCell,Cluster=myCluster" or
            "/Cell:myCell/ServerCluster:myCluster/" or
            "myCluster(cells/myCell/clusters/myCluster|cluster.xml#Cluster_1)"
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


def createDataSource(*args: Any) -> Any:
    """ Create a new data source in your configuration. """
    ...

def createJDBCProviderAtScope(*args: Any) -> Any:
    """ Create a new JDBC provider in your environment on the specified scope. """
    ...

def createDataSourceUsingTemplate(*args: Any) -> Any:
    """ Use a template to create a new data source in your configuration. """
    ...

def createJDBCProviderUsingTemplateAtScope(*args: Any) -> Any:
    """ Use a template to create a new JDBC provider in your environment on the specified scope. """
    ...

def createJDBCProvider(*args: Any) -> Any:
    """ Create a new JDBC provider in your environment. """
    ...

def createDataSourceAtScope(*args: Any) -> Any:
    """ Create a new data source in your configuration on the specified scope. """
    ...

def createJDBCProviderUsingTemplate(*args: Any) -> Any:
    """ Use a template to create a new JDBC provider in your environment. """
    ...

def createDataSourceUsingTemplateAtScope(*args: Any) -> Any:
    """ Use a template to create a new data source in your configuration on the specified scope. """
    ...

def listDataSources(*args: Any) -> Any:
    """ Display a list of configuration IDs for the data sources in your configuration. """
    ...

def listDataSourceTemplates(*args: Any) -> Any:
    """ Display a list of configuration IDs for the data source templates in your environment. """
    ...

def listJDBCProviders(*args: Any) -> Any:
    """ Display a list of configuration IDs for the JDBC providers in your environment. """
    ...

def listJDBCProviderTemplates(*args: Any) -> Any:
    """ Display a list of configuration IDs for the JDBC provider templates in your environment. """
    ...

def help(*args: Any) -> Any:
    """ Display AdminJDBC script library online help. """
    ...
