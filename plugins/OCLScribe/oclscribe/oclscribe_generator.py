#===================================================================================
# oclscribe_generator
#
# This module generates USEOCL text for the following uml constructs:
#  - Enumeration
#  - Class
#  - AssociationClass
#  - Attribute
#  - Operation
#  - TypedElement
#  - Association
#  - NAryAssciation
#  - Constraint
#  - CommentClass
#  - CommentAttribute
# In each case a function "compileXXX" is provided
#===================================================================================



#-----------------------------------------------------------------------------------
#   Module Interface
#-----------------------------------------------------------------------------------
# Exported symbols for this module. Only these symbols are visible from outside.
# Other symbols are symbols that can be used localy within this module.
#__all__ = [
#  "compileEnumerations",
#  "compileClasses",
#  "compileAssociations",
#  "compileConstraints"
#]



#-----------------------------------------------------------------------------------
#   Module Implementation
#-----------------------------------------------------------------------------------

from org.modelio.metamodel.uml.statik import *
from org.modelio.metamodel.uml.infrastructure import *
from org.modelio.metamodel.mda import Project

    
    
#-----------------------------------
#   XXX Enumeration
#-----------------------------------

def compileEnumeration(enumerationElement):
	return ""

#-----------------------------------
#   XXX Class
#-----------------------------------
 
def compileClass(classElement):
	return ""

  
#-----------------------------------
#   XXX AssociationClass
#-----------------------------------  

def compileAssociationClass(classElement):
	return ""

  
#-----------------------------------
#   XXX Attribute
#-----------------------------------    
def compileAttribute(attributeElement):
	return ""

  
#-----------------------------------
#   XXX Operation
#-----------------------------------    	
def compileOperation(operationElement):
	return ""

  
#-----------------------------------
#   XXX TypedElement
#-----------------------------------    
def compileType (typedElement):
	return ""


#-----------------------------------
#   XXX Association
#-----------------------------------  
def compileAssociation (associationEndElement):
	return ""
	
  
#-----------------------------------
#   XXX NAryAssciation
#-----------------------------------  
def compileNAryAssociation (naryEnd):
	return ""


#-----------------------------------
#   XXX Constraint
#-----------------------------------  
def compileConstraint(constraintElement):
	return ""

#-----------------------------------
#   XXX CommentClass
#-----------------------------------  
def compileCommentClass(commentElement):
	return ""

  
#-----------------------------------
#   XXX CommentAttribute
#-----------------------------------    
def compileCommentAttribute(commentElement):
	return ""

  
  
  
  
  
#-----------------------------------------------------------------------------------
#   Main functions called from client modules
#-----------------------------------------------------------------------------------
  
  
#-----------------------------------
#   XXX Enumerations
#-----------------------------------  
def compileEnumerations(enumerationElements):
	return ""
  
#-----------------------------------
#   XXX Classes
#-----------------------------------  
def compileClasses(classElements):
	return ""

#-----------------------------------
#   XXX Associations
#-----------------------------------  
def compileAssociations(associationElements, nAssociations_list, associationList):
	return ""

#-----------------------------------
#   XXX Constraints
#-----------------------------------  
def compileConstraints(constraintElements):
	return ""
  
print "module oclscribe_generator loaded from",__file__