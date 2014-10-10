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

# In developement mode use the following snippet to reload this module each time
#
# try: del sys.modules["modelioscriptor"] ; del modelioscriptor
# except: pass
# from modelioscriptor import * 
#
#

from java.lang                                    import Class as JavaClass
from org.modelio.api.modelio                      import Modelio
from org.modelio.metamodel                        import Metamodel
from org.modelio.metamodel.uml.infrastructure     import Element
from org.modelio.vcore.smkernel.mapi              import MClass
from org.modelio.metamodel.analyst                import *
from org.modelio.metamodel.mda                    import *


def theSession():
  """ Return the current session.
      () -> IModelingSession 
  """
  return Modelio.getInstance().getModelingSession()

  
#----------------------------------------------------------------------------
#   Access to model elements
#----------------------------------------------------------------------------
  
def allInstances(classe):
  """ Return the list of all instances of a given metaclass (or submetaclass)
      for the given session. This includes not only the current project
      but also libraries such as predefined types.
      (MClass|Class|String) -> List(MObject) 
      EXAMPLES:  
        allInstances(UseCase)      # return all UseCase
        allInstances(Element)      # return all Elements
        allInstances("UseCase")    # return all UseCase
  """
  if isinstance(classe,basestring):
    return allInstances(getMClass(classe))
  else:
    return theSession().findByClass(classe)

def selectedInstances(classe,att,val):
  """ Return the list of all the instances that have the 
      property set to the given value. 
      NOTE: Not sure how to deal with property that are not string.
      (MClass|Class)*String*String -> List(MObject)
      EXAMPLES
        selectedInstances(DataType,"Name","string")
  """
  return theSession().findByAtt(classe,att,val)
  
def instancesNamed(classe,name):
  """ Return the list of all instances of that have the given name.
      (MClass|Class)*String -> List(MObject)
      EXAMPLES
        instancesNamed(DataType,"string")
  """
  return theSession().findByAtt(classe,"Name",name)

def instanceNamed(classe,name):
  """ Return the only instance that have the given name.
      If there is more than one instance then raise an 
      (MClass|Class)*String -> MObject|NameError
  """
  r = instancesNamed(classe,name)
  if len(r)==1:
    return r[0]
  elif len(r)==0:
    raise NameError("There is no element named '"+name+"'")
  else:
    raise NameError("There are "+str(len(r))+" elements named '"+name+"'") 

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
#   Access to the metamodel
#----------------------------------------------------------------------------

from org.modelio.vcore.smkernel.meta import SmClass
def allMClasses():
  """ Return the list of all known metaclasses as MClass objects.
      () -> [ MClass ]
      EXAMPLE:
        for m in allMClasses(): print m
  """
  return SmClass.getRegisteredClasses()

  
def allMInterfaces():
  """ Return the list of all known metaclasses as Java interfaces.
      () -> [ Class ]
      EXAMPLE:
        for m in allMClasses(): print m
  """
  return map(Metamodel.getJavaInterface,allMClasses())

def getMClass(nameOrMInterfaceOrElement):
  """ Return the MClass corresponding to a name, a java interface
      or an element.
      (Class | String | Element) -> MClass
      EXAMPLES:
        print getMClass(UseCase)
        print getMClass("UseCase")
        print getMClass(myUseCase1)
  """
  if isinstance(nameOrMInterfaceOrElement,Element):
    return nameOrMInterfaceOrElement.getMClass()
  else:
    return Metamodel.getMClass(nameOrMInterfaceOrElement)
  
def getMInterface(nameOrMClassOrElement):
  """ Return the Java Interface corresponding to a name or a MClass
      (MClass | String) -> CLass
      EXAMPLES
        print getMInterface("UseCase")
        print getMInterface(getMClass("UseCase"))
        print getMInterface(instanceNamed(DataType,"string"))
  """
  if isinstance(nameOrMClassOrElement,Element):
    return nameOrMClassOrElement.getMClass().getJavaInterface()
  elif isinstance(nameOrMClassOrElement,basestring):
    return getMClass(nameOrMClassOrElement).getJavaInterface()
  else:
    return nameOrMClassOrElement.getJavaInterface()
  
  
def theMetamodelExtensions():
  """ TODO, Warning this is not a list!
  """
  return theSession().getMetamodelExtensions()  
  

def isKindOf(element,mclassOrMInterface):
  """ Check if the element is a direct  or indirect instance of a MClass 
      or inteface. Use isTypeOf to test if the type is exactly
      the one specified.
      EXAMPLES
        print isKindOf(instanceNamed(DataType,"string"),Element)
        print isKindOf(instanceNamed(DataType,"string"),UseCase)
  """
  if isinstance(mclassOrMInterface,MClass):
    mclassOrMInterface = mclassOrMInterface.getJavaInterface()
  return isinstance(element,mclassOrMInterface)
  
def isTypeOf(element,mclassOrMInterface):
  """ Check if the element has exactly the type specified, not one of
      its subtype. Use isKindOf to test if the type is exactly the one 
      specified.
      EXAMPLES
        print isTypeOf(instanceNamed(DataType,"string"),DataType)
        print isTypeOf(instanceNamed(DataType,"string"),Element)
  """
  if isinstance(mclassOrMInterface,JavaClass):
    mclassOrMInterface = Metamodel.getMClass(mclassOrMInterface)
  return element.getMClass() is mclassOrMInterface
  
#----------------------------------------------------------------------------
#   Access to diagram graphics
#----------------------------------------------------------------------------  

from org.modelio.api.diagram import IDiagramGraphic
from org.modelio.api.diagram.dg import IDiagramDG
from org.modelio.metamodel.diagrams import AbstractDiagram

def allDiagrams(diagramclasse=AbstractDiagram):
  """ Return all diagrams. If a subclass of AbstractDiagram is given then
      return only diagrams of the given type.
      EXAMPLES:
        print allDiagrams()
        print allDiagrams(ClassDiagram)
  """
  return allInstances(diagramclasse)
  

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
  for diagram in allDiagrams():
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
    diagrams = allDiagrams()
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
  return Modelio.getInstance().getEditionService()
  
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