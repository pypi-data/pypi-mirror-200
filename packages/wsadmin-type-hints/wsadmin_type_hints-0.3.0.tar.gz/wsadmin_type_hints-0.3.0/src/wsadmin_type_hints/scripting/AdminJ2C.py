""" The AdminJ2C script library provides script
    procedures that configure and query J2EE Connector (J2C) resource settings.

    The AdminJ2C script library provides the following script procedures.
    To display detailed information about each procedure, use the help command
    for the AdminJ2C script library, specifying the name of the script of interest
    as an argument.
    The script procedures that take the optional arguments can be specified
    with a list or string format.

    For example, `otherAttributeList` can be specified as:
    
    - `"description=my new resource, isolatedClassLoader=true"`
    - `[["description", "my new resource"], ["isolatedClassLoader", "true"]]`
"""
from typing import Any


def createJ2CActivationSpec(*args: Any) -> Any:
    """ Create a J2C activation specification in your configuration. """
    ...

def createJ2CAdminObject(*args: Any) -> Any:
    """ Create a J2C administrative object in your configuration. """
    ...

def createJ2CConnectionFactory(*args: Any) -> Any:
    """ Create a new J2C connection factory in your configuration. """
    ...

def installJ2CResourceAdapter(*args: Any) -> Any:
    """ Install a J2C resource adapter in your configuration. """
    ...

def listAdminObjectInterfaces(*args: Any) -> Any:
    """ Display a list of the administrative object interfaces for the J2C resource adapter of interest. """
    ...

def listConnectionFactoryInterfaces(*args: Any) -> Any:
    """ Display a list of the connection factory interfaces for the J2C resource adapter of interest. """
    ...

def listMessageListenerTypes(*args: Any) -> Any:
    """ Display a list of the message listener types for the J2C resource adapter of interest. """
    ...

def listJ2CActivationSpecs(*args: Any) -> Any:
    """ Display a list of the J2C activation specifications in your J2C configuration. """
    ...

def listJ2CAdminObjects(*args: Any) -> Any:
    """ Display a list of the administrative objects in your J2C configuration. """
    ...

def listJ2CConnectionFactories(*args: Any) -> Any:
    """ Display a list of J2C connection factories in your J2C configuration. """
    ...

def listJ2CResourceAdapters(*args: Any) -> Any:
    """ Display a list of the J2C connection factories in your J2C configuration. """
    ...

def help(*args: Any) -> Any:
    """ Provide AdminJ2C script library online help. """
    ...
