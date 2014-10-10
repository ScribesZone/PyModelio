# -*- coding: utf-8 -*-

"""
======================================================================================
                Startup of ModelioScribes Framework
======================================================================================

Give access to the ModelioScribe framework.

Modelio provides a lot of features for the development of plugin in java but no
facilities is given for developing in python beyond simple monolithic macro
development.

This very small framework supports the following features:

- support for code development/execution outside modelio workspace macro directory.
- modular development of python modules with reloading features in development mode.
- inclusion of regular python and java libraries thanks to python/java path management.
- support for directory management allowing to develop code independently from execution.
- finding the ModelioScribes directory where more features can be installed.
- extension of the python path and java path to reuse existing python or java libraries.

The framework provides 3 classes:

- PyModelioEnv
- Scribe
- PluginExecution 



The parameter is one of the following key:

- "TMP"                         : temporary directory
- "USER_HOME"                   : home directory of user
- "USER_MODELIO"                : directory .modelio in user home
- "USER_MODELIO_MACROS"         : directory where user macros are stored
- "MODELIO_WORKSPACE"           : workspace directory of modelio
- "MODELIO_WORKSPACE_MACROS"    : macros directory in workspace
- "MODELIO_VERSION_SIMPLE"      : modelio version like "3.2"
- "MODELIO_VERSION_FULL"        : modelio version like "3.2.02.0"
- "PYMODELIO_MAIN"              : ModelioScribes distribution directory
- "PYMODELIO_LOCAL"             : local directory for the user to add features
- "PYMODELIO_PATHS_FILE"        : name of the .modelio/pymodelio_paths.py
- "<ROOT>_LIBS_PYTHON"          : directory containing external python libs
- "<ROOT>_LIBS_JAVA"            : directory containing external java libs
- "<ROOT>_COMMONS"              : commons directory
- "<ROOT>_PLUGINS"              : directory plugins
- "<ROOT>_PLUGINS_NAMES"        : name of subdirectories in the plugin directories
- "PLUGINS_MAP"               : list of names of all scribes found
- "PYTHON_PATH_ADDED_DIRS"     : list of directories added to the py path

"""

import os
import sys
# noinspection PyUnresolvedReferences
import java.lang
# noinspection PyUnresolvedReferences
import java.net
# noinspection PyUnresolvedReferences
from org.modelio.api.modelio import Modelio
from pymodelio.core.plugins import Plugin


