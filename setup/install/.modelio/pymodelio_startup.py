# coding=utf-8

#---------- get PYMODELIO_MAIN path -------------------------------------------
import os
import sys

# To avoid strange when loading some modules (due to modelio)
# noinspection PyUnresolvedReferences
import encodings # needed


def __deleteCoreModules():
    CoreModules = \
        PyModelioEnv.FRIEND_PYALAOCL_MODULES \
        + PyModelioEnv.MAIN_COMMONS_MODULES
    for moduleName in CoreModules:
        if moduleName in sys.modules:
            # if moduleName == 'pyalaocl.modelio':
            #     try:
            #         pyalaocl.modelio.symbolGroups.deleteFromScope(globals())
            #     except Exception as e:
            #         print "pymodelio_startup: Can't finalize pyalaocl.modelio."
            #         print "                  ", e
            # if 'pyalaocl.modelio.profiles' in sys.modules:
            #     try:
            #         pyalaocl.modelio.profiles.symbolGroups.deleteFromScope(globals())
            #     except Exception as e:
            #         print "pymodelio_startup: Can't finalize pyalaocl.modelio.profiles"
            #         print "                  ", e
            try:
                del sys.modules[moduleName]
                print '%s module deleted from system' % moduleName,
                if moduleName in globals():
                    try:
                        exec ( "del " + moduleName )
                        print 'and scope.'
                    except AttributeError:
                        print '. It was not in scope (AttributeError)'
                    except NameError:
                        print '.'
                else:
                    print '.'
            except Exception as e:
                print 'deletion of %s failed' % moduleName
                print "             ", e

# make sure that the core is reloaded
if 'DEBUG_PYMODELIO_CORE' in globals() \
        and DEBUG_PYMODELIO_CORE:
    __deleteCoreModules()

try:
    # Check if this variable is defined.
    # If yes, the framework has already been initialized.
    # So this file do don't do anything.

    # noinspection PyStatementHasNoEffect PyUnboundLocalVariable
    PYMODELIO_INITIALIZED

    if 'DEBUG_PYMODELIO_CORE' in globals():
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
                                    ".modelio","pymodelio_config.py")


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
        sys.stderr.write( msg % USER_CONFIG_FILE)
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
        del PYMODELIO_MAIN # Fundamental to force reload of PATHS_FILE later
        raise Exception( msg % (PATHS_FILE,current_value) )



    #--------------------------------------------------------------------------
    # Import the PyModelio environment and create it.
    #--------------------------------------------------------------------------
    framework_commons = os.path.join(PYMODELIO_MAIN,"commons")
    if framework_commons not in sys.path:
        # Add the directory containing the core of the PyModelio framework
        # to the python path
        sys.path.insert(0,framework_commons)
    print "Starting pymodelio.core.env.PyModelioEnv from path %s" \
          % framework_commons
    from pymodelio.core.env import PyModelioEnv

    #--------------------------------------------------------------------------
    # Define global functions that will enable accessing modelio global
    # variable from modules at any time.
    #--------------------------------------------------------------------------

    if WITH_MODELIO:
        from pyalaocl import asSeq
        def getSelectedElements():
            global selectedElements
            return asSeq(selectedElements)
        PyModelioEnv.addGlobalFunction(getSelectedElements)

        def getModelingSession():
            global modelingSession
            return modelingSession
        PyModelioEnv.addGlobalFunction(getModelingSession)

        def getSelection():
            global selection
            return asSeq(selection)
        PyModelioEnv.addGlobalFunction(getModelingSession)


    #--------------------------------------------------------------------------
    # Import modules to inject code and for convenience in the python console
    #--------------------------------------------------------------------------

    from pymodelio.core.env import *
    # make pyalaocl features available at the top level
    from pyalaocl import *
    # install jython extensions. In particular instrument JDK collections.
    import pyalaocl.jython
    # install modelio extensions. In particular instrument modelio collections.
    from pyalaocl.modelio import *
    from pyalaocl.modelio.profiles import *
    from pymodelio.simple import *

    print "  PyModelio environment successfully initialized. "
    print "  For more information 'print PyModelioEnv.show()'"

    PYMODELIO_INITIALIZED=True
