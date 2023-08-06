class ConfigurationObjectName(str):
    """Object name representing an entry in the configuration.

    !!! Example
        ``` 
        Db2JdbcDriver(cells/testcell/nodes/testnode|resources.xml#JDBCProvider_1)
        ```
    """
    ...

class ConfigurationContainmentPath(str):
    """Represents the path of a resource in the configuration.

    Warning:
        The containment path MUST contain the **correct hierarchical order**.

        For example, if you specify `/Server:server1/Node:node/` as the containment path, 
        you will not receive a valid configuration ID because `Node` is a parent 
        of `Server` and comes before Server in the hierarchy.

    !!! Example
        ``` 
        /Cell:testcell/Node:testNode/JDBCProvider:Db2JdbcDriver/
        ```
    """
    ...

class RunningObjectName(str):
    """This `ObjectName` uniquely identifies running objects and is in the 
        form `[domainName]:property=value[,property=value]*`.
    
    The `RunningObjectName` class consists of the following elements:

    - The domain name `"WebSphere"`.
    - Several key properties, for example:
        - `name` represents the display name of the particular object, for example, `MyServer`.
        - `type` indicates the type of object that is accessible through the MBean, for example, `ApplicationServer`, and EJBContainer.
        - `cell` represents the name of the cell on which the object runs.
        - `node` represents the name of the node on which the object runs.
        - `process` represents the name of the server process in which the object runs.
        - `mbeanIdentifier` correlates the MBean instance with corresponding configuration data.
    
    For more info see the [official documentation](https://www.ibm.com/docs/en/was-nd/8.5.5?topic=administration-objectname-attribute-attributelist-classes-using-wsadmin-scripting).

    !!! Example
        ```
        WebSphere:cell=MyCell,name=TraceService,mbeanIdentifier=TraceService,type=TraceService,node=MyNode,process=server1
        ```
    """
    ...

class RunningObjectTemplate(str):
    """This `ObjectName` is a string containing a segment of the object name to be matched. 
    The template has the same format as an object name with the following pattern: `[domainName]:property=value[,property=value]*`.
    
    For more information, see Object name, Attribute, Attribute list.
    
    You can use the asterisk (`*`) at the end as a **wildcard character**, so that you do not have to specify the entire set of key properties.

    For more info see the [official documentation](https://www.ibm.com/docs/en/was-nd/8.5.5?topic=administration-objectname-attribute-attributelist-classes-using-wsadmin-scripting).

    Note:
        The only difference between a `template` and an `object name` is that the template can be partial and use wildcards.
        It can then be used to retrieve a complete Object Name.

    !!! Example
        ```
        WebSphere:name="My Server",type=ApplicationServer,node=n1,*
        ```
    """
    ...
