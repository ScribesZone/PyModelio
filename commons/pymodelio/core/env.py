# -*- coding: utf-8 -*-

"""
===============================================================================
                PyModelio Environment
===============================================================================

Give access to the PyModelio framework.


The framework provides 4 classes:

* PyModelioEnv
* Plugin
* PluginExecution
* PluginMacro



The parameter is one of the following key:

- "TMP"                         : temporary directory
- "USER_HOME"                   : home directory of user
- "USER_MODELIO"                : directory .modelio in user home
- "MODELIO_WORKSPACE"           : workspace directory of modelio
- "MODELIO_VERSION_SIMPLE"      : modelio version like "3.2"
- "MODELIO_VERSION_FULL"        : modelio version like "3.2.02.0"
- "MAIN"                        : ModelioScribes distribution directory
- "LOCAL"                       : local directory for the user to add features
- "USER_CONFIG_FILE"            : name of the .modelio/pymodelio_config.py
- "<ROOT>_LIBS_PYTHON"          : directory containing external python libs
- "<ROOT>_LIBS_JAVA"            : directory containing external java libs
- "<ROOT>_COMMONS"              : commons directory
- "<ROOT>_PLUGINS"              : directory plugins
- "<ROOT>_PLUGINS_NAMES"        : name of subdirectories in the plugin directories
- "PLUGINS_MAP"                 : list of names of all scribes found
- "PYTHON_PATH_ADDED_DIRS"      : list of directories added to the py path

"""

FRIEND_PROJECTS = ['PyAlaOCL']

import os
import sys
import re
import platform
import types


import pymodelio.core.plugins
from pymodelio.core.plugins import Plugin,PluginExecution

import pymodelio.core.misc
from pymodelio.core.misc import getConstantMap,ensureDirectory,findFile

import pymodelio.core.macros

