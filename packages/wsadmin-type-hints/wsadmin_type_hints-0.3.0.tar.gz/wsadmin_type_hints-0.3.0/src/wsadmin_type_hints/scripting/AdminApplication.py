""" The AdminApplication script library provides script
        procedures that configure, administer, and deploy applications.

        The Adminapplication script library provides the following script procedures.
        To display detailed information about each script procedure, use the help command
        for the AdminApplication script library, specifying the name of the script of interest
        as an argument.
"""

from typing import Any


# Group 1: Install and uninstall applications

def installAppModulesToDiffServersWithPatternMatching(*args: Any) -> Any:
    """ Install application modules to different application servers using Java pattern matching """
    ...
    
def installAppModulesToDiffServersWithMapModulesToServersOption(*args: Any) -> Any:
    """ Install application modules to different application servers with MapModulesToServers option for the AdminApp object. """
    ...
    
def installAppModulesToMultiServersWithPatternMatching(*args: Any) -> Any:
    """ Install application modules to multiple application servers using Java pattern matching. """
    ...
    
def installAppModulesToSameServerWithPatternMatching(*args: Any) -> Any:
    """ Install application modules to the same application server using Java pattern matching. """
    ...
    
def installAppModulesToSameServerWithMapModulesToServersOption(*args: Any) -> Any:
    """ Install application modules to the same application server using the MapModulesToServers option for the AdminApp object. """
    ...
    
def installAppWithClusterOption(*args: Any) -> Any:
    """ Install application to a cluster using the cluster option for the AdminApp object. """
    ...
    
def installAppWithDefaultBindingOption(*args: Any) -> Any:
    """ Install application using the default binding options. """
    ...
    
def installAppWithDeployEjbOptions(*args: Any) -> Any:
    """ Install application using the deployejb option for the AdminApp object. """
    ...
    
def installAppWithNodeAndServerOptions(*args: Any) -> Any:
    """ Install application using the node and server options for the AdminApp object. """
    ...
    
def installAppWithTargetOption(*args: Any) -> Any:
    """ Install application using the target option for the AdminApp object. """
    ...
    
def installAppWithVariousTasksAndNonTasksOptions(*args: Any) -> Any:
    """ Install application using different deployed tasks. """
    ...
    
def installWarFile(*args: Any) -> Any:
    """ Install a Web archive (WAR) file. """
    ...
    
def uninstallApplication(*args: Any) -> Any:
    """ Uninstall application. """
    ...
    
# Group 2: Queries application configurations

def checkIfAppExists(*args: Any) -> Any:
    """ Display whether the application exists. """
    ...
    
def getAppDeployedNodes(*args: Any) -> Any:
    """ Display the nodes on which the application is deployed. """
    ...
    
def getAppDeploymentTarget(*args: Any) -> Any:
    """ Display the deployment target for the application. """
    ...
    
def getTaskInfoForAnApp(*args: Any) -> Any:
    """ Display detailed task information for a specific install task. """
    ...
    
def help(*args: Any) -> Any:
    """ Provides general help information for the AdminApplication script library. """
    ...
    
def listApplications(*args: Any) -> Any:
    """ Display each deployed application in your configuration. """
    ...
    
def listApplicationsWithTarget(*args: Any) -> Any:
    """ Display each deployed application for the deployment target. """
    ...
    
def listModulesInAnApp(*args: Any) -> Any:
    """ Display each application module in the deployed application. """
    ...
    
# Group 3: Update applications

def addPartialAppToAnAppWithUpdateCommand(*args: Any) -> Any:
    """ Update a partial application to a deployed application. """
    ...
    
def addSingleFileToAnAppWithUpdateCommand(*args: Any) -> Any:
    """ Add a single file to a deployed application. """
    ...
    
def addSingleModuleFileToAnAppWithUpdateCommand(*args: Any) -> Any:
    """ Add a single module file to a deployed application. """
    ...
    
def addUpdateSingleModuleFileToAnAppWithUpdateCommand(*args: Any) -> Any:
    """ Add and updates a single module file to a deployed application. """
    ...
    
