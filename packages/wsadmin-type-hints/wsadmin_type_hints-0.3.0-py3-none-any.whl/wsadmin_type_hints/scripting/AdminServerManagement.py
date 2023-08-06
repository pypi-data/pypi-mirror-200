""" The AdminServerManagement script library provides script
        procedures that configure, administer, and query server settings.

        The AdminServerManagement script library provides the following script procedures.
        To display detailed information about each script procedure, use the help command for
        the AdminServerManagement script library, specifying the name of the script of interest
        as an argument.
"""

# Group 1: ServerConfiguration

from typing import Any

    
def checkIfServerExists(*args: Any) -> Any:
    """ Determine whether the server of interest exists in your configuration. """
    ...

def checkIfServerTemplateExists(*args: Any) -> Any:
    """ Determine whether the server template of interest exists in your configuration. """
    ...

def configureApplicationServerClassloader(*args: Any) -> Any:
    """ Configure a class loader for the application server.
    
        Class loaders enable applications that are deployed on the application server to access repositories of available classes and resources.
    """
    ...

def configureCookieForServer(*args: Any) -> Any:
    """ Configure cookies in your application server configuration. Configure cookies to track sessions. """
    ...

def configureCustomProperty(*args: Any) -> Any:
    """ Configure custom properties in your application server configuration. 
    
        You can use custom properties for configuring internal system properties which some components use,
        for example, to pass information to a Web container.
    """
    ...

def configureEndPointsHost(*args: Any) -> Any:
    """ Configure the hostname of the server endpoints. """
    ...

def configureProcessDefinition(*args: Any) -> Any:
    """ Configure the server process definition.
    
        Enhance the operation of an application server by defining command-line information for starting
        or initializing the application server process.
    """
    ...

def configureSessionManagerForServer(*args: Any) -> Any:
    """ This script configures the session manager for the application server.
    
        Sessions allow applications running in a Web container to keep track of individual users.
    """
    ...

def createApplicationServer(*args: Any) -> Any:
    """ Create a new application server. """
    ...

def createAppServerTemplate(*args: Any) -> Any:
    """ Create a new application server template. """
    ...

def createGenericServer(*args: Any) -> Any:
    """ Create a new generic server. """
    ...

def createWebServer(*args: Any) -> Any:
    """ Create a new Web server. """
    ...

def deleteServer(*args: Any) -> Any:
    """ Delete a server. """
    ...

def deleteServerTemplate(*args: Any) -> Any:
    """ Delete a server template. """
    ...

def getJavaHome(*args: Any) -> Any:
    """ Display the Java home value. """
    ...

def getServerPID(*args: Any) -> Any:
    """ Display the server process ID. """
    ...

def getServerProcessType(*args: Any) -> Any:
    """ Display the type of server process for a specific server. """
    ...

def listJVMProperties(*args: Any) -> Any:
    """ Display the properties that are associated with your Java virtual machine (JVM) configuration. """
    ...

def listServerTemplates(*args: Any) -> Any:
    """ Display the server templates in your configuration. """
    ...

def listServerTypes(*args: Any) -> Any:
    """ Display the server types available on the node of interest. """
    ...

def listServers(*args: Any) -> Any:
    """ Display the servers that exist in your configuration. """
    ...

def queryMBeans(*args: Any) -> Any:
    """ Query the application server for Managed Beans (MBeans). """
    ...

def setJVMProperties(*args: Any) -> Any:
    """ Set Java Virtual Machine properties"""
    ...

def showServerInfo(*args: Any) -> Any:
    """ Display server configuration properties for the server of interest. """
    ...

def startAllServers(*args: Any) -> Any:
    """ Start each available server on a specific node. """
    ...

def startSingleServer(*args: Any) -> Any:
    """ Start a single server on a specific node. """
    ...

def stopAllServers(*args: Any) -> Any:
    """ Stop each running server on a specific node. """
    ...

def stopSingleServer(*args: Any) -> Any:
    """ Stop a single running server on a specific node. """
    ...

def viewProductInformation(*args: Any) -> Any:
    """ Display the application server product version. """

# Group 2: ServerTracingAndLoggingConfiguration
    ...

def configureJavaProcessLogs(*args: Any) -> Any:
    """ Configure Java process logs for the application server.
    
        The system creates the JVM logs by redirecting the System.out and System.err streams of the JVM to independent log files.
    """
    ...

