#===================================================================================
# oclscribe
#
# This module provides the interface for the OCLScribe macros
# Currently there is only one macro:
#  - generate_ocl
# For each macro XXX there is a function do_XXX which is called when the macro is
# applied.
#===================================================================================

#---------------------------------------------------------------------------
# GUI : 
# The OCL output is generated in a html window
#---------------------------------------------------------------------------
from org.eclipse.swt import SWT
from org.eclipse.swt import *
from org.eclipse.swt.widgets import Text, Composite
from org.eclipse.swt.layout import FillLayout
from org.eclipse.swt.widgets import Shell,Display,Label,Button,Listener
from org.eclipse.swt.browser import Browser
from org.eclipse.swt.layout import GridData,GridLayout
from org.eclipse.swt.custom import ScrolledComposite
from org.eclipse.swt.graphics import Color, Image
class USEWindow(object):
  def __init__(self, title= None, toDisplay= None):


    parentShell = Display.getDefault().getActiveShell()
    self.window = Shell(parentShell, SWT.CLOSE | SWT.RESIZE)
    self.window.setText(title)
    self.window.setLayout(FillLayout())
    self.window.setSize (self.window.computeSize(1400, 500))
    self.text = Browser(self.window, SWT.NONE)
    self.text.setText( \
              "<html><header><style>" +
              "<!--.tab { margin-left: 40px;} .tab2 { margin-left: 80px; }" + 
              " .tab3 { margin-left: 120px; }.tab4 { margin-left: 160px; }-->" +
              "</style></header><body><div style=\"overflow: auto;\">" + 
              toDisplay + "</div></body></html>")
    self.window.open ()
        
#---------------------------------------------------------------------------
#  Process the selection
#---------------------------------------------------------------------------
from org.modelio.metamodel.uml.statik import *
from org.modelio.metamodel.uml.infrastructure import *
from org.modelio.metamodel.mda import Project
from oclscribe_generator import compileEnumerations
from oclscribe_generator import compileClasses
from oclscribe_generator import compileAssociations
from oclscribe_generator import compileConstraints


def compileSelectedElements(selectedElements):
  toDisplay = ""
  nAssociations_list = []
  associationList = []
  modelElement  = selectedElements.get(0)
  while not isinstance(modelElement, Project):
    modelElement = modelElement.getCompositionOwner()
  toDisplay += "<b>model </b>" +modelElement.getName() + "<br><br>"
  toDisplay += "<b>--enumerations</b><br>"
  for selectedEnumerations in selectedElements:
    toDisplay += compileEnumerations(selectedEnumerations)
  toDisplay += "<b>--classes</b><br>"
  for selectedClasses in selectedElements:
    toDisplay += compileClasses(selectedClasses)
  toDisplay = toDisplay +  "<b>--associations</b><br>"
  for selectedAssociations in selectedElements:
    toDisplay += compileAssociations(selectedAssociations, nAssociations_list, associationList)  
  toDisplay = toDisplay +  "<b>-- OCL constraints</b><br>"
  for selectedConstraints in selectedElements:
    toDisplay = toDisplay + compileConstraints(selectedConstraints)
  return toDisplay

  
#---------------------------------------------------------------------------
#  Macro definition
#---------------------------------------------------------------------------
def macro_generate_ocl(scribeexec): 
  if (scribeexec.selectedElements.size() > 0):
    toDisplay = compileSelectedElements(scribeexec.selectedElements)
    USEWindow(title = "USE Generation", toDisplay = toDisplay)
  else:
    USEWindow(title = "USE Code Generation", toDisplay = "No Element has been selected") 