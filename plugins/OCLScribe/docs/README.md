OCLScribe 
=========
This script allows the generation of an USE OCL textual syntax from a modelio model. It also inclused a reverse engineering feature allowing to create a modelio model from a ocl model. 

Forward engineering of the model
--------------------------------
The structural part of the model (class, attribute, operation, association) is used to generate the structure of the USE OCL model. Notes are used in modelio to describe the OCL constraints (preconditions, postconditions, invariants). These constraints are generated in the output in the right place according to the context of the note.

Reverse engineering of the model
--------------------------------
To avoid building a full parser for USE OCL syntax, the reverse engineering feature is based on the command "help model" of use ocl. This command flushes in a standard formatted way the content of a model. This methods present the following drawbacks:
* all comments are lost
* formatting is lost. This is not a problem for the structure but all constraints are on a single line.
* some variables are introduced in the constraints. The representation corresponds to an internal representation


