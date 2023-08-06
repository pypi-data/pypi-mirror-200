""" The `wsadmin` Jython **scripting library** provides a set of procedures to **automate** the
    most **common** application server **administration operations**.


    !!! Info
        ### Library location
        The script library code is located in the
        `${APP_SERVER_ROOT}/scriptLibraries` directory. Within this directory, the
        scripts are organized into **subdirectories** according to functionality.
        
        For example, the `${APP_SERVER_ROOT}/scriptLibraries/application/V70`
        subdirectory contains procedures that perform application management tasks
        that are applicable to Websphere Application Server v7.0 and later.

        ### Add scripts to the library
        To automatically load your own Jython scripts (`*.py`) when the `wsadmin` tool
        starts, create a new **subdirectory**, and save existing automation scripts in
        the `${APP_SERVER_ROOT}/scriptLibraries` directory. 
        
        Each script library name must be **unique** and cannot be duplicated.

    The scripting library consists of the following automation scripts:

    - [`AdminApplication`](/reference/wsadmin_type_hints/AdminApplication/): Use it to install, uninstall, and update your **applications** with various options.
    - [`AdminAuthorizations`](/reference/wsadmin_type_hints/AdminAuthorizations/): Use it to configure **authorization groups**.
    - [`AdminBLA`](/reference/wsadmin_type_hints/AdminBLA/): Use it to configure, administer and deploy **Business Level Applications** (BLA).
    - [`AdminClusterManagement`](/reference/wsadmin_type_hints/AdminClusterManagement/): Use it to manage server **clusters**.
    - [`AdminJ2C`](/reference/wsadmin_type_hints/AdminJ2C/): Use it to create and configure Java 2 Connector (**J2C**) resource adapters.
    - [`AdminJDBC`](/reference/wsadmin_type_hints/AdminJDBC/): Use it to manage data sources and Java Database Connectivity (**JDBC**) providers.
    - [`AdminJMS`](/reference/wsadmin_type_hints/AdminJMS/): Use it to configure and manage your Java Messaging Service (**JMS**) configurations.
    - [`AdminLibHelp`](/reference/wsadmin_type_hints/AdminLibHelp/): Use it to list each available script library, display information for specific script libraries, and to display information for specific script procedures.
    - [`AdminNodeGroupManagement`](/reference/wsadmin_type_hints/AdminNodeGroupManagement/): Use it to manage **node groups**.
    - [`AdminNodeManagement`](/reference/wsadmin_type_hints/AdminNodeManagement/): Use it to manage **Nodes**.
    - [`AdminResources`](/reference/wsadmin_type_hints/AdminResources/): Use it to configure mail, URL, and **resource** settings.
    - [`AdminServerManagement`](/reference/wsadmin_type_hints/AdminServerManagement/): Use it to configure classloaders, Java™ virtual machine (JVM) settings, Enterprise JavaBeans (EJB) containers, performance monitoring, dynamic cache, and so on.
    - [`AdminUtilities`](/reference/wsadmin_type_hints/AdminUtilities/): Use it to configure trace, debugging, logs, and performance monitoring.

    For more info see the [official documentation](https://www.ibm.com/docs/en/was-zos/8.5.5?topic=sasew-using-script-library-automate-application-serving-environment-using-wsadmin-scripting).
"""

__all__ = [
    "AdminApplication",
    "AdminAuthorizations",
    "AdminBLA",
    "AdminClusterManagement",
    "AdminJ2C",
    "AdminJDBC",
    "AdminJMS",
    "AdminLibHelp",
    "AdminNodeGroupManagement",
    "AdminNodeManagement",
    "AdminResources",
    "AdminServerManagement",
    "AdminUtilities",
]

# Additional try/except to ensure that even if installed in a real environment,
# the original modules do not get overwritten.
try:
    (AdminApplication) # pyright: ignore[reportUnboundVariable, reportUnusedExpression]
except NameError:
    from . import AdminApplication
    from . import AdminAuthorizations
    from . import AdminBLA
    from . import AdminClusterManagement
    from . import AdminJ2C
    from . import AdminJDBC
    from . import AdminJMS
    from . import AdminNodeGroupManagement
    from . import AdminNodeManagement
    from . import AdminResources
    from . import AdminServerManagement
    from . import AdminUtilities

    # -----              Helper module              -----
    from . import AdminLibHelp