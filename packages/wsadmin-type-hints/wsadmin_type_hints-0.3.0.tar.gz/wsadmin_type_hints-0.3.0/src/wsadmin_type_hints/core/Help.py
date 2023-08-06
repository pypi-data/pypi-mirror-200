"""
You can use the `Help` command to find general help and dynamic online information. 

Use the `Help` object as an aid in writing and running scripts with the `AdminControl` object.

For more info see the [official documentation](https://www.ibm.com/docs/en/was-nd/8.5.5?topic=scripting-commands-help-object-using-wsadmin).
"""
from typing import Optional

from wsadmin_type_hints.typing_objects.object_name import RunningObjectName


def AdminApp() -> str:
    """
    Use the `AdminApp` command to view a summary of each available method for the `AdminApp` object.
    
    Returns:
        str: The list of available methods for the `AdminApp` object.

    Example:
        ```pycon
        >>> print(Help.AdminApp())
        WASX7095I: The AdminApp object allows application objects to
        be manipulated -- this includes installing, uninstalling, editing,
        and listing.  Most of the commands supported by AdminApp operate in two
        modes: the default mode is one in which AdminApp communicates with the
        product to accomplish its tasks.  A local mode is also
        possible, in which no server communication takes place.  The local
        mode of operation is invoked by bringing up the scripting client with
        no server connected using the command line "-conntype NONE" option or setting the 
        "com.ibm.ws.scripting.connectionType=NONE" property in the wsadmin.properties.
        [...]
        ```
    """
    ...


def AdminConfig() -> str:
    """Use the `AdminConfig` command to view a summary of each available method for the `AdminConfig` object.

    Returns:
        str: The list of available methods for the `AdminConfig` object.

    Example:
        ```pycon
        >>> print(Help.AdminApp())
        WASX7053I: The following functions are supported by AdminConfig: 
        [...]
        ```
    """
    ...

def AdminControl() -> str:
    """Use the `AdminControl` command to view a summary of each available method for the `AdminControl` object.

    Returns:
        str: The list of available methods for the `AdminControl` command.

    Example:
        ```pycon
        >>> print(Help.AdminControl())
        WASX7027I: The following functions are supported by AdminControl:
        [...]
        ```
    """
    ...

def AdminTask() -> str:
    """Use the `AdminTask` command to view a summary of each available method for the `AdminTask` object.

    Returns:
        str: The list of available methods for the `AdminTask` command.

    Example:
        ```pycon
        >>> print(Help.AdminTask())
        WASX8001I: The AdminTask object enables the available administrative commands. AdminTask commands 
        operate in two modes: the default mode is one whichAdminTask communicates with the
        product to accomplish its task. A local mode 
        is also available in which no server communication takes place. The local mode of operation is invoked by 
        bringing up the scripting client using the command line "-conntype NONE" option or setting the
        "com.ibm.ws.scripting.connectiontype=NONE" property in wsadmin.properties file.
        [...]
        ```
    """
    ...

def all(mbean_name: RunningObjectName, /) -> str:
    """Use the `all` command to view a summary of all the information associated with the MBean 
        identified by `mbean_name`.

    Args:
        mbean_name (RunningObjectName): The object name which identifies the desired MBean.

    Returns:
        str: Summary of the information requested.

    Example:
        ```pycon
        >>> mbean = AdminControl.queryNames('type=Server,*').splitlines()[0]
        >>> print(Help.all(mbean))
        Description: Managed object for overall server process.
        Class name: javax.management.modelmbean.RequiredModelMBean

        Attribute                       Type                            Access
        name                            java.lang.String                RO
        shortName                       java.lang.String                RO
        threadMonitorInterval           int                             RW
        threadMonitorThreshold          int                             RW
        threadMonitorAdjustmentThreshold  int                             RW
        pid                             java.lang.String                RO
        cellName                        java.lang.String                RO
        cellShortName                   java.lang.String                RO
        [...]
        ```
    """
    ...


def attributes(mbean_name: str, attribute_name: Optional[str] = None, /) -> str:
    """Use the `attributes` command to view a summary of all the attributes of the MBean identified by `mbean_name`. 
    
    - If the `attribute_name` parameter is _omitted_, the command displays information about all the attributes, operations, 
        constructors, description, notifications, and classname of the specified MBean. 
    
    - If the `attribute_name` parameter is _set_, the command will display only the information about
        the specified attribute.

    Args:
        mbean_name (str): The object name which identifies the desired MBean.
        attribute_name (str, optional): The attribute of interest. Defaults to None.

    Returns:
        str: Summary of all the attributes of the specified MBean

    Example:
        ```pycon
        >>> mbean = AdminControl.queryNames('type=Server,*').splitlines()[0]
        >>> print(Help.attributes(mbean))
        Attribute                       Type                            Access
        name                            java.lang.String                RO
        shortName                       java.lang.String                RO
        threadMonitorInterval           int                             RW
        threadMonitorThreshold          int                             RW
        threadMonitorAdjustmentThreshold  int                             RW
        [...]


        >>> print(Help.attributes(mbean, "pid"))
        Attribute                       Type                            Access
        pid                             java.lang.String                RO

        Description: Process id for the server process.
        ```
    """
    ...

