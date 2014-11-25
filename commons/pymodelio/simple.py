# -*- coding: utf-8 -*-

#
# Simple module to make modelio scripting easier.
# This module provides essentially shortcuts to Modelio API
##
# Compatibility: Modelio 3.x
# 
# History
#   Version 1.0 - December 04, 2013
#      - functions M1 <--> M2
#      - function theMClass renamed to getMClass
#      - function with MJavaInterface in their name renamed to MInterface
#      - first delivery for a university course
#   Version 0.3 - December 02, 2013
#      - functions for root elements
#      - functions for edition services 
#   Version 0.2 - December 01, 2013
#      - addition of functions for diagram graphics
#   Version 0.1 - November 28, 2013
#      - first version 


# DO NOT DEFINE __all__: THIS WILL BREAK import * statements

# noinspection PyUnresolvedReferences
from org.modelio.api.modelio                      import Modelio
# noinspection PyUnresolvedReferences
from org.modelio.metamodel.analyst                import AnalystProject
# noinspection PyUnresolvedReferences
from org.modelio.metamodel.mda                    import Project,ModuleComponent


def theSession():
  """ Return the current session.
      () -> IModelingSession 
  """
  return Modelio.getInstance().getModelingSession()


#----------------------------------------------------------------------------
#   Access to top level elements
#----------------------------------------------------------------------------
    
def theUMLProject():
  """ Return the UML project.
      () -> Project
  """
  for root in theSession().getModel().getModelRoots():
    if isinstance(root,Project):
      return root
      
def theRootPackage():
  """ Return the root package of the UML project.
      () -> Project
  """
  return theUMLProject().getModel()

  
def theAnalystProject():
  """ Return the analyst project.
      () -> AnalystProject
  """
  for root in theSession().getModel().getModelRoots():
    if isinstance(root,AnalystProject):
      return root
      
def theLocalModule():
  """ Return the Local Module
      () -> ModuleComponent
  """
  for root in theSession().getModel().getModelRoots():
    if isinstance(root,ModuleComponent):
      return root



#----------------------------------------------------------------------------
#   Access model factories
#----------------------------------------------------------------------------
      
def theUMLFactory():
  """ Return the factory that allow to create UML and indeed BPMN elements
      The function theBPMNFactory() return the same IUMLModel
      () -> IUmlModel
  """
  return theSession().getModel()

def theBPMNFactory():
  """ Return the factory that allow to create BPMN and indeed UML elements
      Same as theUMLFactory
      () -> IUmlModel
  """
  return theSession().getModel()
  
def theAnalystFactory():
  """ Return the factory that allow to create Analyst elements
      () -> IAnalystModel
  """
  return theSession().getRequirementModel()

  
  

#----------------------------------------------------------------------------
#   Access to diagram graphics
#----------------------------------------------------------------------------  

# noinspection PyUnresolvedReferences
from org.modelio.api.diagram import IDiagramGraphic
# noinspection PyUnresolvedReferences
from org.modelio.api.diagram.dg import IDiagramDG
# noinspection PyUnresolvedReferences
from org.modelio.metamodel.diagrams import AbstractDiagram


  

def theDiagramService():
  return Modelio.getInstance().getDiagramService()
  
def allStyleHandles():
  """ TODO 
  """
  return theDiagramService().listStyles()
  
def theAutoDiagramFactory():
  """ TODO
  """
  return theDiagramService().getAutoDiagramFactory()
  
def getDiagramHandle(diagram):
  return theDiagramService().getDiagramHandle(diagram)
  
def getDisplayingDiagrams(element):
  """ Return all diagrams displaying the element in some graphical form
      Element -> [ AbstractDiagram ]
      EXAMPLES
        print getDisplayingDiagrams(myclass)
  """
  selectedDiagrams = []
  for diagram in AbstractDiagram.allInstances():
    handle = getDiagramHandle(diagram)
    graphicElements = handle.getDiagramGraphics(element)
    if len(graphicElements)!=0:
      selectedDiagrams.append(handle.getDiagram())
    handle.close()
  return selectedDiagrams

def getDiagramGraphics(element,diagramOrDiagramsOrNone=None):
  """ Return all diagram graphics (i.e. DiagramLink, DiagramNode) that are used
      to display the given element. If a second parameter is given then
      only the search is restricted to the given diagram(s) 
      (Element,(AbstractDiagram|[AbstractDiagram]|?) -> [ AbstractDiagram ]      
      EXAMPLES
        print getDiagramGraphics(e)
        print getDiagramGraphics(e,mydiagram)
        print getDiagramGraphics(e,[diagram1,diagram2,diagram3])
  """
  if diagramOrDiagramsOrNone is None:
    diagrams = AbstractDiagram.allInstances()
  elif isinstance(diagramOrDiagramsOrNone,AbstractDiagram):
    diagrams = [ diagramOrDiagramsOrNone ]
  else: 
    diagrams = diagramOrDiagramsOrNone
  diagramGraphics = []
  for diagram in diagrams:
    handle = getDiagramHandle(diagram)  
    diagramGraphics.extend(handle.getDiagramGraphics(element))
    handle.close()
  return diagramGraphics
  
def saveDiagram(diagram,filename):
    """ Save a given diagram in as an image file
    """
    extension = filename[filename.rindex('.')+1:]
    handle=getDiagramHandle(diagram)
    handle.saveInFile(extension,filename,0)
    handle.close()

  
#----------------------------------------------------------------------------
#   Access to editors
#----------------------------------------------------------------------------  

def theEditionService():  
  """ The edition service
  """
  return Modelio.getInstancalle().getEditionService()
  
