""" The AdminAuthorizations script library provides script
        procedures that configure security authorization groups.

        The AdminAuthorizations script library provides the following script procedures.
        To display detailed information about each script procedure, use the help command for
        the AdminAuthorizations script library, specifying the name of the script of interest
        as an argument.
"""
from typing import Any

    
def addResourceToAuthorizationGroup(*args: Any) -> Any:
    """ Add a resource to an existing authorization group. """
    ...

def createAuthorizationGroup(*args: Any) -> Any:
    """ Create a new authorization group. """
    ...

def deleteAuthorizationGroup(*args: Any) -> Any:
    """ Delete an existing authorization group. """
    ...

def help(*args: Any) -> Any:
    """ Display the script procedures that the AdminClusterManagement script library supports. 
    
        To display detailed help for a specific script, specify the name of the script of interest
    """
    ...

def listAuthorizationGroups(*args: Any) -> Any:
    """ List the existing authorization groups in your configuration. """
    ...

def listAuthorizationGroupsForGroupID(*args: Any) -> Any:
    """ List authorization groups to which a specific group has access. """
    ...

def listAuthorizationGroupsForUserID(*args: Any) -> Any:
    """ List authorization groups to which a specific user has access. """
    ...

def listAuthorizationGroupsOfResource(*args: Any) -> Any:
    """ List each authorization group to which a specific resource is mapped. """
    ...

def listGroupIDsOfAuthorizationGroup(*args: Any) -> Any:
    """ Display the group IDs and access level that are associated with a specific authorization group. """
    ...

def listResourcesForGroupID(*args: Any) -> Any:
    """ Display the resources that a specific group ID can access. """
    ...

def listResourcesForUserID(*args: Any) -> Any:
    """ Display the resources that a specific user ID can access. """
    ...

def listResourcesOfAuthorizationGroup(*args: Any) -> Any:
    """ Display the resources that are associated with a specific authorization group. """
    ...

def listUserIDsOfAuthorizationGroup(*args: Any) -> Any:
    """ Display the user IDs and access level that are associated with a specific authorization group. """
    ...

def mapGroupsToAdminRole(*args: Any) -> Any:
    """ Map group IDs to one or more administrative roles in the authorization group. 
    
        The name of the authorization group that you provide determines the authorization table.
        The group ID can be a short name or fully qualified domain name in case LDAP user registry is used.
    """
    ...

def mapUsersToAdminRole(*args: Any) -> Any:
    """ Map user IDs to one or more administrative roles in the authorization group. 
    
        The name of the authorization group that you provide determines the authorization table.
        The user ID can be a short name or fully qualified domain name in case LDAP user registry is used.
    """
    ...

def removeGroupFromAllAdminRoles(*args: Any) -> Any:
    """ Remove a specific group from an administrative role in each authorization group in your configuration. """
    ...

def removeGroupsFromAdminRole(*args: Any) -> Any:
    """ Remove specific groups from an administrative role in the authorization group of interest. """
    ...

def removeResourceFromAuthorizationGroup(*args: Any) -> Any:
    """ Remove a specific resource from the authorization group of interest. """
    ...

def removeUsersFromAdminRole(*args: Any) -> Any:
    """ Remove specific users from an administrative role in the authorization group of interest. """
    ...

def removeUserFromAllAdminRoles(*args: Any) -> Any:
    """ Remove a specific user from an administrative role in each authorization group in your configuration. """
    ...