class PyModelioEnv(object):
    """
    Global Scribe environment, singleton made available as PYMODELIO_ENV top
    level variable.
  
    Once executed there will be only one instance for this class. It is
    created at the beginning when any macro (using the framework) is
    launched for the first time. This environment is then available to later
    as "SCRIBE_ENV". (see the end of this file).
    """
    MAIN = None
    LOCAL = None
    LOCAL_WORKING_DIRECTORY = None
    WITH_MODELIO = None
    WITH_JYTHON = None


    MACROS_SYSTEM_DIRECTORY = None
    MACROS_SYSTEM_CATALOG_FILE = None
    MACROS_SYSTEM_CATALOG = None
    MACROS_WORKSPACE_DIRECTORY = None
    MACROS_WORKSPACE_CATALOG_FILE = None
    MACROS_WORKSPACE_CATALOG = None

    MODELIO_SYSTEM_DIRECTORY = None
    MODELIO_WORKSPACE = None
    MODELIO_VERSION_FULL = None
    MODELIO_VERSION_SIMPLE = None
    MODELIO_HOME = None
    MODELIO_IMPORT_FILE = None
    MODELIO_JYTHON_JAR_FILE = None
    MODELIO_WEB = None
    MODELIO_WEB_USER_MANUALS = None
    MODELIO_WEB_DOC_ROOT = None
    MODELIO_WEB_DOC_JAVADOC = None
    MODELIO_WEB_DOC_METAMODEL = None

    PLUGIN_NAMES = []
    PLUGINS = {}
    PLUGIN_EXECUTIONS = []
    PATH_PYTHON = []
    PATH_PYTHON_INITIAL = []
    PATH_JAVA = []
    PATH_JAVA_INITIAL_CLASS_LOADER = None
    PATH_DOCS = []

    PYTHON_INTERPRETER_GLOBAL_SCOPE = None
    PYTHON_INTERPRETER_GLOBAL_SYMBOLS_BEFORE = set()
    PYTHON_INTERPRETER_GLOBAL_SYMBOLS_AFTER = set()
    PYTHON_INTERPRETER_GLOBAL_SYMBOLS_DEFINED = set()
    TMP = None

    USER_HOME = None
    USER_MODELIO = None
    USER_MODELIO_MACROS = None
    USER_MODELIO_MACROS_CATALOG = None
    USER_CONFIG_FILE = None

    theLog = ""


    @classmethod
    def start(cls):
        """
        Create the PyModelio environment defining a bunch of constants.

        These constants describe the property of this environment and
        in particular relevant directories and paths for Python & Java paths.
        """
        this_directory = os.path.dirname(__file__)
        cls.MAIN = \
            os.path.realpath(os.path.join(this_directory,'..','..','..'))
        cls.WITH_MODELIO = cls.hasPackage('org.modelio.api.modelio')
        cls.WITH_JYTHON = (platform.python_implementation() == 'Jython')
        cls.__setInitialPythonPath()
        cls.__setInitialJavaClassLoader()
        # Many other constants are defined. See documentation
        cls.restart()




    @classmethod
    def restart(cls):
        """
        Define constants and set the java and python paths according to the
        current environment.
        
        Use this method if new directories, plugins, etc. are added.
        Otherwise these changes will not be taken into consideration.
        """
        cls.PLUGIN_EXECUTIONS = []
        cls.__registerSystemDirectories()              # define constants
        if cls.WITH_MODELIO:
            cls.__registerModelioProperties()              # define constants
        cls.__registerUserDirectoriesToProperties()    # define constants
        cls.__managePyModelioLocal()
        cls.__registerRootsCommonsAndLibs()            # define constants
        cls.log('    Registering plugins')
        cls.__registerPlugins()                        # register all plugins
        cls.__registerFriendProjects()
        cls.log('    %i plugin(s) registered' % len(cls.PLUGIN_NAMES))
        cls.__setPythonPath()
        cls.log('    %i directories added to python path'%len(cls.PATH_PYTHON))
        if cls.WITH_JYTHON:
            cls.__setJavaPath()
            cls.log('    %i jar files added to java path' % len(cls.PATH_JAVA))
        cls.__setDocsPath()
        cls.__registerMacros()
        cls.log('    %i directories added to docs path' % len(cls.PATH_DOCS))
        cls.log('    Working directory set to %s' % os.getcwd())

    @classmethod
    def getPlugin(cls,name):
        """
        Get a plugin by name.

        The given name can either be the PluginName (e.g. MetaScribe) or a
        lower version of it.

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
        execution = PluginExecution(plugin,entryFunctionName,modules,debug)
        cls.PLUGIN_EXECUTIONS.append(execution)
        plugin._addExecution(execution)
        execution.run()

    @classmethod
    def fromRoot(cls,root,pathElements=()):
        """
        Return a path to a file or a directory relative to the PyModelio
        *root* directory, *root* being either "LOCAL" or "MAIN".

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
        Return a path to a file or a directory relative to the PyModelio
        main directory.
        
        If nothing is provided then return the main directory.
        """
        return cls.fromRoot("MAIN",pathElements)

    @classmethod
    def fromLocal(cls,pathElements=()):
        """
        Return a path to a file or a directory relative to the PyModelio
        local directory.

        If nothing is provided then return the local directory.
        """
        return cls.fromRoot("LOCAL",pathElements)

    @classmethod
    def loadPythonModule(cls,moduleNames,reload=False):

        # TODO Check this page:
        # https://www.inkling.com/read/learning-python-mark-lutz-4th/
        #                          chapter-24/transitive-module-reloads


        """ 
        Load/reload a (list of) module(s)

        :param str|[str] moduleNames: either a string or a list of strings
        corresponding to module names.

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
                except:
                    pass
            exec( "import "+moduleName )

    @classmethod
    def listPythonModulesInDirectory(cls,rootDirectory):
        modules = []
        for root_dir, dirs, files in os.walk(rootDirectory):
            if '__init__.py' in files:
                package = \
                    '.'.join(
                        os.path.relpath(root_dir, rootDirectory).split(os.sep))
                modules.append(package)
                for file in files:
                    if file.endswith('.py') and file != '__init__.py':
                        module = package + '.' + file[:-len('.py')]
                        modules.append(module)
        return modules

    @classmethod
    def isPythonModule(cls, module):
        return (
            module is not None
            and hasattr(module,'__dict__')
            and hasattr(module,'__name__')
            and hasattr(module,'__file__')
            and (module.__file__ is not None)
            and re.match(r'.*(\.py(c|d|o)?|\$py.class)$',module.__file__)
        )

    @classmethod
    def isPythonDeveloperModule(cls, module):
        return (
            cls.isPythonModule(module)
            and re.match('^__pyclasspath__/Lib/.*',module.__file__) is None
        )

    @classmethod
    def __undoModule(cls, module):
        if hasattr(module, 'unload'):
            print ('UNDO PyModelioEnv: %s ' % module.__name__),
            try:
                module.unload()
                print ('unloaded ')
            except Exception as e:
                print ("PyModelioEnv: unload %s failed: %s"
                      % (module.__name__, e))


    @classmethod
    def __undoGlobalScope(cls):
        import importlib

        for symbol in cls.PYTHON_INTERPRETER_GLOBAL_SYMBOLS_DEFINED:
            if symbol != 'PyModelioEnv':
                try:
                    del cls.PYTHON_INTERPRETER_GLOBAL_SCOPE[symbol]
                except:
                    print 'PyModelioEnv.undo:  cannot delete %s' % symbol

        #CoreModules = \
        #    cls.FRIEND_PYALAOCL_MODULES \
        #    + cls.MAIN_COMMONS_MODULES
        # for some reasons it seems that toplevel modules
        # should be imported for reloading submodules to work
        import pymodelio  # useful
        import pyalaocl  # useful
        #
        # for moduleName in CoreModules:
        #     if moduleName in sys.modules:
        #         module = sys.modules[moduleName]
        #         if hasattr(module, 'unload'):
        #             try:
        #                 module.unload()
        #             except Exception as e:
        #                 print "PyModelioEnv.undo: unload %s failed: %s" \
        #                       % (moduleName, e)
        #     try:
        #         exec ('reload(%s)' % moduleName)
        #         print "PyModelioEnv.undo: %s reloaded" % moduleName
        #     except Exception as e:
        #         print 'PyModelioEnv.undo: Failed to reload(%s): %s ' \
        #               % (moduleName, e)
        #         importlib.import_module(moduleName)
        #         print 'PyModelioEnv.undo: %s imported' % moduleName
        #
        #         #
                # def __deleteAndImportCoreModules():
                #     CoreModules = \
                #         PyModelioEnv.FRIEND_PYALAOCL_MODULES \
                #         + PyModelioEnv.MAIN_COMMONS_MODULES
                #     for moduleName in CoreModules:
                #         if moduleName in sys.modules:
                #             module = sys.modules[moduleName]
                #             if hasattr(module, 'unload'):
                #                 try:
                #                     module.unload()
                #                 except Exception as e:
                #                     print "unload %s: %s" % (moduleName,e)
                #             # if moduleName == 'pyalaocl.modelio':
                #             #      try:
                #             #          pyalaocl.modelio.symbolGroups.deleteFromScope(globals())
                #             #      except Exception as e:
                #             #          print "pymodelio_startup: Can't finalize pyalaocl.modelio."
                #             #          print "                  ", e
                #             # if 'pyalaocl.modelio.profiles' in sys.modules:
                #             #      try:
                #             #          pyalaocl.modelio.profiles.symbolGroups.deleteFromScope(globals())
                #             #      except Exception as e:
                #             #          print "pymodelio_startup: Can't finalize pyalaocl.modelio.profiles"
                #             #          print "                  ", e
                #             try:
                #                 del sys.modules[moduleName]
                #                 print '%s module deleted from system' % moduleName,
                #                 if moduleName in globals():
                #                     try:
                #                         exec ( "del " + moduleName )
                #                         print 'and scope.'
                #                     except AttributeError:
                #                         print '. It was not in scope (AttributeError)'
                #                     except NameError:
                #                         print '.'
                #                 else:
                #                     print '.'
                #             except Exception as e:
                #                 print 'deletion of %s failed' % moduleName
                #                 print "             ", e


    @classmethod
    def __reloadModule(cls, module):
        print ('RELOAD PyModelioEnv: %s ' % module.__name__),
        try:
            reload(module)
            print ('reloaded ')
        except Exception as e:
            print ('PyModelioEnv: reload %s failed: %s'
                    % (module.__name__, e))



    #@classmethod
    #def reloadAllDeveloperPythonModules(cls):

        # def dependentPythonModules(module, acceptModule):
        #     if hasattr(module,'__dict__'):
        #         return [value for value in module.__dict__.values()
        #                 if type(value) == types.ModuleType
        #                     and cls.isPythonModule(value)
        #                     and acceptModule(value)]
        #     else:
        #         return []
        #
        # def transitiveReload(module, visited):
        #     if (cls.isPythonModule(module)
        #             and module not in visited
        #             and acceptModule(module)):
        #         visited[module] = True
        #         for m in dependentPythonModules(module, acceptModule):
        #             transitiveReload(m, visited)
        #         cls.__reloadModule(module)
        #
        # visited = {}
        # for module in modules:
        #     if cls.isPythonModule(module) and acceptModule(module):
        #         transitiveReload(module, visited)

    @classmethod
    def allModulesRecursively(cls, modules, acceptModule):
        """ in inverse dependence order """
        def dependentPythonModules(module):
            if hasattr(module, '__dict__'):
                return [value for value in module.__dict__.values()
                        if type(value) == types.ModuleType
                        and acceptModule(value)]
            else:
                return []

        def dependentTransitive(module, visited):
            if (cls.isPythonModule(module)
                and module not in visited
                and acceptModule(module)):
                visited.append(module)
                for m in dependentPythonModules(module):
                    dependentTransitive(m, visited)

        visited = []
        for module in modules:
            if acceptModule(module):
                dependentTransitive(module, visited)
        return list(reversed(visited))

    @classmethod
    def reboot(cls):
        print
        print '>'*80
        print 'REBOOTING PyModelio'
        orderedDeveloperModules = \
            cls.allModulesRecursively(
                sys.modules.values(),
                cls.isPythonDeveloperModule)

        print orderedDeveloperModules
        cls.__undoGlobalScope()

        for module in orderedDeveloperModules:
            cls.__undoModule(module)

        for module in list(reversed(orderedDeveloperModules)):
            cls.__reloadModule(module)
        print '<' * 80


    @classmethod
    def hasPackage(cls,packageName):
        try:
            exec('import %s'%packageName)
            return True
        except ImportError:
            return False

    @classmethod
    def log(cls,message):
        cls.theLog += message+'\n'

    @classmethod
    def show(cls):
        print "PyModelioEnv initialization log:"
        print cls.theLog
        print
        print "PyModelioEnv"
        for (constant,value) in getConstantMap(cls).items():
            print "    %s = %s" % (constant,value)



        
    #====================================================================
    #                          Class Implementation
    #====================================================================

    @classmethod
    def _setPythonInterpreterGlobalScope(cls,globalScope):
        cls.PYTHON_INTERPRETER_GLOBAL_SCOPE = globalScope


    @classmethod
    def _setPythonInterpreterGlobalSymbolsBefore(cls, symbols):
        cls.PYTHON_INTERPRETER_GLOBAL_SYMBOLS_BEFORE = set(list(symbols))


    @classmethod
    def _setPythonInterpreterGlobalSymbolsAfter(cls, symbols):
        cls.PYTHON_INTERPRETER_GLOBAL_SYMBOLS_AFTER = set(list(symbols))
        cls.PYTHON_INTERPRETER_GLOBAL_SYMBOLS_DEFINED = \
            cls.PYTHON_INTERPRETER_GLOBAL_SYMBOLS_AFTER \
            - cls.PYTHON_INTERPRETER_GLOBAL_SYMBOLS_BEFORE


    @classmethod
    def __setInitialPythonPath(cls):
        if cls.PATH_PYTHON_INITIAL == []:
            # remove the following directory from the path to get the real
            # initial path.
            framework_commons = os.path.join(cls.MAIN,"commons")
            sys.path.remove(framework_commons)
            cls.PATH_PYTHON_INITIAL = list(sys.path)


    @classmethod
    def __setInitialJavaClassLoader(cls):
        if cls.WITH_JYTHON and cls.PATH_JAVA_INITIAL_CLASS_LOADER is None:
            # noinspection PyUnresolvedReferences
            cls.PATH_JAVA_INITIAL_CLASS_LOADER = sys.getClassLoader()


    @classmethod
    def addGlobalFunction(cls,function):
        # define the modelio global function on this very class
        setattr(cls,function.__name__,staticmethod(function))


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
        version = context.getVersion().toString()
        cls.MODELIO_VERSION_FULL= version
        cls.MODELIO_VERSION_SIMPLE = ".".join(version.split(".")[0:2])
        cls.MODELIO_HOME = getModelioHome()
        cls.MODELIO_IMPORT_FILE = getModelioImportFile()
        cls.MODELIO_JYTHON_JAR_FILE = getJythonJarFile()
        cls.MODELIO_WEB = 'http://modelio.org'
        cls.MODELIO_WEB_USER_MANUALS = \
            'http://modelio.org/documentation/user-manuals.html'
        cls.MODELIO_WEB_DOC_ROOT = "http://modelio.org/documentation"
        cls.MODELIO_WEB_DOC_JAVADOC = \
            cls.MODELIO_WEB_DOC_ROOT+'/javadoc-' + cls.MODELIO_VERSION_SIMPLE
        cls.MODELIO_WEB_DOC_METAMODEL =\
            cls.MODELIO_WEB_DOC_ROOT+'/metamodel-'+cls.MODELIO_VERSION_SIMPLE


    @classmethod
    def __registerUserDirectoriesToProperties(cls):
        cls.USER_HOME = os.path.expanduser("~")
        userModelio = os.path.join(cls.USER_HOME,".modelio")
        cls.USER_MODELIO = userModelio
        if cls.WITH_MODELIO:
            version = cls.MODELIO_VERSION_SIMPLE
            cls.MODELIO_SYSTEM_DIRECTORY = os.path.join(userModelio, version)
        cls.USER_CONFIG_FILE = \
            os.path.join(userModelio,"pymodelio_config.py")


    @classmethod
    def __managePyModelioLocal(cls):
        """
        Check if there is a local structure or create it otherwise.

        Set the working directory to LOCAL_WORKING_DIRECTORY.
        """
        # TODO: register this directory in the path in a cleaner way
        cls.__addDirectoryToPythonPath(cls.USER_MODELIO)
        try:
            import pymodelio_config
        except Exception as e:
            sys.stderr.write("ERROR: cannot import pymodelio_config")
            raise
        try:
            # noinspection PyUnresolvedReferences
            cls.LOCAL = pymodelio_config.PYMODELIO_LOCAL
        except Exception as e:
            print e
            cls.LOCAL = None
        # check if there was a setting by the user in .modelio
        # otherwise use the directory .modelio/PyModelioLocal
        if cls.LOCAL is None:
            # The user has not specified any value in its file
            # By default this will be a directory in in the .modelio directory
            cls.LOCAL = os.path.join(cls.USER_MODELIO,"PyModelioLocal")
        cls.LOCAL_WORKING_DIRECTORY = \
            os.path.join(cls.LOCAL,'working_directory')
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
        path_keys = set([path_key
                         for (x,path_key) in SUBDIRECTORY_MAP.values()
                         if path_key is not None])
        path_elements = {}
        for path_key in path_keys:
            path_elements[path_key]=[]

        # deal with directories listed in SUBDIRECTORY_MAP
        for root in ["LOCAL", "MAIN"]:
            for path_key in path_keys:
                path_elements[path_key]=[]
            for (constant_suffix,(subdir,path_key)) \
                    in SUBDIRECTORY_MAP.items():
                constant = root+"_"+constant_suffix
                directory = cls.fromRoot(root,subdir.split(" "))
                setattr(cls,constant,directory)
                # add the directory to the corresponding path if any
                if path_key is not None:
                    if path_key=='JAVA':
                        # In case of java, jar files are to be added,
                        # not the directory
                        jar_files = cls._searchJarFiles(directory)
                        path_elements[path_key].extend(jar_files)
                    elif path_key=='PYTHON':
                        modules = cls.listPythonModulesInDirectory(directory)
                        setattr(cls,constant+'_MODULES',modules)
                        path_elements[path_key].append(directory)
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
        Register the various plugins with LOCAL plugins taking precedence
        over MAIN plugins.
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
                plugin = Plugin(root,plugin_name)
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
    def __registerFriendProjects(cls):
        cls.FRIEND_PROJECTS = FRIEND_PROJECTS
        for friend in FRIEND_PROJECTS:
            directory = os.path.join(cls.MAIN, '..', friend)
            setattr(cls,'FRIEND_'+friend.upper(),directory)
            modules = cls.listPythonModulesInDirectory(directory)
            setattr(cls,'FRIEND_'+friend.upper()+'_MODULES',modules)


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
        sys.path = list(cls.PATH_PYTHON_INITIAL)
        l = list(cls.PATH_PYTHON)
        # reverse the list since the directories are added at the beginning.
        l.reverse()
        for directory in l:
            cls.__addDirectoryToPythonPath(directory)
        # TODO: should this be formalized and generalized? Not sure
        for friend in cls.FRIEND_PROJECTS:
            directory = getattr(cls,'FRIEND_'+friend.upper())
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
        newClassLoader = \
            java.net.URLClassLoader(urls,cls.PATH_JAVA_INITIAL_CLASS_LOADER)
        # noinspection PyUnresolvedReferences
        sys.setClassLoader(newClassLoader)


    @classmethod
    def __setDocsPath(cls):
        cls.__registerPathElements('DOCS')


    @classmethod
    def __registerModelioStyles(cls):
        pass
        # TODO: add code to register styles
        # import os
        # import java.io
        # import re
        #
        #
        # def styleFileName(root, name):
        #     return os.path.join(root, 'styles', name + '.style')
        #     return java.io.File(style_file_name)
        #
        #
        # def readStyleProperties(styleFileName):
        #     properties = {}
        #     for line in tuple(open(filename)):
        #         m = re.match(r'^(?P<key>\w+) *=(?P<value>[^\n]*)', line)
        #         if m:
        #             properties[m.group('key')] = m.group('value')
        #     return properties
        #
        #
        # # print PyModelioEnv.show() # MAIN_ROOT
        # filename = styleFileName(PyModelioEnv.MAIN, 'SRoot')
        # properties = readStyleProperties(filename)
        # print properties['stylename']
        # print properties['basestyle']


    @classmethod
    def __registerMacros(cls):
        # get workspace macros
        cls.MACROS_WORKSPACE_DIRECTORY = \
            os.path.join(cls.MODELIO_WORKSPACE, 'macros')
        cls.MACROS_WORKSPACE_CATALOG_FILE = \
            os.path.join(cls.MACROS_WORKSPACE_DIRECTORY, '.catalog')
        cls.MACROS_WORKSPACE_CATALOG = \
            pymodelio.core.macros.MacroCatalog(
                'workspace', cls.MACROS_WORKSPACE_CATALOG_FILE)

        # register system macros
        cls.MACROS_SYSTEM_DIRECTORY = \
            os.path.join(cls.MODELIO_SYSTEM_DIRECTORY, 'macros')
        cls.MACROS_SYSTEM_CATALOG_FILE = \
            os.path.join(cls.MACROS_SYSTEM_DIRECTORY, '.catalog')
        cls.MACROS_SYSTEM_CATALOG = \
            pymodelio.core.macros.MacroCatalog(
                'system', cls.MACROS_SYSTEM_CATALOG_FILE)


PyModelioEnv.start()




