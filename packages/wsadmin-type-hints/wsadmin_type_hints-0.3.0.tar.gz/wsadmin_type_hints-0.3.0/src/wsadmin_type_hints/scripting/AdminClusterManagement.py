""" The AdminClusterManagement script library provides the script
    procedures that configure and administer server clusters.

    The AdminClusterManagement script library provides the following script procedures.
    To display detailed information about each script procedure, use the help command for
    the AdminClusterManagement script library, specifying the name of the script of interest
    as an argument.
"""

from typing import Any

    
def checkIfClusterExists(*args: Any) -> Any:
    """ Display whether the cluster of interest exists in your configuration. """
    ...

def checkIfClusterMemberExists(*args: Any) -> Any:
    """ Display whether the cluster server member of interest exists in your configuration. """
    ...

def createClusterMember(*args: Any) -> Any:
    """ Assigns a server cluster member to a specific cluster. When you create the first cluster member, 
        a copy of that member is stored as part of the cluster data and becomes the template for all additional cluster members that you create.
    """
    ...

def createClusterWithFirstMember(*args: Any) -> Any:
    """ Create a new cluster configuration and adds the first cluster member to the cluster. """
    ...

def createClusterWithoutMember(*args: Any) -> Any:
    """ Create a new cluster configuration in your environment. """
    ...

def createFirstClusterMemberWithTemplate(*args: Any) -> Any:
    """ Use a template to add the first server cluster member to a specific cluster. 
    
        A copy of the first cluster member that you create is stored in the cluster scope as a template.
    """
    ...

def createFirstClusterMemberWithTemplateNodeServer(*args: Any) -> Any:
    """ Use a node with an existing application server as a template to create a new cluster member in your configuration. 
    
        When you create the first cluster member, a copy of that member is stored as part of the cluster data and
        becomes the template for all additional cluster members that you create.
    """
    ...

def deleteCluster(*args: Any) -> Any:
    """ Delete the configuration of a server cluster. 
    
        A server cluster consists of a group of application servers that are referred to as cluster members.
        The script deletes the server cluster and each of its cluster members.
    """
    ...

def deleteClusterMember(*args: Any) -> Any:
    """ Remove a cluster member from your cluster configuration. """
    ...

def help(*args: Any) -> Any:
    """ Provides AdminClusterManagement script library online help. """
    ...

def immediateStopAllRunningClusters(*args: Any) -> Any:
    """ Stop the server cluster members for each active cluster within a specific cell. 
        
        The server ignores any current or pending tasks.
    """
    ...

def immediateStopSingleCluster(*args: Any) -> Any:
    """ Stop the server cluster members for a specific cluster within a cell. 
        
        The server ignores any current or pending tasks.
    """
    ...

def listClusterMembers(*args: Any) -> Any:
    """ Display the server cluster members that exist in a specific cluster configuration. """
    ...

def listClusters(*args: Any) -> Any:
    """ Display each cluster that exists in your configuration. """
    ...

def rippleStartAllClusters(*args: Any) -> Any:
    """ Stop and restarts each cluster within a cell configuration. """
    ...

def rippleStartSingleCluster(*args: Any) -> Any:
    """ Stop and restarts the cluster members within a specific cluster configuration. """
    ...

def startAllClusters(*args: Any) -> Any:
    """ Start each cluster within a cell configuration. """
    ...

def startSingleCluster(*args: Any) -> Any:
    """ Start a specific cluster in your configuration. """
    ...

def stopAllClusters(*args: Any) -> Any:
    """ Stop the server cluster members of each active cluster within a specific cell. 
        
        Each server stops in a manner that allows the server to finish existing requests and allows failover to another member of the cluster.
    """
    ...

def stopSingleCluster(*args: Any) -> Any:
    """ Stop the server cluster members of a specific active cluster within a cell. 
        
        Each server stops in a manner that allows the server to finish existing requests and allows failover to another member of the cluster.
    """
    ...
