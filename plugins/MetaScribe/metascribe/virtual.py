# coding=utf-8

# noinspection PyUnresolvedReferences
from org.modelio.api.modelio import Modelio

#----------------------------------------------------------------------------------------
#     Virtual methods for diagrams
#----------------------------------------------------------------------------------------

# noinspection PyUnresolvedReferences
from org.modelio.metamodel.uml.infrastructure import Element as ModelioElement
# noinspection PyUnresolvedReferences
from org.modelio.api.diagram import IDiagramGraphic
# noinspection PyUnresolvedReferences
from org.modelio.api.diagram.dg import IDiagramDG
# noinspection PyUnresolvedReferences
from org.modelio.metamodel.diagrams import AbstractDiagram as ModelioAbstractDiagram
from metascribe.introspection import VirtualRegistry,VirtualMetaFeature

DIAGRAM_SERVICE = Modelio.getInstance().getDiagramService()
ALL_DIAGRAMS = Modelio.getInstance().getModelingSession().findByClass(ModelioAbstractDiagram)
# Should this be computed on demand and refreshed when new diagrams are updated?
ALL_DIAGRAM_HANDLES = map(DIAGRAM_SERVICE.getDiagramHandle,ALL_DIAGRAMS)


def getDisplayingDiagrams(element):
    """ Return all diagrams displaying the element in a graphical form """
    selectedDiagrams = []
    for diagramHandle in ALL_DIAGRAM_HANDLES:
        graphicElements = diagramHandle.getDiagramGraphics(element)
        if len(graphicElements) != 0:
            selectedDiagrams.append(diagramHandle.getDiagram())
    return selectedDiagrams



def getDiagramGraphics(element):
    """ Return all diagram graphics (i.e. DiagramLink, DiagramNode) that are used
        to display this element
    """
    diagramGraphics = []
    for diagramHandle in ALL_DIAGRAM_HANDLES:
        diagramGraphics.extend(diagramHandle.getDiagramGraphics(element))
    return diagramGraphics

def getDiagramNode(d):
    return DIAGRAM_SERVICE.getDiagramHandle(d).getDiagramNode()


def registerVirtualMetaFeatures():
    VirtualRegistry.add(
        VirtualMetaFeature(getDisplayingDiagrams,ModelioElement,                                              'getDisplayingDiagrams',ModelioAbstractDiagram,True))
    VirtualRegistry.add(
        VirtualMetaFeature(getDiagramGraphics,ModelioElement,
                           'getDiagramGraphics',IDiagramGraphic,True))
    VirtualRegistry.add(
        VirtualMetaFeature(getDiagramNode,ModelioAbstractDiagram,
                          'getDiagramNode',IDiagramDG,False))