def deletePartialAppToAnAppWithUpdateCommand(*args: Any) -> Any:
    """ Delete a partial application from a deployed application. """
    ...
    
def deleteSingleFileToAnAppWithUpdateCommand(*args: Any) -> Any:
    """ Delete a single file in a deployed application. """
    ...
    
def deleteSingleModuleFileToAnAppWithUpdateCommand(*args: Any) -> Any:
    """ Delete a single module file from a deployed application. """
    ...
    
def updateApplicationUsingDefaultMerge(*args: Any) -> Any:
    """ Update application using default merging """
    ...
    
def updateApplicationWithUpdateIgnoreNewOption(*args: Any) -> Any:
    """ Update application using the update.ignore.new option for the AdminApp object. """
    ...
    
def updateApplicationWithUpdateIgnoreOldOption(*args: Any) -> Any:
    """ Update application using the update.ignore.old option for the AdminApp objects. """
    ...
    
def updateEntireAppToAnAppWithUpdateCommand(*args: Any) -> Any:
    """ Update an entire application to a deployed application. """
    ...
    
def updatePartialAppToAnAppWithUpdateCommand(*args: Any) -> Any:
    """ Update a partial application to a deployed application. """
    ...
    
def updateSingleFileToAnAppWithUpdateCommand(*args: Any) -> Any:
    """ Update a single file to a deployed application. """
    ...
    
def updateSingleModuleFileToAnAppWithUpdateCommand(*args: Any) -> Any:
    """ Update a single module file to a deployed application. """
    ...
    
# Group 4: Export applications

def exportAllApplicationsToDir(*args: Any) -> Any:
    """ Export  each application in your configuration to a specific directory. """
    ...
    
def exportAnAppDDLToDir(*args: Any) -> Any:
    """ Export  application data definition language (DDL) to a specific directory. """
    ...
    
def exportAnAppToFile(*args: Any) -> Any:
    """ Export  application to a specific file. """
    ...
    
# Group 5: Configure application deployment

def configureApplicationLoading(*args: Any) -> Any:
    """ Configure the application loading for the deployed targets. """
    ...
    
def configureClassLoaderLoadingModeForAnApplication(*args: Any) -> Any:
    """ Configure class loader loading mode for application deployment. """
    ...
    
def configureClassLoaderPolicyForAnApplication(*args: Any) -> Any:
    """ Configure a class loader policy for application deployment. """
    ...
    
def configureConnectorModulesOfAnApplication(*args: Any) -> Any:
    """ Configure connector module attributes for application deployment. """
    ...
    
def configureEJBModulesOfAnApplication(*args: Any) -> Any:
    """ Configure enterprise bean (EJB) module settings for application deployment. """
    ...
    
def configureLibraryReferenceForAnApplication(*args: Any) -> Any:
    """ Configure shared library reference for the application. """
    ...
    
def configureSessionManagementForAnApplication(*args: Any) -> Any:
    """ Configure session management settings for application deployment. """
    ...
    
def configureStartingWeightForAnApplication(*args: Any) -> Any:
    """ Configure starting weight settings for application deployment. """
    ...
    
def configureWebModulesOfAnApplication(*args: Any) -> Any:
    """ Configure Web modules settings for application deployment. """
    ...
    
# Group 6: Administer applications

def startApplicationOnAllDeployedTargets(*args: Any) -> Any:
    """ Start an application on each deployed target. """
    ...
    
def startApplicationOnCluster(*args: Any) -> Any:
    """ Start an application on a cluster. """
    ...
    
def startApplicationOnSingleServer(*args: Any) -> Any:
    """ Start an application on a single server. """
    ...
    
def stopApplicationOnAllDeployedTargets(*args: Any) -> Any:
    """ Stop an application on each deployed target. """
    ...
    
def stopApplicationOnCluster(*args: Any) -> Any:
    """ Stop an application on a cluster. """
    ...
    
def stopApplicationOnSingleServer(*args: Any) -> Any:
    """ Stop an application on single server """
    ...
    