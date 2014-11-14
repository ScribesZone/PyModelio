# coding=utf-8

_DEBUG_PYMODELIO_CORE = True

#---------- get PYMODELIO_MAIN path -------------------------------------------
import os
import sys

# To avoid strange when loading some modules (due to modelio)
# noinspection PyUnresolvedReferences
import encodings  # needed

if _DEBUG_PYMODELIO_CORE:  # make sure that the core is reloaded
    try:
        import pymodelio.core.misc
        import pymodelio.core.plugins
        import pymodelio.core.env
        import alaocl
        import alaocl.injector
        import alaocl.jython
        import alaocl.modelio
        import alaocl.jinja2

        reload(pymodelio.core.misc)
        reload(pymodelio.core.plugins)
        reload(pymodelio.core.env)
        reload(alaocl)
        reload(alaocl.injector)
        reload(alaocl.jython)
        reload(alaocl.modelio)
        reload(alaocl.jinja2)
    except Exception as e:
        print "Packages has not been defined yet."
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

    # Set WITH_MODELIO
    try:
        Modelio
    except NameError:
        # This will happen for instance if Sphynx is looking at the source
        WITH_MODELIO = False
    else:
        WITH_MODELIO = True

    USER_CONFIG_FILE = os.path.join(os.path.expanduser("~"),
                                    ".modelio", "pymodelio_config.py")


    #--------------------------------------------------------------------------
    # Try to find and set PYMODELIO_MAIN path variable.
    #--------------------------------------------------------------------------
    try:
        # check if the variable is already defined at the top level
        PYMODELIO_MAIN
    except:
        # PYMODELIO_MAIN not defined. Get it from .modelio/pymodeliopaths.py
        print ("Executing %s to get the variable PYMODELIO_MAIN ..."
               % USER_CONFIG_FILE),
        try:
            execfile(USER_CONFIG_FILE)
        except Exception as e:
            print " FAILED!\n"
            sys.stderr.write("ERROR: cannot execute %s\n\n" % USER_CONFIG_FILE)
            raise
        else:
            print " ok"

    # Check again that the variable is defined at the top level.
    try:
        PYMODELIO_MAIN
    except Exception as e:
        msg = "The value PYMODELIO_MAIN must be defined in %s\n\n"
        sys.stderr.write(msg % USER_CONFIG_FILE)
        raise


    # Here we are sure that PYMODELIO_MAIN is defined (or an exception was
    # raised). We may also have a value for PYMODELIO_LOCAL if the user has
    # defined it?

    #--------------------------------------------------------------------------
    # Check that PYMODELIO_MAIN is a directory
    #--------------------------------------------------------------------------

    # Check if the variable PYMODELIO_MAIN is a valid path
    if not os.path.isdir(PYMODELIO_MAIN):
        msg = "In %s, PYMODELIO_MAIN is set to %s, but this is not a directory"
        current_value = PYMODELIO_MAIN  # keep it just to display it a below
        del PYMODELIO_MAIN  # Fundamental to force reload of PATHS_FILE later
        raise Exception(msg % (PATHS_FILE, current_value))



    #--------------------------------------------------------------------------
    # Import the PyModelio environment and create it.
    #--------------------------------------------------------------------------
    framework_commons = os.path.join(PYMODELIO_MAIN, "commons")
    if framework_commons not in sys.path:
        # Add the directory containing the core of the PyModelio framework
        # to the python path
        sys.path.insert(0, framework_commons)
    print "Starting pymodelio.core.env.PyModelioEnv from path %s" \
          % framework_commons
    from pymodelio.core.env import PyModelioEnv

    #--------------------------------------------------------------------------
    # Define global functions that will enable accessing modelio global
    # variable from modules at any time.
    #--------------------------------------------------------------------------

    if WITH_MODELIO:
        def getSelectedElements():
            global selectedElements
            return selectedElements

        PyModelioEnv.addGlobalFunction(getSelectedElements)

        def getModelingSession():
            global modelingSession
            return modelingSession

        PyModelioEnv.addGlobalFunction(getModelingSession)

        def getSelection():
            global selection
            return selection

        PyModelioEnv.addGlobalFunction(getModelingSession)


    #--------------------------------------------------------------------------
    # Import modules to inject code and for convenience in the python console
    #--------------------------------------------------------------------------

    from pymodelio.core.env import *

    # make alaocl features available at the top level
    from alaocl import *
    # install jython extensions. In particular instrument JDK collections.
    import alaocl.jython
    # install modelio extensions. In particular instrument modelio collections.
    from alaocl.modelio import *

    from pymodelio.simple import *

    print "PyModelio environment successfully initialized. " \
          "For more information 'print PyModelioEnv.show()'"
    print

    PYMODELIO_INITIALIZED = True
