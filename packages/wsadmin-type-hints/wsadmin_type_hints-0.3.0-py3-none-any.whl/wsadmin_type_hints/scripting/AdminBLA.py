""" The AdminBLA script library provides the script procedures that configure,
    administer and deploy business level applications.

    The AdminBLA script library provides the following script procedures. To
    display detailed information for each script procedures, use the help
    command for the AdminBLA script library, specifying the name of the script
    of interest as an argument.
"""

from typing import Any


def addCompUnit(*args: Any) -> Any:
    """ Add a composition unit to a business level application. """
    ...

def createEmptyBLA(*args: Any) -> Any:
    """ Create an empty business level application. """
    ...

def deleteAsset(*args: Any) -> Any:
    """ Delete a registered asset from WebSphere configuration repository. """
    ...

def deleteBLA(*args: Any) -> Any:
    """ Delete a business level application. """
    ...

def deleteCompUnit(*args: Any) -> Any:
    """ Delete a composition unit in a business level application. """
    ...

def editAsset(*args: Any) -> Any:
    """ Edit an asset metadata. """
    ...

def editCompUnit(*args: Any) -> Any:
    """ Edit a composition unit in a business level application. """
    ...

def exportAsset(*args: Any) -> Any:
    """ Export a registered asset to a file. """
    ...

def help(*args: Any) -> Any:
    """ Provide AdminBLA script library online help. """
    ...

def importAsset(*args: Any) -> Any:
    """ Import and register an asset to WebSphere management domain. """
    ...

def listAssets(*args: Any) -> Any:
    """ List registered assets in a cell. """
    ...

def listBLAs(*args: Any) -> Any:
    """ List business level applications in a cell. """
    ...

def listCompUnits(*args: Any) -> Any:
    """ List composition units in a business level application. """
    ...

def startBLA(*args: Any) -> Any:
    """ Start a business level application. """
    ...

def stopBLA(*args: Any) -> Any:
    """ Stop a business level application. """
    ...

def viewAsset(*args: Any) -> Any:
    """ View a registered asset. """
    ...

def viewCompUnit(*args: Any) -> Any:
    """ View a composition unit in a business level application. """
    ...
