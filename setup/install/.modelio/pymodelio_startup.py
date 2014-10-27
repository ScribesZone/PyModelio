# coding=utf-8

_DEBUG_PYMODELIO_CORE = True

#---------- get PYMODELIO_MAIN path -------------------------------------------------
import os
import sys
# noinspection PyUnresolvedReferences
import encodings # needed to avoid strange when loading some modules (due to modelio)

if _DEBUG_PYMODELIO_CORE:   # make sure that the core is reloaded
    try:
        import pymodelio.core.misc
        import pymodelio.core.plugins
        import pymodelio.core.env
        import alaocl
        import alaocl.jython
        import alaocl.modelio
        reload (pymodelio.core.misc)
        reload (pymodelio.core.plugins)
        reload (pymodelio.core.env)
        reload (alaocl)
        reload (alaocl.jython)
        reload (alaocl.modelio)
    except Exception as e:
        print e

try:
    # Check if this variable is defined.
    # If yes, the framework has already been initialized.
    # So this file do don't do anything.

    # noinspection PyStatementHasNoEffect PyUnboundLocalVariable
    PYMODELIO_INITIALIZED

    if _DEBUG_PYMODELIO_CORE:
        raise Exception('Just to go to except part...')

except:
    # This is the first time this file is executed, or at least it was never
    # executed completely because of errors.

    # Set WITH_JYTHON
    import platform
    WITH_JYTHON = (platform.python_implementation() == 'Jython')

    # Set WITH_MODELIO
    try:
        Modelio
    except NameError:
        # This will happen for instance if Sphynx is looking at the source
        WITH_MODELIO = False
        print "Execution of PyModelio outside Modelio. Most probably for sphynx?"
    else:
        WITH_MODELIO = True

    PATHS_FILE = os.path.join(os.path.expanduser("~"),".modelio","pymodelio_paths.py")


    #------------------------------------------------------------------------------------
    # Define global functions that will enable accessing modelio global variable
    # from modules at any time.
    #------------------------------------------------------------------------------------

    def getSelectedElements():
        global selectedElements
        return selectedElements

    def getModelingSession():
        global modelingSession
        return modelingSession

    def getSelection():
        global selection
        return selection

    MODELIO_GLOBAL_FUNCTIONS = [getSelectedElements,getModelingSession,getSelection]

    #------------------------------------------------------------------------------------
    # Try to find and set PYMODELIO_MAIN path variable.
    #------------------------------------------------------------------------------------
    try:
        # check if the variable is already defined at the top level
        PYMODELIO_MAIN
    except:
        # PYMODELIO_MAIN not defined yet. Get it from .modelio/pymodeliopaths.py
        print ("Executing %s to get the variable PYMODELIO_MAIN ..." % PATHS_FILE),
        try:
            execfile(PATHS_FILE)
        except Exception as e:
            print " FAILED!\n"
            sys.stderr.write("ERROR: cannot execute %s\n\n" % PATHS_FILE)
            raise
        else:
            print " ok"

    # Check again that the variable is defined at the top level.
    try:
        PYMODELIO_MAIN
    except Exception as e:
        msg = "The value PYMODELIO_MAIN must be defined in %s\n\n"
        sys.stderr.write( msg % PATHS_FILE)
        raise
    # If the user do not define the PYMODELIO_LOCAL variable, set it to None
    # A default value will be chosen by the environment PyModelioEnv
    try:
        # noinspection PyUnboundLocalVariable
        PYMODELIO_LOCAL
    except:
        PYMODELIO_LOCAL = None

    # Here we are sure that PYMODELIO_MAIN is defined (or an exception was raised).
    # We may also have a value for PYMODELIO_LOCAL if the user has defined it?

    #------------------------------------------------------------------------------------
    # Check that PYMODELIO_MAIN is a directory
    #------------------------------------------------------------------------------------

    # Check if the variable PYMODELIO_MAIN is a valid path
    if not os.path.isdir(PYMODELIO_MAIN):
        msg = "In %s, PYMODELIO_MAIN is set to %s, but this is not a directory"
        current_value = PYMODELIO_MAIN  # keep it just to display it a few lines below
        del PYMODELIO_MAIN  # Fundamental to force reload of PATHS_FILE next time
        raise Exception( msg % (PATHS_FILE,current_value) )

    #------------------------------------------------------------------------------------
    # Deal with first path adjustments
    #------------------------------------------------------------------------------------
    try:
        # noinspection PyUnboundLocalVariable
        INITIAL_PYTHON_PATH
    except:
        # Save the path for further possible rollbacks
        INITIAL_PYTHON_PATH = list(sys.path)
    framework_commons = os.path.join(PYMODELIO_MAIN,"commons")
    if framework_commons not in sys.path:
        # add the directory containing the core of the PyModelio framework to the python path
        sys.path.insert(0,framework_commons)



    #------------------------------------------------------------------------------------
    # Import the PyModelio environment and create it.
    #------------------------------------------------------------------------------------
    print
    print "Loading pymodelio.core.env.PyModelioEnv from path %s" % framework_commons
    from pymodelio.core.env import PyModelioEnv
    print "Initializing PyModelio environment."
    PyModelioEnv.start(INITIAL_PYTHON_PATH,PYMODELIO_MAIN,PYMODELIO_LOCAL,
                       MODELIO_GLOBAL_FUNCTIONS, WITH_MODELIO,WITH_JYTHON )

    #------------------------------------------------------------------------------------
    # Import modules to inject code and for convenience in the python console
    #------------------------------------------------------------------------------------

    from pymodelio.core.env import *

    # make alaocl features available at the top level
    from alaocl import *
    # install jython extensions. In particular instrument JDK collections.
    import alaocl.jython
    # install modelio extensions. In particular instrument modelio collections.
    from alaocl.modelio import *

    print "PyModelio environment successfully initialized. For more information 'print PyModelioEnv.show()'"
    print

    PYMODELIO_INITIALIZED=True
