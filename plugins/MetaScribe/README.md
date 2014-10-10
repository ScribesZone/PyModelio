Target audience
===============
This modelio plugin is  mainly dedicated to developers who need to understand modelio Metamodel, for instance to develop scripts or modules. It allows the co-exploration of a model and the corresponding metamodel.

Description
===========
This macro allows to explore the set of selected elements by navigating at the
same time in the model and the metamodel. While Modelio' model explorer and property
sheets presents a "user oriented" view of the model, the CoExplorer will present
a view strictly in line with the actual metamodel. 
The set of all (non empty) features associated with each element is displayed,
allowing the navigation to continue. Note that the tree is virtually infinite and
that there is currently no indication that an element has been already visited.
The methods followed are those of the form getXXX(), isXXX() and toString() with no
parameters. A few "virtual" methods which do not have direct correspondance in modelio
are also added, in particular to enable navigation to and within diagrams.
The co-explorer allows to navigate at the same time the model
and discover a slice of the metamodel, the slice that is useful for the model at hand.
The explorer not only allow to explore ModelElement, but also other Java entities,
and interestingly enough the DiagramGraphic elements. In modelio graphical entities
are not modeled, but the exploration is made possible.

History
=======
* Version 1.3 
  * refactoring and integration to ModelioScribes framework and MetaScribe
* Version 1.2
* Version 1.1 - December 02, 2013
  * addition of some messages  when the macro starts
  * use modelioscriptor
  * changes in startup 
* Version 1.0 - October 31, 2013
  * first public realease
  
  
  #
# CoExplorer
#
# Model/Metamodel co-explorer for Modelio.
#
# Author: jmfavre
#
# Compatibility: Modelio 3.x
#

# Installation:
#   This script should be installed as a workspace macro using standard modelio procedure
#   to add macros. The options to use are the following options:
#      - "Applicable on" : No Selection. The macro is application on any kind of element
#      - "Show in contextual menu" : YES
#      - "Show in toolbar" : YES
#   This script is based on the content of the "lib" directory which must be copied manually
#   in the same directory as this very file. That is, in the directory where this file
#   CoExplorer.py will be installed by modelio through the standard macro installation procedure.
#   Ultimately we should have the following structure 
#          CoExplorer.py             <--- this very file
#             lib/
#                 introspection.py
#                 misc.py
#                 modelioscriptor.py
#                 ...                <--- possibly other jython modules
#                 res/
#                     assoc-1.gif
#                     assoc-n.gif
#                     ...            <--- other resources.
#