def openEditor(diagramOrArtifactOrExternDocument):
  """ Open an editor window for the given diagram, artifact
      or extern document. Note that the diagram is not "selected" in 
      the sense that it does not becomes the current displayed diagram,
      unless obviously if the diagram was closed before.
      (AbstractDiagram|Artifact|ExternDocument) -> ()
      EXAMPLES:
        openEditor(myclass)
        openEditor(myartifact)
        openEditor(mydocument)
      SEE
        
  """
  theEditionService().openEditor(diagramOrArtifactOrExternDocument)  

#----------------------------------------------------------------------------
#   Access to the selection
#----------------------------------------------------------------------------

def setSelection(elementOrElements):
  """ Change the current selection with an element or a list of elements
  """
  Modelio.getInstance().getNavigationService().fireNavigate(elementOrElements)



#----------------------------------------------------------------------------
#   Metamodel import
#----------------------------------------------------------------------------

import pyalaocl.modelio
from pyalaocl.modelio import *

import pyalaocl.modelio.profiles
from pyalaocl.modelio.profiles import *




#----------------------------------------------------------------------------
#   Metamodel extensions
#----------------------------------------------------------------------------


# noinspection PyUnresolvedReferences
from pyalaocl.injector import readOnlyPropertyOf
# noinspection PyUnresolvedReferences
from org.modelio.metamodel.uml.statik import Class as IClass
# noinspection PyUnresolvedReferences
from org.modelio.metamodel.uml.statik import Association as IAssociation
# noinspection PyUnresolvedReferences
from org.modelio.metamodel.uml.statik import AggregationKind
# noinspection PyUnresolvedReferences
from org.modelio.metamodel.uml.statik import AssociationEnd as IAssociationEnd


#------------------------------------------------------------------------------
#   Class
#------------------------------------------------------------------------------

@readOnlyPropertyOf(IClass, 'simple')
def isAssociationClass(self):
    return self.linkToAssociation is not None


@readOnlyPropertyOf(IClass, 'simple')
def asAssociation(self):
    if self.isAssociationClass:
        return self.linkToAssociation.associationPart
    else:
        return None

#------------------------------------------------------------------------------
#   Association
#------------------------------------------------------------------------------

@readOnlyPropertyOf(IAssociation, 'simple')
def sourceEnd(self):
    return self.end[1]


@readOnlyPropertyOf(IAssociation, 'simple')
def targetEnd(self):
    return self.end[0]


@readOnlyPropertyOf(IAssociation, 'simple')
def isComposition(self):
    return self.end.exists(
        lambda e:e.aggregation == AggregationKind.KINDISCOMPOSITION)


@readOnlyPropertyOf(IAssociation, 'simple')
def isTowardsComponent(self):
    return self.sourceEnd.isComposition


@readOnlyPropertyOf(IAssociation, 'simple')
def isTowardsComposite(self):
    return self.targetEnd.isComposition


@readOnlyPropertyOf(IAssociation, 'simple')
def isAggregation(self):
    return self.end.exists(
        lambda e: e.aggregation == AggregationKind.KINDISAGGREGATION)


@readOnlyPropertyOf(IAssociation, 'simple')
def isTowardsAggregated(self):
    return self.sourceEnd.isAggregated


@readOnlyPropertyOf(IAssociation, 'simple')
def isTowardsAggregate(self):
    return self.targetEnd.isAggregated


@readOnlyPropertyOf(IAssociation, 'simple')
def isBiNavigable(self):
    return self.sourceEnd.navigable and self.targetEnd.navigable


@readOnlyPropertyOf(IAssociation, 'simple')
def isUniNavigable(self):
    return self.sourceEnd.navigable != self.targetEnd.navigable


@readOnlyPropertyOf(IAssociation, 'simple')
def isNotNavigable(self):
    return not (self.sourceEnd.navigable) and not(self.targetEnd.navigable)


@readOnlyPropertyOf(IAssociation, 'simple')
def isAssociationClass(self):
    return self.linkToClass is not None


@readOnlyPropertyOf(IAssociation, 'simple')
def asClass(self):
    if self.isAssociationClass:
        return self.linkToClass.classPart
    else:
        return None





#------------------------------------------------------------------------------
#   AssociationEnd
#------------------------------------------------------------------------------


@readOnlyPropertyOf(IAssociationEnd, 'simple')
def actualTarget(self):
    """ Return always the target class to which the association end is
    attached. The 'target' property is defined only if the property is
    navigable, otherwise it returns None.
    """
    if self.isNavigable:
        return self.target
    else:
        return self.opposite.source

@readOnlyPropertyOf(IAssociationEnd, 'simple')
def nameOrDefault(self):
    if self.name != '':
        return self.name
    else:
        class_name = self.actualTarget.name
        return class_name[0].lower()+class_name[1:]


@readOnlyPropertyOf(IAssociationEnd, 'simple')
def isSourceEnd(self):
    return self.association.sourceEnd is self


@readOnlyPropertyOf(IAssociationEnd, 'simple')
def isTargetEnd(self):
    return self.association.targetEnd is self


@readOnlyPropertyOf(IAssociationEnd, 'simple')
def isComposition(self):
    return self.aggregation == AggregationKind.KINDISCOMPOSITION


@readOnlyPropertyOf(IAssociationEnd, 'simple')
def isAggregation(self):
    return self.aggregation == AggregationKind.KINDISAGGREGATION


@readOnlyPropertyOf(IAssociationEnd, 'simple')
def isCompositionOpposite(self):
    return self.opposite.isComposition


@readOnlyPropertyOf(IAssociationEnd, 'simple')
def isAggregationOpposite(self):
    return self.opposite.isComposition



