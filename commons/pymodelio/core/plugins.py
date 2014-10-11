# -*- coding: utf-8 -*-


"""


"""

import os
import sys

import java.lang
import java.net





class Plugin(object):
    """
    Plugin defined within the context of PyModel and executed at least once.

    Constants specific to this plugin are with the "PLUGIN" prefix. In the plugin
    this prefix is used to avoid having to refer to the name of the plugin.

    - PLUGIN                : the  directory of the plugin
    - PLUGIN_NAME           : the name of the plugin
    - PLUGIN_ROOT           : either "MAIN" or "LOCAL"
    - PLUGIN_RES            : directory for resources
    - PLUGIN_PACKAGE        : directory for root plugin package. Plugin name in lowercase.
    - PLUGIN_TESTS
    - PLUGIN_DOCS
    - PLUGIN_PACKAGE
    - PLUGIN_PYTHON_PATH_ELEMENTS
    - PLUGIN_JAVA_PATH_ELEMENTS
    - PLUGIN_DOCS_PATH_ELEMENTS

    All the property of PyModelioEnv are also available directly on this object.
    """

    def __init__(self,pyModelioEnv,root,pluginName):
        """
        Create a new plugin representation and register in the environment constant about
        this plugin.

        Just like the environment there is one instance for each plugin.
        Each time a plugin is executed, a PluginExecution is created for that particular
        execution.
        :param str pluginName: the name of the plugin
        :param "MAIN"|"LOCAL" root: either "MAIN" or "LOCAL"
        :return: a Plugin object
        """
        print "        Registering plugin %s.%s ..." %(root,pluginName),
        self.ENV = pyModelioEnv         #: environment
        self.PLUGIN_ROOT = root
        self.PLUGIN_NAME = pluginName
        self.PLUGIN_CONSTANT_PREFIX = self.PLUGIN_ROOT+"_"+self.PLUGIN_NAME.upper()
        self.__registerPluginDirectories(self,"PLUGIN")
        self.__registerPluginDirectories(self.ENV,self.PLUGIN_CONSTANT_PREFIX)
        print 'done'

    #====================================================================
    #                          Class Implementation
    #====================================================================

    def __getattr__(self,constant):
        """ Return a constant defined on this plugin or the environment.
        :param constant: the constant to read
        :return: the value of the constant
        :raise: KeyError if the constant is neither defined in this plugin nor the environment.
        """
        return getattr(self.ENV,constant)

    def __registerPluginDirectories(self,objectToChange,constantPrefix):
        """
        Define on this plugin some constants corresponding subdirectories.
        These constants will be define either on this plugin object or
        on the environment (and this depending on the first parameter).
        In each case a distinct prefix will be used for the constants.
        Create also constants for the various path.
        :param objectToChange PuModelioEnv|Plugin: either self or the environment.
        :param constantPrefix str: the prefix to be add to constant.
        :return: none
        """

        SUBDIRECTORY_MAP = {
            # Constant Suffix directories path_key
            ''              : ('',None),
            '<PLUGIN_NAME>' : (None,'PYTHON'),
            'RES'           : ('res',None),
            'TESTS'         : ('tests','PYTHON'),
            'DOCS'          : ('docs','DOCS'),
            'LIBS_JAVA'     : ('libs java','JAVA'),
            'LIBS_PYTHON'   : ('libs python','PYTHON')
            }

        # initialize the different path element lists to []
        path_keys = set([path_key for (x,path_key) in SUBDIRECTORY_MAP.values()
                         if path_key is not None])
        path_elements = {}
        for path_key in path_keys:
            path_elements[path_key]=[]

        # deal with plugin directories listed in SUBDIRECTORY_MAP
        for (constant_suffix,(subdir_string,path_key)) in SUBDIRECTORY_MAP.items():
            # define the constant (either in this class
            if constant_suffix == "<PLUGIN_NAME>":
                constant = constantPrefix+"_PACKAGE"
                subdir_elements = ['plugins',self.PLUGIN_NAME,self.PLUGIN_NAME.lower()]
            else:
                constant = constantPrefix+("_" if constant_suffix else "")+constant_suffix
                subdir_elements = ['plugins',self.PLUGIN_NAME]+subdir_string.split(' ')
            directory = self.ENV.fromRoot(self.PLUGIN_ROOT,subdir_elements)
            setattr(objectToChange,constant,directory)
            # add the directory to the corresponding path if any
            if path_key is not None:
                if path_key=='JAVA':
                    # In case of java, jar files are to be added, not the directory
                    jar_files = self.ENV._searchJarFiles(directory)
                    path_elements[path_key].extend(jar_files)
                else:
                    # In other cases, we add simply the directory
                    path_elements[path_key].append(directory)
        # update the different paths constant with the information collected
        for path_key in path_keys:
            path_constant = constantPrefix+"_PATH_"+path_key
            setattr(objectToChange,path_constant,path_elements[path_key])

    def __str__(self):
        r = "Plugin "+self.PLUGIN_ROOT+"."+self.PLUGIN_NAME+"\n"
        for attribute in self.__attrs__:
            if attribute.startsWith("PLUGIN_"):
                r += "    %s = %s\n" % (getattr(self,attribute,"*No Value*"))
        return r

    def __repr__(self):
        return "Plugin(%s.%s:%s)" %(self.PLUGIN_ROOT,self.PLUGIN_NAME,self.PLUGIN)





class PluginExecution(Plugin):
    def __init__(self, plugin_name, entryFunName, modules=[], debug=None):
        """ Execute a particular plugin entry point.
        """

        global PLUGIN
        super(PluginExecution, self).__init__(self, plugin_name)
        self.env.plugin = self  # set the current plugin just for information
        PLUGIN = self

        # --- collect selectedElements, modelingSession, selection from modelio variables
        global selectedElements  #RO
        self.selectedElements = selectedElements
        global modelingSession  #RO
        self.modelingSession = modelingSession
        global selection  #RO
        self.selection = selection

        #--- compute debug flag, based on the parameter or DEBUG global variable otherwise
        if debug is None:
            try:
                global DEBUG
                self.debug = DEBUG
            except:
                self.debug = DEBUG
        else:
            self.debug = debug

        #--- compute
        (m, f) = self._computeEntry(plugin_name, entryFunName)
        self.entryModule = m
        self.entryFunName = f

        #-- load the list of modules specified (plus the entry modules)
        self.modules = modules
        if self.entryModule not in modules:
            self.modules += [self.entryModule]
        self.env.loadPythonModule(self.modules, self.debug)

        #-- execute the entry function
        self.runEntryFunction()


    def runEntryFunction(self):
        self.env.plugin = self  # set the current plugin
        exec ( "import " + self.entryModule + ";"
               + self.entryFunName + "(self)" )


    def _computeEntry(self, pluginname, entryFunName):
        """ compute the name of the entryModule from the entry function name provided
        """
        lastDotIndex = entryFunName.rfind('.')
        if lastDotIndex == -1:
            # if the entry function is not qualified, then deduce the module from pluginname
            entryModule = pluginname.lower()
            entryFunName = entryModule + "." + entryFunName
        else:
            # take the qualifier
            entryModule = entryFunName[0:lastDotIndex]
            entryFunName = entryFunName
        return (entryModule, entryFunName)