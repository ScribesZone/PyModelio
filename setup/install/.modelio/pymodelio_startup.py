#---------- get PYMODELIO_MAIN path -------------------------------------------------
import os
import sys

try:
    # Check if this variable is defined.
    # If yes, the framework has already been initialized.
    # So this file do don't do anything.
    PYMODELIO_ENV

except:
    # This is the first time this file is executed, or at least it was never
    # executed completely because of errors.
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
        INITIAL_PYTHON_PATH
    except:
        # Save the path for further possible rollbacks
        INITIAL_PYTHON_PATH = sys.path
    framework_commons = os.path.join(PYMODELIO_MAIN,"commons")
    if framework_commons not in sys.path:
        # add the directory containing the core of the PyModelio framework to the python path
        sys.path.append(framework_commons)


    #------------------------------------------------------------------------------------
    # Import the PyModelio environment and create it.
    #------------------------------------------------------------------------------------
    print "Loading pymodelio.core.env.PyModelioEnv from path %s" % framework_commons
    from pymodelio.core.env import PyModelioEnv
    print "Initializing PyModelio environment ... "
    PYMODELIO_ENV = PyModelioEnv(INITIAL_PYTHON_PATH,PYMODELIO_MAIN,PYMODELIO_LOCAL,WITH_MODELIO)
    print "ok"

    #------------------------------------------------------------------------------------
    # Import some modules for convenience in the python console (or for other reasons)
    #------------------------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    import encodings # needed to avoid strange when loading some modules (due to modelio)