class PyModelioEnv(object):
    """ 
    Global Scribe environment, singleton made available as PYMODELIO_ENV top level variable.
  
    Once executed there will be only one instance for this class. It is created
    at the beginning when any macro (using the framework) is launched for the first time. 
    This environment is then available to later as "SCRIBE_ENV". 
    (see the end of this file). 
    """

    def __init__(self, initialPythonPath, pyModelioMain, pyModelioLocal, withModelio=True):
        """
        Create the PyModelio environment with a bunch of constants towards relevant directories
        and with correct values for Python & Java paths.
        """
        self.INITIAL_PYTHON_PATH = initialPythonPath    #: Initial python path
        self.PYMODELIO_MAIN = pyModelioMain             #: "PyModelio" Directory
        # The following value will be processed in this class.
        # It can have None currently but then a default place will be given.
        self.PYMODELIO_LOCAL = pyModelioLocal           #: "PyModelioLocal" Directory
        self.WITH_MODELIO = withModelio                 #: Is the execution in the context of modelio?
        # noinspection PyUnresolvedReferences
        if self.WITH_MODELIO:
            self.INITIAL_JAVA_CLASS_LOADER = sys.getClassLoader()   #! Initial class loader
        else:
            self.INITIAL_JAVA_CLASS_LOADER = None
        # Many other constants are defined. See documentation
        self.restart()

    def restart(self):
        """ 
        Define constants and set the java and python paths according to the current environment.
        
        Use this method if new directories, plugins, etc. are added.
        Otherwise these changes will not be taken into consideration.
        """
        self.PYTHON_PATH_DIRECTORIES = []               # will be updated by some methods below
        self.__registerSystemDirectories()              # define constants
        if self.WITH_MODELIO:
            self.__registerModelioProperties()              # define constants
        self.__registerUserDirectoriesToProperties()    # define constants
        self.__managePyModelioLocal()                   # constants + directory structure
        self.__registerRootsCommonsAndLibs()            # define constants
        self.__registerPlugins()
        # add common modules and python libraries to the path
        dirsAddedToPath = self._addAllModulesAndPythonLibraryDirectoriesToPythonPath()
        # FIXME:! self.PYTHON_PATH_ADDED_DIRS = user_dirsAddedToPath

        self.scribe = None      # set in scribe. Is it really useful?
        print ("ModelioScribes framework initialized from %s" % self.PYMODELIO_MAIN)


    def fromRoot(self,root,pathElements=()):
        """
        Return a path to a file or a directory relative to the PyModelio *root* directory,
        *root* being either "LOCAL" or "MAIN".

        If nothing is provided then return the *root* directory.
        :param "MAIN"|"ROOT" root: the root directory used as a reference.
        :param [str] patheElements: a list (or tuple) of directory/file names.
            Only only the last element could be file.
        """
        if root=="MAIN":
            root = self.PYMODELIO_MAIN
        elif root=="LOCAL":
            root = self.PYMODELIO_LOCAL
        else:
            raise ValueError("%s given. Must be either MAIN or LOCAL"%root)
        return os.path.join(* [root]+pathElements)

    def fromMain(self,pathElements=()):
        """ 
        Return a path to a file or a directory relative to the PyModelio main directory.
        
        If nothing is provided then return the main directory.
        """
        return self.fromRoot("MAIN",pathElements)
        
    def fromLocal(self,pathElements=()):
        """
        Return a path to a file or a directory relative to the PyModelio local directory.

        If nothing is provided then return the local directory.
        """
        return self.fromRoot("LOCAL",pathElements)


    def loadPythonModule(self,moduleNames,reload=False):
        """ 
        Load/reload a (list of) module(s)
        
        :param str|[str] moduleNames: either a string or a list of strings corresponding to module names.
        :param boolean reload: reload the module(s) if true.
            This parameter is useful for debugging purposes.
        """
        if  isinstance(moduleNames, basestring):
            moduleNames = [ moduleNames ]
        for moduleName in moduleNames:
            notLoaded = moduleName not in sys.modules
            if reload or notLoaded:
                try: 
                    del sys.modules[moduleName]
                    exec( "del "+moduleName )
                except:pass
            exec( "import "+moduleName )

    def setJavaPath(self,pathEntries,baseDirectory=None):
        urls = []
        for pe in pathEntries:
            urls.append(java.net.URL("file:"+pe))
        sys.setClassLoader(java.net.URLClassLoader(urls,self.INITIAL_JAVA_CLASS_LOADER))
        
    def restoreJavaPath(self):
        sys.setClassLoader(self.INITIAL_JAVA_CLASS_LOADER)
    # def __str__(self):
    #    sep = java.lang.System.getProperty("path.separator")
    #    urls = sys.getClassLoader().getURLs()
    #    return sep.join([url.getPath() for url in urls])    
        

    #-----------------------------------------------------------------
    # Access to modelio changing variables
    #-----------------------------------------------------------------
        
    def getSelectedElements(self):
        """  Return current selected elements of modelio. """
        global selectedElements
        return selectedElements
        
    def getModelingSession(self):
        global modelingSession
        return modelingSession     



        
    #====================================================================
    #                          Class Implementation
    #====================================================================
    
    # use to build the mapping between constants and paths
    # keep it to make evolution of mapping possible
    _STRUCTURE_MAPPING = {
        "COMMONS": "commons",
        "LIBS_PYTHON": "libs python",
        "LIBS_JAVA": "libs java",
        }
        
    _IN_PYTHON_PATH = ["COMMONS","LIBS_PYTHON"]
    

        
        
    
    def __registerSystemDirectories(self):
        """ add system directories to properties 
        :rtype : void
        """
        import tempfile
        self.TMP = tempfile.gettempdir()
    
    def __registerModelioProperties(self):
        context = Modelio.getInstance().getContext()
        workspaceDir = context.getWorkspacePath().toString()
        self.MODELIO_WORKSPACE = workspaceDir
        self.MODELIO_WORKSPACE_MACROS = os.path.join(workspaceDir,'macros')
        version = context.getVersion().toString()
        self.MODELIO_VERSION_FULL= version
        self.MODELIO_VERSION_SIMPLE = ".".join(version.split(".")[0:2])
        
    def __registerUserDirectoriesToProperties(self):
        self.USER_HOME = os.path.expanduser("~")            
        userModelio = os.path.join(self.USER_HOME,".modelio")
        self.USER_MODELIO = userModelio
        if self.WITH_MODELIO:
            version = self.MODELIO_VERSION_SIMPLE
            self.USER_MODELIO_MACROS = \
        self.PYMODELIO_PATHS_FILE = \
            os.path.join(userModelio,"pymodelio_paths.py")

    def __managePyModelioLocal(self):
        """ Check if there is a local structure or create it otherwise """
        # check if there was a setting by the user in .modelio
        # otherwise use the directory .modelio/PyModelioLocal
        if self.PYMODELIO_LOCAL is None:
            # The user has not specified any value in its file
            # By default this will be a directory in in the .modelio directory
            self.PYMODELIO_LOCAL = os.path.join(self.USER_MODELIO,"PyModelioLocal")
        if not os.path.isdir(self.PYMODELIO_LOCAL):
            # There is no directory for the local structure
            # initialize it
            self.__initializePyModelioLocal()
        
    def __initializePyModelioLocal(self):
        """ Create an initial PyModelioLocal directory structure """
        os.mkdir(self.PYMODELIO_LOCAL)
        # TODO: copy the structure from an existing place
            
    def __registerRootsCommonsAndLibs(self):
        """
        Add directories following these patterns:

        - <ROOT>/commons
        - <ROOT>/libs/python
        - <ROOT>/libs/java
        :return:
        """
        for (key,spaced_path) in self._STRUCTURE_MAPPING.items():
            for root in ["MAIN", "LOCAL"]:
                constant = root+"_"+key
                # print "%s = %s(%s)" % (constant,spaced_path,spaced_path.split(" "))
                value = self.fromRoot(root,spaced_path.split(" "))
                setattr(self,constant,value)
                if key in self._IN_PYTHON_PATH:
                    print "PATH ",
                print "%s ROOTS %s = %s" % (key,constant,value)


    def __registerPlugins(self):
        """
        Add directories following these patterns to the path:

        - <ROOT>/plugins/<PLUGIN_NAME>/<PLUGIN_NAME>
        - <ROOT>/plugins/<PLUGIN_NAME>/libs/python
        - <ROOT>/plugins/<PLUGIN_NAME>/libs/java
        """
        # Add the directories in an order that make
        # that plugin defined locally will override
        # plugins with the same name in the main root.
        for root in ["MAIN","LOCAL"]:  # DO NOT change this order!
            plugin_dir = root+os.sep+"plugins"
            setattr(self,root+"_PLUGINS",plugin_dir)
            if os.path.isdir(plugin_dir):
                plugin_names = os.listdir(plugin_dir)
            else:
                plugin_names = []
            setattr(self, root+"_PLUGINS_NAMES", plugin_names)

            for plugin_name in plugin_names:
                plugin = Plugin(self,root,plugin_name)

        raise Exception("Hello - directory has to be added to the path, check variables")
        # add these directory to python path
        for directory in directories:
            if os.path.isdir(directory):
                self.__addDirectoryToPythonPath(directory)
            else:
                raise Exception("%s is not a directory. Cannot add it to python path"%directory)



    #-----------------------------------------------------------------------
    #  Module Management and python library management.
    #-----------------------------------------------------------------------

    def __addDirectoryToPythonPath(self,directory):
        """ 
        Add the directory to the python path if it does not exist already.
        
        Check that the directory is valid. Otherwise a message is simply issued.
        Returns a boolean indicating if this was a success or not but no
        exception is raised.
        """
        if not directory in sys.path:
            if os.path.isdir(directory):
                sys.path.append(directory)
        else:
            print \
               "WARNING: %s was notadded to python path. Not a valid directory!"%directory
    





    #TODO: use this in reading configuration settings
    def isGlobalConstant(self,name):
        import re
        return re.match(r"^[A-Z][A-Z_]*$",name) is not None

    def getGlobalConstants(self,entity):
        return [(name,value) for (name,value) in entity.__dict__.items() if self.isGlobalConstant(name)]







