# -*- coding: utf-8 -*-

# modelioscriptor
#
# Simple module to make modelio scripting easier.
# This module provides essentially shortcuts to Modelio API
#
# Author: jmfavre
#
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

# In developement mode use the following snippet to reload this module each
# time
#
# try: del sys.modules["modelioscriptor"] ; del modelioscriptor
# except: pass
# from modelioscriptor import * 
#
#

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
  


  
print "module modelioscriptor loaded from",__file__
