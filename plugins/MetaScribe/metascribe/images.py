# coding=utf-8
"""
Provides icons for metaclasses and other elements.

This module extends modelio image service.
"""

__all__ = (
    'getImageFromType',
    'getImageFromName',
)

# noinspection PyUnresolvedReferences
from org.modelio.api.modelio import Modelio
from metascribe.introspection import getNameFromType
from pymodelio.gui import ImageProvider


#---- Extension of the Modelio' Image Service -----------------------
# Modelio provide images only for subclass of element
# Here we provide more images for other types.
# This includes both basic types, but also graphics, etc.

class ClassImageProvider(ImageProvider):
    """ Provide some images for types.
        We first try to check if there is an image corresponding exactly
        to the name of the type (unqualified). If this is not the case then
        the we search in a class root path in a sequential order. The first
        class which is a superclass of return the image. That is, the types
        given as a path should be from the most specific one, to the most
        general one.
    """

    def __init__(self,resourcePath="",classSearchPath=()):
        ImageProvider.__init__(self,resourcePath)
        # the order in which one will select the image. Contains a list of classes
        self.classSearchPath = classSearchPath

    def appendClassesToSearchPath(self,classes):
        self.classSearchPath.append(classes)

    def getImageFromType(self,classe):
        # first try to get the image with the exact name of the type
        image = self.getImageFromName(getNameFromType(classe,noPath=True))
        if image is not None:
            return image
        else:
            # not found, then search in the class root path
            for class_root in self.classSearchPath:
                if issubclass(classe,class_root):
                    image = self.getImageFromName(
                        getNameFromType(class_root,noPath=True))
                    if image is not None:
                        return image
            return None

    def getImageFromObject(self,object):
        r = self.getImageFromType(type(object))
        return self.getImageFromType(type(object))

# TODO: Other useful classes to consider
# LocalPropertyTable
# MStatus
# IStyle ?
# StyleKey ?
# FactoryStyle ?



# noinspection PyUnresolvedReferences
from org.modelio.api.diagram import IDiagramNode,IDiagramLink,ILinkPath
# noinspection PyUnresolvedReferences
from org.modelio.api.diagram.style import IStyleHandle
# noinspection PyUnresolvedReferences
from org.eclipse.draw2d.geometry import Rectangle,Dimension,Point
# noinspection PyUnresolvedReferences
from java.util import UUID
# noinspection PyUnresolvedReferences
from org.modelio.vcore.smkernel.mapi import MClass,MAttribute,MDependency

CLASSES_SEARCH_ORDER = [
    IDiagramNode,
    IDiagramLink,
    ILinkPath,
    IStyleHandle,
    Rectangle,
    Dimension,
    Point,
    UUID,
    MClass,
    MAttribute,
    MDependency,
]

import os

RES_DIRECTORY = os.path.join(os.path.dirname(__file__),'..','res')
NAVIGATOR_IMAGE_PROVIDER = ClassImageProvider(
    resourcePath=RES_DIRECTORY,
    classSearchPath=CLASSES_SEARCH_ORDER)


def getImageFromType(metaclass):
    """ return the image corresponding to a metaclass or None if no image is available
    """
    try:
        r = Modelio.getInstance().getImageService() \
            .getMetaclassImage(metaclass)
        return r
    except:
        return NAVIGATOR_IMAGE_PROVIDER.getImageFromType(metaclass)

def getImageFromName(name):
    return NAVIGATOR_IMAGE_PROVIDER.getImageFromName(name)