def configureJavaVirtualMachine(*args: Any) -> Any:
    """ Configure a Java virtual machine (JVM).
    
        The application server, being a Java process, requires a JVM in order to run, and to support the Java applications running on it.
    """
    ...

def configurePerformanceMonitoringService(*args: Any) -> Any:
    """ Configure performance monitoring infrastructure (PMI) in your configuration. """
    ...

def configurePMIRequestMetrics(*args: Any) -> Any:
    """ Configure PMI request metrics in your configuration. """
    ...

def configureRASLoggingService(*args: Any) -> Any:
    """ Configure the RAS logging service. """
    ...

def configureServerLogs(*args: Any) -> Any:
    """ Configure server logs for the application server of interest. """
    ...

def configureTraceService(*args: Any) -> Any:
    """ Configure trace settings for the application server.
    
        Configure trace to obtain detailed information about running the application server.
    """
    ...

def setTraceSpecification(*args: Any) -> Any:
    """ Set the trace specification for the server. """

# Group 3: OtherServicesConfiguration
    ...

def configureAdminService(*args: Any) -> Any:
    """ Configure the AdminService interface.
    
        The AdminService interface is the server-side interface to the application server administration functions.
    """
    ...

def configureCustomService(*args: Any) -> Any:
    """ Configure a custom service in your application server configuration.
    
        Each custom services defines a class that is loaded and initialized whenever the server starts and shuts down.
    """
    ...

def configureDynamicCache(*args: Any) -> Any:
    """ Configure the dynamic cache service in your server configuration.
    
        The dynamic cache service works within an application server Java virtual machine (JVM), intercepting calls to cacheable objects.
    """
    ...

def configureEJBContainer(*args: Any) -> Any:
    """ Configure an Enterprise JavaBeans (EJB) container in your server configuration.
    
        An EJB container provides a run-time environment for enterprise beans within the application server.
    """
    ...

def configureFileTransferService(*args: Any) -> Any:
    """ Configure the file transfer service for the application server.
    
        The file transfer service transfers files from the deployment manager to individual remote nodes.
    """
    ...

def configureHTTPTransportEndPointForWebContainer(*args: Any) -> Any:
    """ Configure HTTP transport endpoint for a Web container. """
    ...

def configureHTTPTransportForWebContainer(*args: Any) -> Any:
    """ Configure HTTP transports for a Web container.
    
        Transports provide request queues between application server plug-ins for Web servers and Web containers
        in which the Web modules of applications reside.
    """
    ...

def configureListenerPortForMessageListenerService(*args: Any) -> Any:
    """ Configure the listener port for the message listener service in your server configuration.
    
        The message listener service is an extension to the Java Messaging Service (JMS) functions of the JMS provider.
    """
    ...

def configureMessageListenerService(*args: Any) -> Any:
    """ Configure the message listener service in your server configuration.
    
        The message listener service is an extension to the Java Messaging Service (JMS) functions of the JMS provider.
    """
    ...

def configureORBService(*args: Any) -> Any:
    """ Configure an Object Request Broker (ORB) service in your server configuration.
    
        An Object Request Broker (ORB) manages the interaction between clients and servers, using the Internet InterORB Protocol (IIOP).
    """
    ...

def configureRuntimeTransactionService(*args: Any) -> Any:
    """ Configure the transaction service for your server configuration.
    
        The transaction service is a server runtime component that coordinates updates to multiple resource managers to ensure atomic updates of data.
    """
    ...

def configureStateManageable(*args: Any) -> Any:
    """ Configure the initial state of the application server.
    
        The initial state refers to the desired state of the component when the server process starts.
    """
    ...

def configureThreadPool(*args: Any) -> Any:
    """ Configure thread pools in your server configuration.
    
        A thread pool enables components of the server to reuse threads, which eliminates the need to create new threads at run time.
    """
    ...

def configureTransactionService(*args: Any) -> Any:
    """ Configure the transaction service for your application server. """
    ...

def configureWebContainer(*args: Any) -> Any:
    """ Configure Web containers in your application server configuration.
    
        A Web container handles requests for servlets, JavaServer Pages (JSP) files, and other types of files that include server-side code.
    """
    ...

def help(*args: Any) -> Any:
    """ Provides AdminServerManagement script library online help. """
    ...
