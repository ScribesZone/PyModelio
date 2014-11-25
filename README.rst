While the open source environment Modelio allows to develop extensions in the
form of so-called '**modules**' written in java, it does not provide support
to develop non-trivial extensions in jython/python. This is exactly what
the PyModelio framework is for: PyModelio allows to develop what we call 
'**plugins**' in jython/python. 

PyModelio is based on of the best features of Modelio, the jython interpreter. 
With modelio alone, one can write simple macros in jython. While this is
handy for very simple task, macro development could rapidly becomes difficult
when complexity raises. PyModelio aims to solve this and make it possible to
offer the developer wishing to entend modelio to choose between:

* developing 'modules' in java, 
* developing 'plugins' in jython/python. 

The term "plugin" (which is not a modelio  concept) is used here to refer to 
consistent set of jython scripts with possibly additional resources. While 
scripts are installed as "macros" in modelio some other are called by these 
macros. While macros are usually in a  single file, we use here full fledged 
modular development as allowed by  jython/python including the possibility to 
use arbitrary java libraries. 

The alternative to develop what we called "plugin" in jython, is to develop 
modelio modules in java. This requires much more effort though. 

Modelio provides a lot of features for the development of plugin in java but no
facilities is given for developing in python beyond simple monolithic macro
development.

This PyModelio framework supports the following features:

* support for code development/execution outside modelio workspace macro
  directory.

* support for 'ala' OCL operations thanks to PyAlaOCL python package.

* automatic instrumentation/extension of modelio metamodel with operations
  such as those to support AlaOCL.

* support so that the developer can themselves instrument modelio metamodel
  for adding additional methods computing derived information for instance.

* modular development of python modules with reloading features in
  development mode.

* inclusion of regular python and java libraries thanks to python/java path
  management.

* automatic definition of a global environment for jython interpreter, with
  globals symbols for project profiles.

* support for directory management allowing to develop code independently
  from execution.

* finding the local plugins directory where more features can be installed.

* extension of the python path and java path to reuse existing pure python or
  java libraries.

* access to modelio global variables (selection, selectedElements,
  modelingSession from inside modules.

* set the working directory to a local directory so that macros can read and
  write in a well defined place. When using Modelio the working directory
  is set to the Modelio installation directory. This is definitively not a good
  place to write files.

* allow the definition of modelio styles in plugins and automatically
  register these styles.
