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
- access to modelio global variables (selection, selectedElements, modelingSession from
  modules.
- set the working directory to a local directory so that macros can read and write
  in a well defined place. By default the local directory is Modelio installation
  directory, which is definitively not a good place to write files.

The framework provides 3 classes:

- PyModelioEnv
- Plugin
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
from pymodelio.core.plugins import Plugin,PluginExecution
from pymodelio.core.misc import getConstantMap,ensureDirectory,findFile


class PyModelioEnv(object):
    """ 
    Global Scribe environment, singleton made available as PYMODELIO_ENV top level variable.
  
    Once executed there will be only one instance for this class. It is created
    at the beginning when any macro (using the framework) is launched for the first time. 
    This environment is then available to later as "SCRIBE_ENV". 
    (see the end of this file). 
    """

    @classmethod
    def start(cls, initialPythonPath, pyModelioMain, pyModelioLocal,
                 modelioGlobalFunctions,
                 withModelio=True, withJython=True):
        """
        Create the PyModelio environment with a bunch of constants towards relevant directories
        and with correct values for Python & Java paths.
        :param initialPythonPath:
        :param pyModelioMain:
        :param pyModelioLocal:
        :param modelioGlobalFunctions:
        :param withModelio:
        :param withJython:
        """
        cls.INITIAL_PYTHON_PATH = initialPythonPath    #: Initial python path
        cls.MAIN = pyModelioMain                       #: "PyModelio" Directory
        # The following value will be processed in this class.
        # It can have None currently but then a default place will be given.
        cls.LOCAL = pyModelioLocal                     #: "PyModelioLocal" Directory
        cls.WITH_MODELIO = withModelio                 #: Is the execution in the context of modelio?
        cls.WITH_JYTHON =  withJython                  #: Is the execution on the Jython platform?
        if cls.WITH_JYTHON:
            # noinspection PyUnresolvedReferences
            cls.INITIAL_JAVA_CLASS_LOADER = sys.getClassLoader()   #: Initial class loader
        else:
            cls.INITIAL_JAVA_CLASS_LOADER = None
        # Many other constants are defined. See documentation

        # define the modelio global function on this very class
        for function in modelioGlobalFunctions:
            setattr(cls,function.__name__,staticmethod(function))

        cls.restart()

    @classmethod
    def restart(cls):
        """ 
        Define constants and set the java and python paths according to the current environment.
        
        Use this method if new directories, plugins, etc. are added.
        Otherwise these changes will not be taken into consideration.
        """
        cls.PLUGIN_EXECUTIONS = []
        cls.__registerSystemDirectories()              # define constants
        if cls.WITH_MODELIO:
            cls.__registerModelioProperties()              # define constants
        cls.__registerUserDirectoriesToProperties()    # define constants
        cls.__managePyModelioLocal()                   # constants + directory structure
        cls.__registerRootsCommonsAndLibs()            # define constants
        print '    Registering plugins'
        cls.__registerPlugins()                        # register all plugins
        print '    %i plugin(s) registered' % len(cls.PLUGIN_NAMES)
        cls.__setPythonPath()
        # noinspection PyUnresolvedReferences
        print '    %i directories added to python path' % len(cls.PATH_PYTHON)
        if cls.WITH_JYTHON:
            cls.__setJavaPath()
            # noinspection PyUnresolvedReferences
            print '    %i jar files added to java path' % len(cls.PATH_JAVA)
        cls.__setDocsPath()
        # noinspection PyUnresolvedReferences
        print '    %i directories added to docs path' % len(cls.PATH_DOCS)
        print '    Working directory set to %s' % os.getcwd()

    @classmethod
    def getPlugin(cls,name):
        """
        Get a plugin by name.

        The given name can either be the PluginName (e.g. MetaScribe) or a lower
        version of it.

        :param name: The name of the plugin or a lowercase version of it.
        :type name: str
        :return: a plugin object
        :rtype: pymodelio.core.plugins.Plugin
        :raise: ValueError if no such plugin
        """
        # try first to get it directly
        try:
            return cls.PLUGINS[name]
        except KeyError:
            # try to search with lower cases
            for (pluginName,plugin) in cls.PLUGINS.items():
                if name==pluginName.lower():
                    return plugin
            # not found
            raise ValueError('No Plugin named %s' % name)

    @classmethod
    def execute(cls,entryFunctionName,modules=(),debug=False):
        name = entryFunctionName.split(".")[0]
        plugin = cls.getPlugin(name)
        execution = PluginExecution(cls,plugin,entryFunctionName,modules,debug)
        cls.PLUGIN_EXECUTIONS.append(execution)
        plugin._addExecution(execution)
        execution.run()

    @classmethod
    def fromRoot(cls,root,pathElements=()):
        """
        Return a path to a file or a directory relative to the PyModelio *root* directory,
        *root* being either "LOCAL" or "MAIN".

        If nothing is provided then return the *root* directory.
        :param "MAIN"|"ROOT" root: the root directory used as a reference.
        :param [str] pathElements: a list (or tuple) of directory/file names.
            Only only the last element could be file.
        """
        if root=="MAIN":
            root = cls.MAIN
        elif root=="LOCAL":
            root = cls.LOCAL
        else:
            raise ValueError("%s given. Must be either MAIN or LOCAL"%root)
        return os.path.join(* [root]+pathElements)

    @classmethod
    def fromMain(cls,pathElements=()):
        """ 
        Return a path to a file or a directory relative to the PyModelio main directory.
        
        If nothing is provided then return the main directory.
        """
        return cls.fromRoot("MAIN",pathElements)

    @classmethod
    def fromLocal(cls,pathElements=()):
        """
        Return a path to a file or a directory relative to the PyModelio local directory.

        If nothing is provided then return the local directory.
        """
        return cls.fromRoot("LOCAL",pathElements)

    @classmethod
    def loadPythonModule(cls,moduleNames,reload=False):

        # TODO Check this page https://www.inkling.com/read/learning-python-mark-lutz-4th/chapter-24/transitive-module-reloads


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


    @classmethod
    def show(cls):
        print "PyModelioEnv"
        for (constant,value) in getConstantMap(cls).items():
            print "    %s = %s" % (constant,value)



        
    #====================================================================
    #                          Class Implementation
    #====================================================================


    @classmethod
    def __registerSystemDirectories(cls):
        """ add system directories to properties 
        :rtype : void
        """
        import tempfile
        cls.TMP = tempfile.gettempdir()

    @classmethod
    def __registerModelioProperties(cls):

        def getModelioHome():
            # noinspection PyUnresolvedReferences
            eclipse_home = sys.registry.getProperty('eclipse.home.location')
            import urlparse
            import urllib
            return urllib.url2pathname(urlparse.urlsplit(eclipse_home).path)

        def getModelioImportFile():
            return findFile('initengine.py',cls.MODELIO_HOME)

        def getJythonJarFile():
            return findFile('jython.jar',cls.MODELIO_HOME)
        # noinspection PyUnresolvedReferences
        from org.modelio.api.modelio import Modelio
        context = Modelio.getInstance().getContext()
        workspaceDir = context.getWorkspacePath().toString()
        cls.MODELIO_WORKSPACE = workspaceDir
        cls.MODELIO_WORKSPACE_MACROS = os.path.join(workspaceDir,'macros')
        version = context.getVersion().toString()
        cls.MODELIO_VERSION_FULL= version
        cls.MODELIO_VERSION_SIMPLE = ".".join(version.split(".")[0:2])
        cls.MODELIO_HOME = getModelioHome()
        cls.MODELIO_IMPORT_FILE = getModelioImportFile()
        cls.MODELIO_JYTHON_JAR_FILE = getJythonJarFile()
        cls.MODELIO_WEB = 'http://modelio.org'
        cls.MODELIO_WEB_USER_MANUALS = 'http://modelio.org/documentation/user-manuals.html'
        cls.MODELIO_WEB_DOC_ROOT = "http://modelio.org/documentation"
        cls.MODELIO_WEB_DOC_JAVADOC = cls.MODELIO_WEB_DOC_ROOT \
                                      + '/javadoc-' + cls.MODELIO_VERSION_SIMPLE
        cls.MODELIO_WEB_DOC_METAMODEL = cls.MODELIO_WEB_DOC_ROOT \
                                        + '/metamodel-' + cls.MODELIO_VERSION_SIMPLE

    @classmethod
    def __registerUserDirectoriesToProperties(cls):
        cls.USER_HOME = os.path.expanduser("~")
        userModelio = os.path.join(cls.USER_HOME,".modelio")
        cls.USER_MODELIO = userModelio
        if cls.WITH_MODELIO:
            version = cls.MODELIO_VERSION_SIMPLE
            cls.USER_MODELIO_MACROS = \
        cls.PYMODELIO_PATHS_FILE = \
            os.path.join(userModelio,"pymodelio_paths.py")

    @classmethod
    def __managePyModelioLocal(cls):
        """
        Check if there is a local structure or create it otherwise.

        Set the working directory to LOCAL_WORKING_DIRECTORY.
        """
        # check if there was a setting by the user in .modelio
        # otherwise use the directory .modelio/PyModelioLocal
        if cls.LOCAL is None:
            # The user has not specified any value in its file
            # By default this will be a directory in in the .modelio directory
            cls.LOCAL = os.path.join(cls.USER_MODELIO,"PyModelioLocal")
        cls.LOCAL_WORKING_DIRECTORY = os.path.join(cls.LOCAL,'working_directory')
        cls.__ensurePyModelioLocalStructure()
        os.chdir(cls.LOCAL_WORKING_DIRECTORY)

    @classmethod
    def __ensurePyModelioLocalStructure(cls):
        """ Ensure that the PyModelioLocal directory structure is ok """
        ensureDirectory(cls.LOCAL)
        ensureDirectory(cls.LOCAL_WORKING_DIRECTORY)

    @classmethod
    def __registerRootsCommonsAndLibs(cls):
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
                directory = cls.fromRoot(root,subdir.split(" "))
                setattr(cls,constant,directory)
                # add the directory to the corresponding path if any
                if path_key is not None:
                    if path_key=='JAVA':
                        # In case of java, jar files are to be added, not the directory
                        jar_files = cls._searchJarFiles(directory)
                        path_elements[path_key].extend(jar_files)
                    else:
                        # In other cases, we add simply the directory
                        path_elements[path_key].append(directory)
            # update the different paths constant with the information collected
            for path_key in path_keys:
                path_constant = root+"_PATH_"+path_key
                setattr(cls,path_constant,path_elements[path_key])

    @classmethod
    def __registerPlugins(cls):
        """
        Register the various plugins with LOCAL plugins taking precedence over MAIN plugins.
        """
        # Add the directories in an order that make
        # that plugin defined locally will override
        # plugins with the same name in the main root.
        for root in ["MAIN","LOCAL"]:  # DO NOT change this order!
            plugin_dir = cls.fromRoot(root,["plugins"])
            plugins = {}
            setattr(cls,root+"_PLUGINS_ROOT",plugin_dir)
            if os.path.isdir(plugin_dir):
                plugin_names = os.listdir(plugin_dir)
            else:
                plugin_names = []
            setattr(cls, root+"_PLUGINS_NAMES", plugin_names)

            for plugin_name in plugin_names:
                plugin = Plugin(cls,root,plugin_name)
                plugins[plugin_name] = plugin

            setattr(cls,root+"_PLUGINS",plugins)

        # Compute the list of plugins. Some "MAIN" plugins can be hidden
        # because of "LOCAL" plugins.
        all_plugins = cls.MAIN_PLUGINS.copy()
        all_plugins.update(cls.LOCAL_PLUGINS)
        cls.PLUGINS = all_plugins
        cls.PLUGIN_NAMES = all_plugins.keys()

        for (name,plugin) in all_plugins.items():
            setattr(cls,'PLUGIN_'+(name.upper()),plugin)

    @classmethod
    def __registerPathElements(cls,pathKey):
        path_elements = []
        for plugin in cls.PLUGINS.values():
            path_elements += getattr(plugin,"PLUGIN_PATH_"+pathKey)
        for root in ["LOCAL","MAIN"]:
            path_elements += getattr(cls,root+'_PATH_'+pathKey)
        setattr(cls,'PATH_'+pathKey,path_elements)

    @classmethod
    def __setPythonPath(cls):
        cls.__registerPathElements('PYTHON')
        sys.path = list(cls.INITIAL_PYTHON_PATH)
        # noinspection PyUnresolvedReferences
        l = list(cls.PATH_PYTHON)
        # reverse the list since the directories are added at the beginning.
        l.reverse()
        for directory in l:
            cls.__addDirectoryToPythonPath(directory)
        # TODO: should this be formalized and generalized? Not sure
        FRIEND_PROJECTS = ['AlaOCL']
        for friend in FRIEND_PROJECTS:
            directory = os.path.join(cls.MAIN,'..',friend)
            cls.__addDirectoryToPythonPath(directory)

    @classmethod
    def __addDirectoryToPythonPath(cls,directory):
        """
        Add the directory at the *beginning* of to the python path
        if it does not exist already.
        """
        if not directory in sys.path:
            sys.path.insert(0,directory)


    @classmethod
    def _searchJarFiles(cls,directory):
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


    @classmethod
    def __setJavaPath(cls):
        # Having these import here instead that at the global level
        # avoid problems with importing this module in python rather
        # then jython. Useful for sphinx and so on.

        # noinspection PyUnresolvedReferences
        import java.net

        cls.__registerPathElements('JAVA')
        urls = []
        # noinspection PyUnresolvedReferences
        for jar_file in cls.PATH_JAVA:
            cls.__addDirectoryToPythonPath(jar_file)
            urls.append(java.net.URL("file:"+jar_file))
        newClassLoader = java.net.URLClassLoader(urls,cls.INITIAL_JAVA_CLASS_LOADER)
        # noinspection PyUnresolvedReferences
        sys.setClassLoader(newClassLoader)



    @classmethod
    def __setDocsPath(cls):
        cls.__registerPathElements('DOCS')


