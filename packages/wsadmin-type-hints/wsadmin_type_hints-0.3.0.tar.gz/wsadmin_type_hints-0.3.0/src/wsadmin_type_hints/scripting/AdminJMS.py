""" The AdminJMS script library provides the script
        procedures that configure and query Java Messaging Services (JMS) provider and resource settings.

        The AdminJMS script library provides the following script procedures.
        To display detailed information about each script library, use the help command
        for the AdminJMS script library, specifying the name of the script of interest
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
                "readAhead=AlwaysOff, maxBatchSize=54" or
                [["readAhead", "AlwaysOff"], ["maxBatchSize", 54]]
"""
from typing import Any


def createGenericJMSConnectionFactory(*args: Any) -> Any:
    """ Create a new GenericJMSConnectionFactory. """
    ...

def createGenericJMSConnectionFactoryAtScope(*args: Any) -> Any:
    """ Create a new GenericJMSConnectionFactory on the specified scope. """
    ...

def createGenericJMSConnectionFactoryUsingTemplate(*args: Any) -> Any:
    """ Create a new GenericJMSConnectionFactory using template. """
    ...

def createGenericJMSConnectionFactoryUsingTemplateAtScope(*args: Any) -> Any:
    """ Create a new GenericJMSConnectionFactory using template on the specified scope. """
    ...

def createGenericJMSDestination(*args: Any) -> Any:
    """ Create a new GenericJMSDestination. """
    ...

def createGenericJMSDestinationAtScope(*args: Any) -> Any:
    """ Create a new GenericJMSDestination on the specified scope. """
    ...

def createGenericJMSDestinationUsingTemplate(*args: Any) -> Any:
    """ Create a new GenericJMSDestination using template. """
    ...

def createGenericJMSDestinationUsingTemplateAtScope(*args: Any) -> Any:
    """ Create a new GenericJMSDestination using template on the specified scope. """
    ...

def createJMSProvider(*args: Any) -> Any:
    """ Create a new JMSProvider. """
    ...

def createJMSProviderAtScope(*args: Any) -> Any:
    """ Create a new JMSProvider on the specified scope. """
    ...

def createJMSProviderUsingTemplate(*args: Any) -> Any:
    """ Create a new JMSProvider using template. """
    ...

def createJMSProviderUsingTemplateAtScope(*args: Any) -> Any:
    """ Create a new JMSProvider using template on the specified scope. """
    ...

def createSIBJMSActivationSpec(*args: Any) -> Any:
    """ Create a SIB JMS ActivationSpec. """
    ...

def createSIBJMSConnectionFactory(*args: Any) -> Any:
    """ Create a SIB JMS Connection factory. """
    ...

def createSIBJMSQueue(*args: Any) -> Any:
    """ Create a SIB JMS Queue. """
    ...

def createSIBJMSQueueConnectionFactory(*args: Any) -> Any:
    """ Create a SIB JMS Queue Connection factory. """
    ...

def createSIBJMSTopic(*args: Any) -> Any:
    """ Create a SIB JMS Topic. """
    ...

def createSIBJMSTopicConnectionFactory(*args: Any) -> Any:
    """ Create a SIB JMS Topic Connection factory. """
    ...

def createWASTopic(*args: Any) -> Any:
    """ Create a new WASTopic. """
    ...

def createWASTopicAtScope(*args: Any) -> Any:
    """ Create a new WASTopic on the specified scope. """
    ...

def createWASTopicUsingTemplate(*args: Any) -> Any:
    """ Create a new WASTopic using template. """
    ...

def createWASTopicUsingTemplateAtScope(*args: Any) -> Any:
    """ Create a new WASTopic using template on the specified scope. """
    ...

def createWASTopicConnectionFactory(*args: Any) -> Any:
    """ Create a new WASTopicConnectionFactory. """
    ...

def createWASTopicConnectionFactoryAtScope(*args: Any) -> Any:
    """ Create a new WASTopicConnectionFactory on the specified scope. """
    ...

def createWASTopicConnectionFactoryUsingTemplate(*args: Any) -> Any:
    """ Create a new WASTopicConnectionFactory using template. """
    ...

