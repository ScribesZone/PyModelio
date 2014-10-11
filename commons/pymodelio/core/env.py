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
- "MAIN"                        : ModelioScribes distribution directory
- "LOCAL"                       : local directory for the user to add features
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
from pymodelio.core.plugins import Plugin
from pymodelio.core.misc import getConstantMap


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
        self.MAIN = pyModelioMain                       #: "PyModelio" Directory
        # The following value will be processed in this class.
        # It can have None currently but then a default place will be given.
        self.LOCAL = pyModelioLocal                     #: "PyModelioLocal" Directory
        self.WITH_MODELIO = withModelio                 #: Is the execution in the context of modelio?
        if self.WITH_MODELIO:
            # noinspection PyUnresolvedReferences
            self.INITIAL_JAVA_CLASS_LOADER = sys.getClassLoader()   #: Initial class loader
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
        self.__registerSystemDirectories()              # define constants
        if self.WITH_MODELIO:
            self.__registerModelioProperties()              # define constants
        self.__registerUserDirectoriesToProperties()    # define constants
        self.__managePyModelioLocal()                   # constants + directory structure
        self.__registerRootsCommonsAndLibs()            # define constants
        print '    Registering plugins'
        self.__registerPlugins()                        # register all plugins
        print '    %i plugin(s) registered' % len(self.PLUGIN_NAMES)
        self.__setPythonPath()
        print '    %i directories added to python path' % len(self.PATH_PYTHON)
        if self.WITH_MODELIO:
            self.__setJavaPath()
            print '    %i jar files added to java path' % len(self.PATH_JAVA)
        self.__setDocsPath()
        print '    %i directories added to docs path' % len(self.PATH_DOCS)

    def fromRoot(self,root,pathElements=()):
        """
        Return a path to a file or a directory relative to the PyModelio *root* directory,
        *root* being either "LOCAL" or "MAIN".

        If nothing is provided then return the *root* directory.
        :param "MAIN"|"ROOT" root: the root directory used as a reference.
        :param [str] pathElements: a list (or tuple) of directory/file names.
            Only only the last element could be file.
        """
        if root=="MAIN":
            root = self.MAIN
        elif root=="LOCAL":
            root = self.LOCAL
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


    def __str__(self):
        r = "PyModelioEnv\n"
        for (constant,value) in getConstantMap(self).items():
            r += "    %s = %s\n" % (constant,value)
        return r

        
    #====================================================================
    #                          Class Implementation
    #====================================================================
    

    
    def __registerSystemDirectories(self):
        """ add system directories to properties 
        :rtype : void
        """
        import tempfile
        self.TMP = tempfile.gettempdir()
    
    def __registerModelioProperties(self):
        # noinspection PyUnresolvedReferences
        from org.modelio.api.modelio import Modelio

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
        if self.LOCAL is None:
            # The user has not specified any value in its file
            # By default this will be a directory in in the .modelio directory
            self.LOCAL = os.path.join(self.USER_MODELIO,"PyModelioLocal")
        if not os.path.isdir(self.LOCAL):
            # There is no directory for the local structure
            # initialize it
            self.__initializePyModelioLocal()
        
    def __initializePyModelioLocal(self):
        """ Create an initial PyModelioLocal directory structure """
        os.mkdir(self.LOCAL)
        # TODO: copy the structure from an existing place
            
    def __registerRootsCommonsAndLibs(self):
        """
        Add directories following these patterns:

        - <ROOT>/commons
        - <ROOT>/libs/python
        - <ROOT>/libs/java
        :return:
        """


        # use to build the mapping between constants and paths
        # keep it to make evolution of mapping possible
        SUBDIRECTORY_MAP = {
            "COMMONS": ("commons","PYTHON"),
            'RES'           : ('res',None),
            'TESTS'         : ('tests','PYTHON'),
            'DOCS'          : ('docs','DOCS'),
            "LIBS_PYTHON": ("libs python","PYTHON"),
            "LIBS_JAVA": ("libs java","JAVA"),
        }

        # initialize the different path element lists to []
        path_keys = set([path_key for (x,path_key) in SUBDIRECTORY_MAP.values()
                         if path_key is not None])
        path_elements = {}
        for path_key in path_keys:
            path_elements[path_key]=[]

        # deal with directories listed in SUBDIRECTORY_MAP
        for root in ["LOCAL", "MAIN"]:
            for path_key in path_keys:
                path_elements[path_key]=[]
            for (constant_suffix,(subdir,path_key)) in SUBDIRECTORY_MAP.items():
                constant = root+"_"+constant_suffix
                directory = self.fromRoot(root,subdir.split(" "))
                setattr(self,constant,directory)
                # add the directory to the corresponding path if any
                if path_key is not None:
                    if path_key=='JAVA':
                        # In case of java, jar files are to be added, not the directory
                        jar_files = self._searchJarFiles(directory)
                        path_elements[path_key].extend(jar_files)
                    else:
                        # In other cases, we add simply the directory
                        path_elements[path_key].append(directory)
            # update the different paths constant with the information collected
            for path_key in path_keys:
                path_constant = root+"_PATH_"+path_key
                setattr(self,path_constant,path_elements[path_key])


    def __registerPlugins(self):
        """
        Register the various plugins with LOCAL plugins taking precedence over MAIN plugins.
        """
        # Add the directories in an order that make
        # that plugin defined locally will override
        # plugins with the same name in the main root.
        for root in ["MAIN","LOCAL"]:  # DO NOT change this order!
            plugin_dir = self.fromRoot(root,["plugins"])
            plugins = {}
            setattr(self,root+"_PLUGINS_ROOT",plugin_dir)
            if os.path.isdir(plugin_dir):
                plugin_names = os.listdir(plugin_dir)
            else:
                plugin_names = []
            setattr(self, root+"_PLUGINS_NAMES", plugin_names)

            for plugin_name in plugin_names:
                plugin = Plugin(self,root,plugin_name)
                plugins[plugin_name] = plugin

            setattr(self,root+"_PLUGINS",plugins)
        all_plugins = self.MAIN_PLUGINS.copy()
        all_plugins.update(self.LOCAL_PLUGINS)
        self.PLUGINS = all_plugins
        self.PLUGIN_NAMES = all_plugins.keys()




    def __registerPathElements(self,pathKey):
        path_elements = []
        for plugin in self.PLUGINS.values():
            path_elements += getattr(plugin,"PLUGIN_PATH_"+pathKey)
        for root in ["LOCAL","MAIN"]:
            path_elements += getattr(self,root+'_PATH_'+pathKey)
        setattr(self,'PATH_'+pathKey,path_elements)

    def __setPythonPath(self):
        self.__registerPathElements('PYTHON')
        # noinspection PyUnresolvedReferences
        for directory in self.PATH_PYTHON:
            self.__addDirectoryToPythonPath(directory)


    def __addDirectoryToPythonPath(self,directory):
        """ Add the directory to the python path if it does not exist already. """
        if not directory in sys.path:
            sys.path.append(directory)



    def _searchJarFiles(self,directory):
        """
        Return the list of .jar files in the given directory.

        If the name given is not a directory or in any case of error
        just return an empty list but do not fail.
        :param directory: the full path to the directory to explore
        :type directory: str
        :return: the list of .jar files
        :rtype: list[str]
        """
        jars = []
        if os.path.isdir(directory):
            try:
                files = os.listdir(directory)
            except:
                return []
            for file in files:
                file_path = directory+os.sep+file
                try:
                  is_jar = file.endswith('.jar') and os.path.isfile(file_path)
                except:
                    is_jar = False
                if is_jar:
                    jars.append(file_path)
        return jars



    def __setJavaPath(self):
        # Having these import here instead that at the global level
        # avoid problems with importing this module in python rather
        # then jython. Useful for sphinx and so on.

        # noinspection PyUnresolvedReferences
        import java.net

        self.__registerPathElements('JAVA')
        urls = []
        # noinspection PyUnresolvedReferences
        for jar_file in self.PATH_JAVA:
            self.__addDirectoryToPythonPath(jar_file)
            urls.append(java.net.URL("file:"+jar_file))
        newClassLoader = java.net.URLClassLoader(urls,self.INITIAL_JAVA_CLASS_LOADER)
        # noinspection PyUnresolvedReferences
        sys.setClassLoader(newClassLoader)

    # def __restoreJavaPath(self):
    #    sys.setClassLoader(self.INITIAL_JAVA_CLASS_LOADER)
    # def __str__(self):
    #    sep = java.lang.System.getProperty("path.separator")
    #    urls = sys.getClassLoader().getURLs()
    #    return sep.join([url.getPath() for url in urls])


    def __setDocsPath(self):
        self.__registerPathElements('DOCS')