def classname(mbean_name: RunningObjectName, /) -> str:
    """Use the `classname` command to get the class name associated with the MBean 
        identified by `mbean_name`.

    Args:
        mbean_name (RunningObjectName): The object name which identifies the desired MBean.

    Returns:
        str: The class name represented by the MBean name.

    Example:
        ```pycon
        >>> mbean = AdminControl.queryNames('type=Server,*').splitlines()[0]
        >>> print(Help.classname(mbean))
        javax.management.modelmbean.RequiredModelMBean
        ```
    """
    ...

def constructors(mbean_name: RunningObjectName, /) -> str:
    """Use the `constructors` command to get all the constructors associated with the MBean 
        identified by `mbean_name`.

    Args:
        mbean_name (RunningObjectName): The object name which identifies the desired MBean.

    Returns:
        str: The summary of all the constructors.
    
    Example:
        ```pycon
        >>> mbean = AdminControl.queryNames('type=Server,*').splitlines()[0]
        >>> print(Help.constructors(mbean))
        Constructors
        ```
    """
    ...

def description(mbean_name: RunningObjectName, /) -> str:
    """Use the `description` command to view a description of the MBean identified by `mbean_name`.

    Args:
        mbean_name (RunningObjectName): The object name which identifies the desired MBean.

    Returns:
        str: The description of the requested MBean.
    
    Example:
        ```pycon
        >>> mbean = AdminControl.queryNames('type=Server,*').splitlines()[0]
        >>> print(Help.description(mbean))
        Managed object for overall server process.
        ```
    """
    ...

def help() -> str:
    """Use the `help` command to view a summary of all the available methods for the `Help` object.

    Returns:
        str: Summary of all the available methods for the Help object.
    
    Example:
        ```pycon
        >>> print(Help.help())
        WASX7028I: The Help object has two purposes:
        [...]
        ```
    """
    ...

def message(message_id: str, /) -> str:
    """Use the `message` command to view information for a message ID.

    Args:
        message_id (str): The desired message ID.

    Returns:
        str: A description for the provided message ID.

    Example:
        ```pycon
        >>> print(Help.message('CNTR0005W'))
        Explanation: The container was unable to passivate an enterprise bean due to exception {2} 
        User action: Take action based upon message in exception {2}
        ```
    
    Question: More testing needed
        I **couldn't** properly **test this command** in my test environment since it kept raising an Exception.
    """
    ...

def notifications(mbean_name: RunningObjectName, /) -> str:
    """Use the `notifications` command to view a summary of all the notifications associated with the MBean 
        identified by `mbean_name`.

    Args:
        mbean_name (RunningObjectName): The object name which identifies the desired MBean.

    Returns:
        str: A **multiline** string containing all the MBean notifications.
    
    Example:
        ```pycon
        >>> mbean = AdminControl.queryNames('type=Server,*').splitlines()[0]
        >>> print(Help.notifications(mbean))
        Notifications
        j2ee.state.starting
        j2ee.state.running
        j2ee.state.stopping
        j2ee.state.stopped
        j2ee.state.failed
        j2ee.attribute.changed
        jmx.attribute.changed
        ```
    """
    ...

def operations(mbean_name: RunningObjectName, operation_name: Optional[str] = None, /):
    """Use the `operations` command to view a summary of all the operations associated with the MBean 
        identified by `mbean_name`.
        
    - If the `operation_name` parameter is set, it will be displayed only the signature of the 
        requested operation.

    Args:
        mbean_name (RunningObjectName): The object name which identifies the desired MBean.
        operation_name (str, optional): The operation of interest. Defaults to None.
    
    Example:
        - Get a list of all the available operations on the provided MBean:

        ```pycon
        >>> mbean = AdminControl.queryNames('type=Server,*').splitlines()[0]
        >>> print(Help.operations(mbean))
        Operation
        java.lang.String getName()
        java.lang.String getShortName()
        int getThreadMonitorInterval()
        void setThreadMonitorInterval(int)
        int getThreadMonitorThreshold()
        void setThreadMonitorThreshold(int)
        int getThreadMonitorAdjustmentThreshold()
        void setThreadMonitorAdjustmentThreshold(int)
        String dumpThreadMonitorHungThreads()
        java.lang.String getPid()
        java.lang.String getCellName()
        java.lang.String getCellShortName()
        ```

        - Get help on a specific operation:
        
        ```pycon
        >>> mbean = AdminControl.queryNames('type=Server,*').splitlines()[0]
        >>> print(Help.operations(mbean, "stop"))
        void stop()

        Description: Stop the server process.

        Parameters:

        -------------------------------------------------------

        void stop(java.lang.Boolean, java.lang.Integer)

        Description: Stop the server process and callback.

        Parameters:

        Type  java.lang.Boolean
        Name  callback
        Description  perform callback to requester.

        Type  java.lang.Integer
        Name  port
        Description  port number for callback.

        -------------------------------------------------------

        void stop(java.lang.String, java.lang.Integer)

        Description: Stop the server process and callback to a host and port.

        Parameters:

        Type  java.lang.String
        Name  host
        Description  host for callback.

        Type  java.lang.Integer
        Name  port
        Description  port number for callback.

        -------------------------------------------------------
        ```
    """
    ...
