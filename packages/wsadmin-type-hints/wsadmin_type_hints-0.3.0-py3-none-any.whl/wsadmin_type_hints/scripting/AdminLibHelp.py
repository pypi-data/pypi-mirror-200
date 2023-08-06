""" The AdminLibHelp provides general help information for the
    Jython script libraries for the wsadmin tool.

    Each script library contains multiple script procedures that perform
    various administration functions. To display detailed information
    for a specific script library, use the help option for the
    AdminLibHelp object, specifying the script library of interest as
    an argument. For example, AdminLibHelp.help("AdminApplication")
    returns the detailed information for the AdminApplication script
    library.
"""


from typing import Any


def AdminApplication(*args: Any) -> Any:
    """ Provide script procedures that configure, administer and deploy applications. """
    ...

def AdminAuthorizations(*args: Any) -> Any:
    """ Provide script procedures that configure security authorization groups. """
    ...


def AdminBLA(*args: Any) -> Any:
    """ Provide script procedures that configure, administer and deploy business level applications. """
    ...

def AdminClusterManagement(*args: Any) -> Any:
    """ Provide script procedures that configure and administer server clusters. """
    ...

def AdminJ2C(*args: Any) -> Any:
    """ Provide script procedures that configure and query J2EE Connector (J2C) resource settings. """
    ...

def AdminJDBC(*args: Any) -> Any:
    """ Provide script procedures that configure and query Java Database Connectivity (JDBC) and data source settings. """
    ...

def AdminJMS(*args: Any) -> Any:
    """ Provide script procedures that configure and query Java Messaging Service (JMS) provider and resource setttings. """
    ...

def AdminLibHelp(*args: Any) -> Any:
    """ Provide general help information for the the script library. """
    ...

def AdminNodeGroupManagement(*args: Any) -> Any:
    """ Provide script procedures that configure and administer node group settings. """
    ...

def AdminNodeManagement(*args: Any) -> Any:
    """ Provide script procedures that configure and administer node settings. """
    ...

def AdminResources(*args: Any) -> Any:
    """ Provide script procedures that configure and administer mail, URL and resource provider settings. """
    ...

def AdminServerManagement(*args: Any) -> Any:
    """ Provide script procedures that configure, administer and query server settings. """
    ...

def AdminUtilities(*args: Any) -> Any:
    """ Provide script procedures that administer utilities settings. """
    ...

