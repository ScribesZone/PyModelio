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
- "MAIN_LIBS_PYTHON"            : directory containing external python libs
- "MAIN_LIBS_JAVA"              : directory containing external java libs
- "MAIN_COMMONS"                : commons directory
- "MAIN_PLUGINS"                : directory plugins
- "MAIN_PLUGINS_NAMES"
- "MAIN_<PLUGIN_NAME>
- "LOCAL_LIBS_PYTHON"           : external python libs for local environment
- "LOCAL_LIBS_JAVA"             : external java libs for local environment
- "LOCAL_COMMONS"               : directory containing external java libs
- "LOCAL_PLUGINS"               : local plugin directory
- "LOCAL_PLUGINS_NAMES"
- "PLUGIN_NAMES"               : list of names of all scribes found
- "PYTHON_PATH_ADDED_DIRS"      : list of directories added to the py path

"""

import os
import sys
import java.lang
import java.net
# noinspection PyUnresolvedReferences
import encodings   # needed to avoid failures when loading some modules
# noinspection PyUnresolvedReferences
import Modelio


class PyModelioEnv(object):
    """ 
    Global Scribe environment, singleton made available as PYMODELIO_ENV top level variable.
  
    Once executed there will be only one instance for this class. It is created
    at the beginning when any macro (using the framework) is launched for the first time. 
    This environment is then available to later as "SCRIBE_ENV". 
    (see the end of this file). 
    """
    
    ENV = None
    """this will be the only instance of PyModelioEnv"""

    def __init__(self):
        """ Create the PyModelio environment.
        
        """
        self.INITIAL_PYTHON_PATH       = sys.path
        self.INITIAL_JAVA_CLASS_LOADER = sys.getClassLoader()
        # Many other constants are defined. See documentation
        self.restart()

    def restart(self):
        """ 
        Define constants and set path based on current environment. 
        
        Use this method if new directories, plugins, etc. are added.
        Otherwise these changes will not be taken into consideration.
        """
        # noinspection PyGlobalUndefined
        global PYMODELIO_MAIN
        self.PYMODELIO_MAIN = PYMODELIO_MAIN
        self.__registerSystemDirectories()
        self.__registerModelioProperties()
        self.__registerUserDirectoriesToProperties()
        self.__managePyModelioLocal()
        self.__registerMainCommonsAndLibs()
        self.__registerPluginDirectories()
        # add common modules and python libraries to the path
        dirsAddedToPath = self._addAllModulesAndPythonLibraryDirectoriesToPythonPath()
        self.PYTHON_PATH_ADDED_DIRS = user_dirsAddedToPath
        
        
        self.scribe = None      # set in scribe. Is it really useful?
        print "ModelioScribes framework initialized from %s" % self.PYMODELIO_MAIN
    
    def fromMain(self,pathElements=[]):
        """ 
        Return a path to a file or a directory relative to the PyModelio main directory.
        
        If nothing is provided then return the main directory.
        """
        return self._from("MAIN",pathElements)
        
    def fromLocal(self,pathElements=[]):
        return self._from("LOCAL",pathElements)


    def loadPythonModule(self,moduleNames,reload=False):
        """ 
        Load/reload a (list of) module(s)
        
        Reload if the second parameter is true.
        - moduleNames is either a string or a list of string.
        - reload the module if the reload parameter is true.
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
        sys.setClassLoader(java.net.URLClassLoader(urls))
        
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
        "PLUGINS": "plugins", 
        }
        
    _IN_PYTHON_PATH = ["COMMONS","LIBS_PYTHON"]
    
    def _from(self,root_property,pathElements=[]):
        if root_property=="MAIN":
            root = self.PYMODELIO_MAIN
        elif root_property=="LOCAL":
            root = self.PYMODELIO_LOCAL
        else:
            raise ValueError("%s given. Must be either MAIN or LOCAL"%rootProperty)
        # print "----",root,pathElements
        return os.path.join(* [root]+pathElements)

        
        
    
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
        """

        :rtype : void
        """
        self.USER_HOME = os.path.expanduser("~")            
        userModelio = os.path.join(self.USER_HOME,".modelio")
        self.USER_MODELIO = userModelio
        version = self.MODELIO_VERSION_SIMPLE
        self.USER_MODELIO_MACROS = \
            os.path.join(userModelio,version,'macros')
        self.PYMODELIO_PATHS_FILE = \
            os.path.join(userModelio,"pymodelio_paths.py")

    def __managePyModelioLocal(self):
        global PYMODELIO_LOCAL
        """ Check if there is a local structure or create it otherwise """ 
        # check if there was a setting by the user in .modelio
        # otherwise use the directory .modelio/PyModelioLocal
        try:            
            self.PYMODELIO_LOCAL = PYMODELIO_LOCAL
        except:
            PYMODELIO_LOCAL = os.path.join(self.USER_MODELIO,"PyModelioLocal")
        if not os.path.isdir(self.PYMODELIO_LOCAL):
            # There is no directory for the local structure
            # initialize it
            self.__initializePyModelioLocal()
        
    def __initializePyModelioLocal(self):
        """ Create an initial PyModelioLocal directory structure """
        os.mkdir(self.PYMODELIO_LOCAL)
        # TODO: copy the structure from an existing place
            
    def __registerMainCommonsAndLibs(self):
        for (key,spacedpath) in self._STRUCTURE_MAPPING.items():
            for root in ["MAIN", "LOCAL"]:
                constant = root+"_"+key
                # print "%s = %s(%s)" % (constant,spacedpath,spacedpath.split(" "))
                value = self._from(root,spacedpath.split(" "))
                setattr(self,constant,value)      
                print "%s = %s" % (constant,value)

                
        
    
    
    
    
    
    
    def isGlobalConstant(self,name):
        import re
        return re.match(r"^[A-Z][A-Z_]*$",name) is not None

    def getGlobalConstants(self,entity):
        return [(name,value) for (name,value) in entity.__dict__.items() if self.isGlobalConstant(name)]


    #-----------------------------------------------------------------------
    #  Module Management and python library management.
    #-----------------------------------------------------------------------

    def __addDirectoryToPythPath(self,directory):
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
    
    def __registerPluginDirectories(self):
        """ 
        Add the directory following these patterns to the path and return the list of directories added.
        - <ROOT>/plugins/<PLUGIN_NAME>/<PLUGIN_NAME>
        - <ROOT>/plugins/<PLUGIN_NAME>/libs/python
        - ModelioScribes/commons/modules
        - ModelioScribes/libs/python
        """
        directories = []
        for root in ["LOCAL","MAIN"]:
            plugin_dir = getattr(self, root+ '_PLUGINS')
            if os.path.isdir(plugin_dir):
                plugin_names = os.listdir(plugin_dir)
            else:
                plugin_names = []
            setattr(self, root+"_PLUGINS_NAMES", plugin_names)
            for plugin_name in plugin_names:
                for subdir in [plugin_name, plugin_name+os.sep+"libs"+os.sep+"python"]:
                    directory = self._from(root, [plugin_dir,subdir])
                    constant = root+"_"+subdir.upper()
                    print "%s = %s" % (constant,directory)
                    setattr(self,constant,directory)
                    directories.append(directory)

        raise Exception("Hello - directory has to be added to the path, check variables")
        # add these directory to python path
        for directory in directories:
            if os.path.isdir(directory):
                self.__addDirectoryToPythonPath(directory)
            else:
                raise Exception("%s is not a directory. Cannot add it to python path"%directory)

       
    
        


    


#-------------------------------------------------------------------------------------- 
#  Global Framework Startup.
#--------------------------------------------------------------------------------------   

try:
  PYMODELIO_ENV
except:  
  PYMODELIO_ENV = PyModelioEnv()

  