def createWASTopicConnectionFactoryUsingTemplateAtScope(*args: Any) -> Any:
    """ Create a new WASTopicConnectionFactory using template on the specified scope. """
    ...

def createWASQueue(*args: Any) -> Any:
    """ Create a new WASQueue. """
    ...

def createWASQueueAtScope(*args: Any) -> Any:
    """ Create a new WASQueue on the specified scope. """
    ...

def createWASQueueUsingTemplate(*args: Any) -> Any:
    """ Create a new WASQueueUsingTemplate. """
    ...

def createWASQueueUsingTemplateAtScope(*args: Any) -> Any:
    """ Create a new WASQueueUsingTemplate on the specified scope. """
    ...

def createWASQueueConnectionFactory(*args: Any) -> Any:
    """ Create a new WASQueueConnectionFactory. """
    ...

def createWASQueueConnectionFactoryAtScope(*args: Any) -> Any:
    """ Create a new WASQueueConnectionFactory on the specified scope. """
    ...

def createWASQueueConnectionFactoryUsingTemplate(*args: Any) -> Any:
    """ Create a new WASQueueConnectionFactory using template. """
    ...

def createWASQueueConnectionFactoryUsingTemplateAtScope(*args: Any) -> Any:
    """ Create a new WASQueueConnectionFactory using template on the specified scope. """
    ...

def createWMQActivationSpec(*args: Any) -> Any:
    """ Create a WMQ ActivationSpec. """
    ...

def createWMQConnectionFactory(*args: Any) -> Any:
    """ Create a WMQ Connection factory. """
    ...

def createWMQQueue(*args: Any) -> Any:
    """ Create a WMQ Queue. """
    ...

def createWMQQueueConnectionFactory(*args: Any) -> Any:
    """ Create a WMQ Queue Connection factory. """
    ...

def createWMQTopic(*args: Any) -> Any:
    """ Create a WMQ Topic. """
    ...

def createWMQTopicConnectionFactory(*args: Any) -> Any:
    """ Create a WMQ Topic Connection factory. """
    ...

def listGenericJMSConnectionFactories(*args: Any) -> Any:
    """ List GenericJMSConnectionFactories. """
    ...

def listGenericJMSConnectionFactoryTemplates(*args: Any) -> Any:
    """ List GenericJMSConnectionFactory templates. """
    ...

def listGenericJMSDestinations(*args: Any) -> Any:
    """ List GenericJMSDestinations. """
    ...

def listGenericJMSDestinationTemplates(*args: Any) -> Any:
    """ List GenericJMSDestination templates. """
    ...

def listJMSConnectionFactories(*args: Any) -> Any:
    """ List JMSConnectionFactories. """
    ...

def listJMSDestinations(*args: Any) -> Any:
    """ List JMSDestinations. """
    ...

def listJMSProviders(*args: Any) -> Any:
    """ List JMSProviders. """
    ...

def listJMSProviderTemplates(*args: Any) -> Any:
    """ List JMSProvider templates. """
    ...

def listWASTopics(*args: Any) -> Any:
    """ List WASTopics. """
    ...

def listWASTopicConnectionFactories(*args: Any) -> Any:
    """ List WASTopicConnectionFactories. """
    ...

def listWASTopicConnectionFactoryTemplates(*args: Any) -> Any:
    """ List WASTopicConnectionFactory templates. """
    ...

def listWASTopicTemplates(*args: Any) -> Any:
    """ List WASTopic templates. """
    ...

def listWASQueues(*args: Any) -> Any:
    """ List WASQueues. """
    ...

def listWASQueueConnectionFactories(*args: Any) -> Any:
    """ List WASQueueConnectionFactories. """
    ...

def listWASQueueConnectionFactoryTemplates(*args: Any) -> Any:
    """ List WASQueueConnectionFactory templates. """
    ...

def listWASQueueTemplates(*args: Any) -> Any:
    """ List WASQueue templates. """
    ...

def startListenerPort(*args: Any) -> Any:
    """ Start the listener port. """
    ...

def help(*args: Any) -> Any:
    """ Provide AdminJMS script library online help. """
    ...
