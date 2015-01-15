# coding=utf-8
"""
CoExplorer user interfaces.

This module provides:

* an html interface,
* a textual interface,
* an interactive graphical user interface in the form of a tree.

"""

__all__ = (
    'show',
    'explore',
    'exp,'
)

import images
import introspection
import metascribe.webdoc
import pymodelio.env.gui
import virtual
# noinspection PyUnresolvedReferences
from org.modelio.metamodel.uml.infrastructure import Element as ModelioElement


virtual.registerVirtualMetaFeatures()

def getElementInfo(element):
    return introspection.ElementInfo(element)

def show(x,html=False):
    if introspection.isElement(x):
        print getElementInfo(x).getText()
    elif introspection.isMetaclass(x):
        if html:
            ftempl = "<li>${mclass}.<b>${fname}</b> :"  \
                + "<em>${ftype}</em>${fmult}</li>"
            fsep = ""
            mctempl = "<h3>$mcsig</h3><ul>$mcbody</ul>"
            html = introspection.getMetaclassInfo(x).getText(
                html=True, fTemplate=ftempl,
                mcTemplate=mctempl,
                fsep="")
            pymodelio.env.gui.HtmlWindow(html,width=600,height=800)
        else:
            print introspection.getMetaclassInfo(x).getText(html=html)
    elif introspection.isList(x):
        for item in x:
            show(item)
    else:
        print x


# noinspection PyUnresolvedReferences
from org.eclipse.swt.graphics import Color,Image
# noinspection PyUnresolvedReferences
from org.eclipse.swt.widgets import Display


def explore(x,browser=False,emptySlots=False):
    if browser:
        metamodelHtmlWindow = \
            pymodelio.env.gui.HtmlWindow(title="Modelio Metamodel Guide")
        javadocHtmlWindow = \
            pymodelio.env.gui.HtmlWindow(title="Modelio API Javadoc")

    def _getChildren(data):
        if isinstance(data, introspection.ElementInfo):
            return data.getSlotList(emptySlots=emptySlots)
        elif isinstance(data,introspection.MetaFeatureSlot):
            mv = data.getModelValue()
            if mv.isElement():
                return [getElementInfo(mv.getValue())]
            elif mv.isElementList():
                return map(getElementInfo,mv.getValue())
            else:
                return []

    def _isLeaf(data):
        if isinstance(data, introspection.ElementInfo):
            return False
        elif isinstance(data, introspection.MetaFeatureSlot):
            mv = data.getModelValue()
            if mv.isElement():
                return False
            elif mv.isElementList():
                return False
            else:
                return True

    def _getText(data):
        if isinstance(data, introspection.ElementInfo):
            return data.getSignature()
        elif isinstance(data, introspection.MetaFeatureSlot):
            mv = data.getModelValue()
            if mv.isAtomic():
                return data.getText()
            elif mv.isElementContainer():
                return data.getMetaFeature().getSignature() \
                       + " = [" + str(data.getCard()) + "]"
            else:
                return "???" + unicode(mv)

    def _getImage(data):
        if isinstance(data, introspection.ElementInfo):
            metaclass = data.getMetaclass()
            image = images.getImageFromType(metaclass)
            return image
        elif isinstance(data, introspection.MetaFeatureSlot):
            mv = data.getModelValue()
            if mv.isElement():
                return images.getImageFromName("assoc-1")
            elif mv.isElementList():
                return images.getImageFromName("assoc-n")
            elif mv.isScalar():
                return images.getImageFromType(type(mv.getValue()))
            elif mv.isEnumerationLiteral():
                return images.getImageFromName("enumeration")

    def _getGrayed(data):
        if isinstance(data, introspection.ElementInfo):
            return False
        else:
            return True

    def _getForeground(data):
        if isinstance(data, introspection.ElementInfo):
            return Color(Display.getCurrent(),0,0,150)
        elif isinstance(data, introspection.MetaFeatureSlot):
            mv = data.getModelValue()
            if mv.isElement() or mv.isElementList():
                return Color(Display.getCurrent(),0,100,0)
            else:
                return Color(Display.getCurrent(),0,180,0)

    def onSelection(data):
        if isinstance(data, introspection.ElementInfo):
            metaclass = data.getMetaclass()
            message = str(data)
            metamodelHtmlWindow.setLabel(message)
            javadocHtmlWindow.setLabel(message)
            if issubclass(metaclass,ModelioElement):
                metamodelHtmlWindow.setURL(
                    metascribe.webdoc.getMetaclassMetamodelURL(metaclass))
                javadocHtmlWindow.setURL(
                    metascribe.webdoc.getMetaclassJavadocURL(metaclass))
            else:
                metamodelHtmlWindow.setText("")
                javadocHtmlWindow.setText("")
        elif isinstance(data, introspection.MetaFeatureSlot):
            mv = data.getModelValue()
            print "slot selected with model value:",mv

    try:
        len(x)
    except:
        x = [x]
    pymodelio.env.gui.TreeWindow(
        map(getElementInfo,x),_getChildren,_isLeaf,
               getTextFun=_getText,getImageFun=_getImage,
               getGrayedFun=_getGrayed,
               getForegroundFun=_getForeground,
               onSelectionFun=onSelection if browser else None,
               title="Model/Metamodel CoExplorer")


def exp(x,emptySlots=False):
    explore(x,True,emptySlots)
