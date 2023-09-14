# coding=utf-8



# FIXME
# When selecting a element in a diagram the folowing code break
# the explorer:
#   x = selection.getFirstElement()
#   print(x)
#   print ":", type(x)
#   print dir(x)
# raise this exception:
# AttributeError: type object 'java.util.List' has no attribute 'getActualTypeArguments' in <script> at line number 10
# Traceback (most recent call last):
#   File "<script>", line 10, in <module>
#   File "C:\DEV\Modelio3WorkspaceGenOCL-G99\macros\lib\introspection.py", line 1146, in explore
#     TreeWindow(map(getElementInfo,x),_getChildren,_isLeaf, \
#   File "C:\DEV\Modelio3WorkspaceGenOCL-G99\macros\lib\introspection.py", line 1032, in getElementInfo
#     info = ElementInfo(element)
#   File "C:\DEV\Modelio3WorkspaceGenOCL-G99\macros\lib\introspection.py", line 964, in __init__
#     self.metaclassInfo = getMetaclassInfo(self.metaclass)
#   File "C:\DEV\Modelio3WorkspaceGenOCL-G99\macros\lib\introspection.py", line 626, in getMetaclassInfo
#     info = MetaclassInfo(metaclass)
#   File "C:\DEV\Modelio3WorkspaceGenOCL-G99\macros\lib\introspection.py", line 584, in __init__
#     self.metaFeatures = getMetaFeatures(metaclass)
#   File "C:\DEV\Modelio3WorkspaceGenOCL-G99\macros\lib\introspection.py", line 567, in getMetaFeatures
#     javaMethodInfos = map(_getJavaMethodInfo,javaMethods )
#   File "C:\DEV\Modelio3WorkspaceGenOCL-G99\macros\lib\introspection.py", line 431, in _getJavaMethodInfo
#     if len(returnType.getActualTypeArguments()) != 0:
# AttributeError: type object 'java.util.List' has no attribute 'getActualTypeArguments'
#
# metascribe_introspection
#
# Model/Metamodel co-explorer for Modelio.
#
# Author: jmfavre
#
# Compatibility: Modelio 2.x, Modelio 3.x
#
# 
# History
#   Version 1.2 - December 04, 2013
#      - addition of a function "exp" as a shortcut to explore with html
#   Version 1.1 - December 03, 2013
#      - support for "metamodel" and "javadoc" browsing
#      - explore(element,browser=True)
#   Version 0.5 - October 30, 2013
#      - icons for Modelio 3' metamodel elements
#      - refactoring
#      - some virtual features added for diagram exploration
#   Version 0.4 - October 29, 2013
#      - better icons and colors for improved navigation
#   Version 0.3 - October 28, 2013
#      - port to Modelio 3 
#   Version 0.2 - October 25, 2013
#      - addition of SWT GUI for the co-explorer
#   Version 0.1 - October 25, 2013
#      - first version for Modelio 2.2
#      - basic functions
#      - showInfo functions

#-----------------------------------------------------------------------------------
#   Interface
#-----------------------------------------------------------------------------------
# exported symbols for this module

__all__ = [

    "getMetaclassFromName",
    "getNameFromMetaclass",
    "isMetaclass",
    "isEnumeration",
    "getNameFromType",
    "getSubMetaclasses",
    "getSuperMetaclasses",
    "MetaFeature",
    "getMetaFeatures",

    "MetaclassInfo",
    "getMetaclassInfo",

    "isElement",
    "isElementList",
    "isScalar",
    "isEnumerationLiteral",
    "isAtomic",
    "getElementId",
    "getElementNameOrId",
    "getElementSignature",

    "getMetaclass",
    "MetaFeatureSlots",
    "getMetaFeatureSlots",

    "ElementInfo",
    "getElementInfo",

    "getAllInstances",
    "getSelectedInstances",
    "getModelRoot",
    "getElementParent",
    "getElementParents",
    "getElementPath",

    "getDiagramContainingElement",
]



#-----------------------------------------------------------------------------------
#   Realisation
#-----------------------------------------------------------------------------------

import pyalaocl

# important as these modules instrument java classes
# noinspection PyUnresolvedReferences
import pyalaocl.jython # DO NOT REMOVE
# important as these modules instrument java classes
# noinspection PyUnresolvedReferences
import pyalaocl.modelio # DO NOT REMOVE

# noinspection PyUnresolvedReferences
from org.eclipse.core.runtime import IAdaptable




# noinspection PyUnresolvedReferences
from org.modelio.metamodel.uml.infrastructure import Element as ModelioElement
# noinspection PyUnresolvedReferences
from org.modelio.api.modelio import Modelio

MODELIO = Modelio.getInstance()
METAMODEL_SERVICE = MODELIO.getMetamodelService()
MODELING_SESSION = MODELIO.getModelingSession()

# useful for python introspection
def _isPythonBuiltin(name):
    return name.startswith('__') and name.endswith('__')




#------------------------------------------------------------------------------
#   Modelio metaclass (in fact meta interfaces) <--> string
#------------------------------------------------------------------------------

def getMetaclassFromName(metaclassName):
    """
    Get the Modelio Metaclass inheriting from ModelioElement and
    corresponding to the given name of a metaclass.
    Return None if the name provided is not the name of a metaclass
    :param metaclassName: the name of a modelio metaclass (e.g. "UseCase")
        or an arbitrary string
    :type metaclassName: str
    :return: The java interface corresponding the metamclass (e.g. the
        interface IUseCase) or None if the name is not valid.
    :rtype:None|java.lang.Class
    """
    return METAMODEL_SERVICE.getMetaclass(metaclassName)

# noinspection PyUnresolvedReferences
from java.lang import Class as JavaLangClass




def getNameFromMetaclass(metaclass):
    """
    Get the name of a metaclass or a java class or a type.
    """
    # TODO
    if issubclass(metaclass,ModelioElement):
        name = METAMODEL_SERVICE.getMetaclassName(metaclass)
    elif metaclass is JavaLangClass:
        name = "java.lang.Class"
    else:
        try:
            name = unicode(metaclass.getCanonicalName())
        except:
            name = unicode(str((metaclass)))
    return name


def isJavaClass(x):
    return isinstance(x,java.lang.Class)


def isMetaclass(x,justInterfaces=False):
    """ return true if the argument is a metaclass or a implementation of a metaclass
    """
    return isJavaClass(x) \
           and getNameFromMetaclass(x) is not None \
           and (not justInterfaces or x.isInterface())

def isEnumeration(x):
    """ return true if x is an enumeration type
    """
    try:
        return issubclass(x,java.lang.Enum)
    except:
        return False


# noinspection PyUnresolvedReferences
from java.util import Collection as JavaCollection
from array import array

# FIXME: Generalizationto alaocl any Collection
# FIXME: support for array.array required
#     solution: a.tolist() for the conversion
#               a.typecode for the type of the component of the array
def isList(x):
    # is it enough?
    return isinstance(x,list) \
           or isinstance(x,JavaCollection) \
           or isinstance(x,pyalaocl.Seq) #\
           #or isinstance(x,array.array)


def getNameFromType(t, noPath=True):
    """ get name from a type, i.e. a metaclass or a basic type
    """
    if t is java.lang.String:
        name = "string"
    elif isEnumeration(t):
        # enumeration type are NOT interfaces in modelio api and are named
        # like com.modeliosoft.modelio.api.model.uml.statik.ObVisibilityModeEnum
        # We remove the path, leaving ObVisibilityModeEnum
        name = t.getCanonicalName().split('.')[-1]
    else:
        try:
            name = getNameFromMetaclass(t)
        except:
            name = None
        if name is None:
            try:
                name = t.__name__
            except:
                try:
                    name = t.name
                except:
                    try:
                        name = t.getName()
                    except:
                        try:
                            name = t.toString()
                        except:
                            name = "<unamed type>"
    if noPath:
        name = name.split('.')[-1]
    return unicode(name)




def getSubMetaclasses(metaclass):
    """ returns the list of direct subMetaclasses of a metaclass starting
    """
    return METAMODEL_SERVICE.getInheritingMetaclasses(metaclass)

#import types


def getSuperMetaclasses(metaclass,inclusive=True):
    """ This function is intended to be used primarily with Modelio java metaclass,
        either implementation or interface, but in all cases that are below Element.
        If inclusive=True includes the metaclass at the beginning.
    """
    metaclasses = [metaclass] if inclusive else []
    if issubclass(metaclass,ModelioElement):
        # for modelio classes, the algorithm below use the fact that until Element
        # there is only one interface
        current = metaclass
        finished = current is ModelioElement
        while not finished:
            superInterfaces = current.getInterfaces()
            if len(superInterfaces) == 1:
                current = superInterfaces[0]
                metaclasses.append(current)
            finished = len(superInterfaces) != 1 or current is ModelioElement
    return metaclasses
    # The code below was working for Modelio 2.x but not anymore for modelio because of
    # problem importing some modules
    # ------------------------------------------
    # not executed
    # pythonClasses = inspect.getmro(metaclass)
    # javaInterfaces = filter(
    #                   lambda x:x.isInterface(),
    #                   excluding(pythonClasses,types.ObjectType))
    # metaClasses = filter(
    #              lambda x:getNameFromMetaclass(x) is not None and x is not IAdaptable,
    #              javaInterfaces)
    # return metaClasses if inclusive else metaClasses[1:]


# SPECIAL_FEATURES = [ 
#  "toString","hashCode","compareTo","wait",
#  "accept",
#  "notify","notifyAll",
#  "class","getClass",
#  "delete","getmodifDate","isValid",
#  "hid","getHid","lid","getLid","getMetaclassId","sessionId","getSessionId","getElementStatus"]
# def _isSpecialFeature(name): return name in SPECIAL_FEATURES

# noinspection PyUnresolvedReferences
import java.lang.reflect.Member
import re


def _getJavaMethods(javaClass,inherited=False,regexp=None,
                    argTypes=None,methodFilterFun=None,
                    natives=False):
    """ returns java methods from a metaclass
        regexp : None or a regular expression to filter method names (e.g. "^get|is")
        methodFilterFun : None or a predicate on a java.lang.reflect.Method object that will be used to filter methods
    """
    try:
        javaMethods = pyalaocl.Seq.new(javaClass.getMethods()) if inherited \
                        else pyalaocl.Seq.new(javaClass.getDeclaredMethods())
    except:
        # it seems that the code above fail in some case
        javaMethods = pyalaocl.Seq()
    if not natives:
        # remove methods starting with _ which seems to be natives ones
        # (should be improved using getModifiers instead ...)
        #-javaMethods = reject(lambda m:m.getName().startswith('-'),javaMethods)
        javaMethods = javaMethods.reject(
            lambda m:m.getName().startswith('-'))
    if regexp is not None:
        #javaMethods = filter(lambda m:re.match(regexp,m.getName()),javaMethods)
        javaMethods = javaMethods.select(
            lambda m:re.match(regexp,m.getName()) is not None)
    if argTypes is not None:
        javaMethods = javaMethods.select(
            lambda m:list(m.getParameterTypes()) == list(argTypes))
    if methodFilterFun is not None:
        javaMethods = javaMethods.select(methodFilterFun)
    return javaMethods


import types
# noinspection PyUnresolvedReferences
from java.util import List as JavaUtilList

# noinspection PyUnresolvedReferences
from org.eclipse.emf.common.util import EList
# noinspection PyUnresolvedReferences
from org.modelio.vcore.smkernel import SmList as ModelioList


def isCollectionType(x):
    return x in LIST_TYPES


LIST_TYPES = [ModelioList,JavaUtilList,types.ListType,EList]


def _getJavaMethodInfo(javaMethod):
    classe = javaMethod.getDeclaringClass()
    name = javaMethod.getName()
    parameterTypes = list(javaMethod.getParameterTypes())
    returnType = javaMethod.getGenericReturnType()
    # check if the return type is a list,
    # in which case this is a multivalued association end
    if javaMethod.getReturnType() in LIST_TYPES:
        multiple = True
        try:
            if len(returnType.getActualTypeArguments()) != 0:
                returnType = returnType.getActualTypeArguments()[0]
            else:
                returnType = javaMethod.getReturnType()[0].getBounds()[0]
        except:
            returnType = None
    else:
        multiple = False
    return (classe,name,parameterTypes,returnType,multiple)



















from string import Template


class MetaFeature(object):
    """ MetaFeature are methods of Metaclass.
        To be more precise only the getter/is functions with no parameters are
        selected
    """

    def __init__(self,metaclass,name,type,multiplicity=False):
        self.metaclass = metaclass
        self.name = name
        self.type = type
        self.isAssociationEnd = isMetaclass(self.type)
        self.isEnumeration = isEnumeration(self.type)
        self.multiplicity = multiplicity

    def getMetaclass(self):
        return self.metaclass

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def isAttribute(self):
        return not self.isAssociationEnd

    def isAssociationEnd(self):
        return self.isAssociationEnd

    def isEnumeration(self):
        return self.isEnumeration

    def isMultiple(self):
        return self.multiplicity

    def getSignature(self,fTemplate=None,html=False):
        if fTemplate is None:
            if html:
                fTemplate = "<b>${fname}</b> : <em>${ftype}</em>${fmult}"
            else:
                fTemplate = "${fname} : ${ftype}${fmult}"
        return Template(fTemplate).substitute(
            mclass=getNameFromMetaclass(self.metaclass),
            fname=self.getName(),
            ftype=getNameFromType(self.type),
            fmult=("[*]" if self.multiplicity else ""))

    def getText(self,fTemplate=None,html=False):
        return self.getSignature(fTemplate,html)

    def __unicode__(self):
        return self.getSignature()

    def __repr__(self):
        return self.getSignature("${mclass}.${fname} : ${ftype}${fmult}")


class GetterMetaFeature(MetaFeature):
    def __init__(self,metaclass,name,type,multiplicity=False):
        MetaFeature.__init__(self,metaclass,name,type,multiplicity)

    def eval(self,element):
        try:
            jythonElementMethod = element.__getattribute__(self.name)
            return apply(jythonElementMethod,[])
        except:
            return 'ERROR("cannot apply ' + self.name + '")'





def _getMetaFeatureFromJavaMethodInfo(javaMethodInfo):
    (classe,name,parameters,return_type,multiplicty) = javaMethodInfo
    return GetterMetaFeature(classe,name,return_type,multiplicty)

#--------------------------------------------------------------------------------
# This should be in module virtual, but it creates circular dependency
#
#
#
#




class VirtualMetaFeature(MetaFeature):
    def __init__(self,fun,metaclass,name,type,multiplicity=False):
        MetaFeature.__init__(
            self,metaclass,('<<<%s>>>' % name),type,multiplicity)
        self.fun = fun

    def eval(self,element):
        return self.fun(element)

    def accept(self,metaclass):
        return issubclass(metaclass,self.metaclass)


class VirtualRegistry(object):
    virtualMetaFeatures = []

    @classmethod
    def add(cls,virtualMetaFeature):
        cls.virtualMetaFeatures.append(virtualMetaFeature)

    @classmethod
    def getFeatures(cls,metaclass):
        return [f for f in cls.virtualMetaFeatures if f.accept(metaclass)]

#
#
#
#
#--------------------------------------------------------------------------------





def getMetaFeatures(metaclass,inherited=True,groupBySuper=False,methodFilterFun=None,
                    additionalFun=()):
    """ return the meta features of a metaclass, that is MetaFeature created
        for methods getXXX(), isXXX() and toString() with no arguments
    """
    javaMethods = _getJavaMethods(metaclass,inherited=inherited,
                                  regexp='^get|is|toString',
                                  argTypes=[],methodFilterFun=methodFilterFun)
    # get the signatures
    javaMethodInfos = map(_getJavaMethodInfo,javaMethods)
    # in method info the parameters are indicated. Here we skip this as we know that
    # the methods do not have parameters.
    metafeatures = map(_getMetaFeatureFromJavaMethodInfo,javaMethodInfos)
    # Add virtual meta features that match the given metaclass using subclasses
    virtual_metafeatures = VirtualRegistry.getFeatures(metaclass)
    return metafeatures + virtual_metafeatures


class MetaclassInfo(object):
    """ Descriptor of metaclass
    """

    def __init__(self,metaclass):
        self.metaclass = metaclass
        self.metaFeatures = getMetaFeatures(metaclass)

    def getName(self):
        return getNameFromMetaclass(self.metaclass)

    def getSuperMetaclasses(self):
        return getSuperMetaclasses(self.metaclass)

    def getSubMetaclasses(self):
        return getSubMetaclasses(self.metaclass)

    def getMetaFeatures(self):
        return self.metaFeatures

    def getSignature(self,mcSignatureTemplate=None,Separator=" > ",html=False):
        if mcSignatureTemplate is None:
            mcSignatureTemplate = "$mcsig"
        s = Template(mcSignatureTemplate).substitute(
            mcsig= \
                Separator.join(map(getNameFromMetaclass,self.getSuperMetaclasses())))
        return unicode(s)

    def __repr__(self):
        return self.getSignature()

    def __unicode__(self):
        return self.getName()

    def getBody(self,fsep=None,fTemplate=None,html=False):
        if fsep is None:
            fsep = "<br/>" if html else "\n"
        return fsep.join(
            [feature.getSignature(fTemplate=fTemplate,html=html) \
             for feature in self.getMetaFeatures()])

    def getText(self,mcTemplate=None,mcSignatureTemplate=None,
                fTemplate=None,fsep=None,html=False):
        if mcTemplate is None:
            if html:
                mcTemplate = "$mcsig<br/>$mcbody"
            else:
                mcTemplate = "$mcsig\n$mcbody"
        s = Template(mcTemplate).substitute(
            mcsig=self.getSignature(mcSignatureTemplate=mcSignatureTemplate,html=html),
            mcbody=self.getBody(fTemplate=fTemplate,fsep=fsep,html=html))
        return unicode(s)


METACLASS_INFOS = dict()


def getMetaclassInfo(metaclass):
    name = getNameFromMetaclass(metaclass)
    if name in METACLASS_INFOS:
        return METACLASS_INFOS[name]
    else:
        info = MetaclassInfo(metaclass)
        METACLASS_INFOS[name] = info
        return info

# this list comes from the modelio script ExportDiagrams.py, function getFullName

PARENT_FEATURES = {
    "ModelTree":"getOwner",
    "Behavior":"getOwner",
    "BpmnRootElement":"getOwner",
    "Feature":"getOwner",
    "AbstractDiagram":"getOrigin",
    "BpmnFlowElement":"getContainer"
}




def getElementParent(element):
    """ return the parent of an element, the notion of parent being defined by
        PARENT_FEATURES
    """
    for metaclassName in PARENT_FEATURES.keys():
        methodName = PARENT_FEATURES[metaclassName]
        metaclass = getMetaclassFromName(metaclassName)
        if isinstance(element,metaclass):
            return apply(element.__getattribute__(methodName),[])
    return None


def _getElementParents(element):
    parent = getElementParent(element)
    if parent is None:
        return []
    else:
        return [parent] + _getElementParents(parent)


def getElementParents(element,inclusive=False,reverse=False):
    parents = ([element] if inclusive else []) + _getElementParents(element)
    return reversed(parents) if reverse else parents





def getElementPath(element):
    """ return a qualified name for the element if it is possible to compute one
        by concatenating the "name" of parent elements.
        The path is computed according to some appropriate
        "parent" association depending on the type of elements.
        If it is not possible to get the path, then return the id of the element.
    """
    try:
        names = pyalaocl.Seq.new(map(lambda x:x.getName(),
                    getElementParents(element,inclusive=True,reverse=True)))
        if names.exists(lambda e:e==''):
            return unicode(getElementId(element))
        else:
            return unicode(".".join(names))
    except:
        return unicode(getElementId(element))













#--------- model level ------------------------------------------


def isNone(x):
    return x is None


def isScalar(x):
    return isinstance(x,basestring) \
           or isinstance(x,int) \
           or isinstance(x,bool) \
           or isinstance(x,long) \
           or isinstance(x,float)


def isEnumerationLiteral(x):
    return isinstance(x,java.lang.Enum)


def isAtomic(x):
    return isScalar(x) or isEnumerationLiteral(x)


def isElement(x):
    """ True for objects XXX
    """
    return isinstance(x,ModelioElement) \
           or (x is not None
               and not isAtomic(x)
               and not isElementList(x))


def isElementList(x):
    return isList(x) and pyalaocl.asSeq(x).forAll(isElement)


def getElementId(element):
    """ get the id of an element. Try various means to do that
    """
    try:
        # this should work on Modelio 2.x
        s = unicode(element.getIdentifier())
    except:
        try:
            s = unicode(element.getUuid().toString())
        except:
            try:
                s = unicode(element.getId())
            except:
                s = u"jythonId#%s" % unicode(id(element))
    return s

# noinspection PyUnresolvedReferences
from java.util import List as JavaList


def getElementNameOrId(element,unnamed=None):
    try:
        s = element.getName()
    except:
        s = None
    if s is None or len(s) == 0:
        if unnamed is None:
            s = getElementId(element)
        else:
            s = unnamed
    return unicode(s)


def getElementSignature(element,unnamed=None):
    """ function to transform an individual element to some text text"
        This function is used in ModelValue class
    """
    return getElementNameOrId(element,unnamed=unnamed) \
           + " : " + getNameFromMetaclass(getMetaclass(element))


class ModelValue(object):
    def __unicode__(self):  return unicode(self.getText())

    # isScalar()
    # getValue()
    # getKind()
    # getText()
    # isElementContainer()
    # isScalar()
    # isAtomic()
    # isEnumerationLiteral()
    # isScalar()
    # isElement()
    # isElementList()
    # isEmpty()
    def notEmpty(self):                 return not self.isEmpty()


class ElementContainerModelValue(ModelValue):
    # isEmpty()
    # notEmpty()
    # getCard()
    # isMultiple()
    def isElementContainer(self):       return True

    def isEnumerationLiteral(self):     return False

    def isScalar(self):                 return False

    def isAtomic(self):                 return False


class NoneModelValue(ElementContainerModelValue):
    def getValue(self):                 return None

    def getKind(self):                  return "element"

    def isElement(self):                return True

    def isElementList(self):            return False

    def getCard(self):                  return 0

    def isMultiple(self):               return False

    def isEmpty(self):                  return True

    def getText(self):                  return "None"


class ElementModelValue(ElementContainerModelValue):
    def __init__(self,element):
        self.element = element

    def getValue(self):                 return self.element

    def getKind(self):                  return "element"

    def isElement(self):                return True

    def isElementList(self):            return False

    def getCard(self):                  return 1

    def isMultiple(self):               return False

    def isEmpty(self):                  return False

    def getText(self):
        return "\n    " + getElementSignature(self.element)


class ElementListModelValue(ElementContainerModelValue):
    def __init__(self,elementList):
        self.elementList = elementList

    def getValue(self):                 return self.elementList

    def getKind(self):                  return "elementList"

    def isElement(self):                return False

    def isElementList(self):            return True

    def getCard(self):                  return len(self.elementList)

    def isMultiple(self):               return True

    def isEmpty(self):                  return self.getCard() == 0

    def getText(self):
        return "\n    " + "\n    ".join(map(getElementSignature,self.elementList))


class AtomicModelValue(ModelValue):
    def isElementContainer(self):       return False

    def isElement(self):                return False

    def isElementList(self):            return False

    def isAtomic(self):                 return True

    def isEmpty(self):                  return False


class EnumerationLiteralModelValue(AtomicModelValue):
    def __init__(self,literal):
        self.literal = literal

    def isEnumerationLiteral(self):     return True

    def getValue(self):                 return self.literal

    def getKind(self):                  return "enumerationLiteral"

    def getText(self):                  return self.literal.toString()

    def isScalar(self):                 return False


class ScalarModelValue(AtomicModelValue):
    def __init__(self,scalar):          self.scalar = scalar

    def getValue(self):                 return self.scalar

    def getKind(self):                  return "scalar"

    def getText(self):                  return unicode(self.scalar)

    def isScalar(self):                 return True


class StringModelValue(ScalarModelValue):
    def __init__(self,string):
        ScalarModelValue.__init__(self,string)

    def getText(self):                  return u'"' + self.scalar + '"'


def getModelValueFromValue(value):
    if value is None:
        return NoneModelValue()
    if isinstance(value,basestring):
        return StringModelValue(value)
    elif isEnumerationLiteral(value):
        return EnumerationLiteralModelValue(value)
    elif isScalar(value):
        return ScalarModelValue(value)
    elif isElementList(value):
        return ElementListModelValue(value)
    elif isElement(value):
        return ElementModelValue(value)
    else:
        print "getModelValueFromValue(%s). type of parameter not recognized: %s" \
                % value,type(value)
        return StringModelValue("UNKNOWN, see the console")






def getMetaclass(element):
    """ returns the metaclass of the given element
    """
    # TODO: check
    if isinstance(element,ModelioElement):
        name = element.getMClass().getName()
        return getMetaclassFromName(name)
    else:
        return type(element)


def getAllInstances(metaclass):
    """ returns all instances of a given metaclass
    """
    return MODELING_SESSION.findByClass(metaclass)


def getSelectedInstances(metaclass,attributeName,attributeValue):
    """ returns all instances with a value for a given attribute
    """
    return MODELING_SESSION.findByAtt(metaclass)


def getModelRoot():
    return MODELING_SESSION.getModel()





class MetaFeatureSlot(object):
    """ MetaFeature slots are values of a given feature for given element
    """

    def __init__(self,element,metafeature):
        self.metaFeature = metafeature
        self.element = element
        # computed on demand
        self.modelValue = None

    def getElement(self):
        return self.element

    def getMetaFeature(self):
        return self.metaFeature

    def getName(self):
        return self.metaFeature.getName()

    def getModelValue(self):
        if self.modelValue is None:
            self.modelValue = getModelValueFromValue(self.metaFeature.eval(self.element))
        return self.modelValue

    def isEmpty(self):
        return self.getModelValue().isEmpty()

    def notEmpty(self):
        return not self.isEmpty()

    def getCard(self):
        return self.getModelValue().getCard()

    def getText(self,stemplate=None,ftemplate=None,mvtemplate=None):
        if stemplate is None:
            stemplate = "$fsig = $mv"
        mval = self.getModelValue()
        fsig = self.getMetaFeature().getText(fTemplate=ftemplate)
        mvaltext = mval.getText()
        # s = Template(stemplate).substitute( \
        # fsig = self.getMetaFeature().getText(ftemplate=ftemplate),
        # mv = mval.getText(mvtemplate=mvtemplate),
        # mvscalar = mvaltext if mval.isScalar() else ""
        # mvenum = mvaltext if mval.isEnumerationLiteral() else ""
        # mvelement = mvaltext if mval.isE
        # mvtype = unicode(type(self.getModelValue().getValue())) )
        s = fsig + " = " + mvaltext
        return unicode(s)

    def __unicode__(self):
        return unicode(self.metaFeature.getSignature() + " = " + unicode(self.getModelValue()))

    def __repr__(self):
        return self.getText()


        # TODO we should probably define equals or something like that


def getMetaFeatureSlots(element,inherited=True):
    metaclass = getMetaclass(element)
    return pyalaocl.Seq.new([MetaFeatureSlot(element,feature) for feature in getMetaFeatures(metaclass)])


class ElementInfo(object):
    """
    """

    def __init__(self,element):
        self.element = element
        self.identifier = id(element)  # TODO self.element.getIdentifier()
        self.metaclass = getMetaclass(element)
        self.metaclassName = getNameFromMetaclass(self.metaclass)
        self.metaclassInfo = getMetaclassInfo(self.metaclass)
        self.name = getElementNameOrId(self.element)
        self.path = getElementPath(element)
        # the slot list keep the order corresponding to inheritance
        # it is computed on demande
        self.slotList = None
        # the slot map is indexed by slot names. It is computed on demand
        self.slotMap = None

    def getElement(self):
        return self.element

    def getName(self):
        return self.name

    def getPath(self):
        return self.path

    def getMetaclass(self):
        return self.metaclass

    def getMetaclassName(self):
        return self.metaclassName

    def getMetaclassInfo(self):
        return self.metaclassInfo

    def _getSlotList(self):
        # compute the slot list on demand
        if self.slotList is None:
            self.slotList = getMetaFeatureSlots(self.element)
        return self.slotList

    def getSlotList(self,emptySlots=True):
        slots = self._getSlotList()
        if not emptySlots:
            slots = slots.reject(MetaFeatureSlot.isEmpty)
        return slots

    def getSlotMap(self):
        if self.slotMap is None:
            slots = self.getSlotList()
            self.slotMap = {}
            for slot in slots:
                self.slotMap[slot.getName()] = slot
        return self.slotMap

    def getSlot(self,name):
        return self.getSlotMap()[name]

    def getModelValue(self,name):
        return self.getSlot(name).getModelValue()

    def getSignature(self,path=True):
        return (self.path if path else self.name) \
               + " : " + self.metaclassInfo.getSignature()

    def getText(self,emptySlots=False):
        return u'\n'.join(
            [self.getSignature()] \
            + [u"  " + slot.__repr__() \
               for slot in self.getSlotList(emptySlots)]
        )

    def __unicode__(self):
        return str(self.element.getName()) + " : " + self.metaclassName

    def __repr__(self):
        return self.getSignature(True)


    # ELEMENT_INFOS = dict()

    # def getElementInfo(element):
    # XXX TODO the idenfier was a good solution, fund anotuer one
    # """ return for an element its description (ElementInfo)
    # """
    # try :
    # i = element.getIdentifier()
    # except:
    # i = id(element)
    # if i in ELEMENT_INFOS:
    # return  ELEMENT_INFOS[i]
    # else:
    # info = ElementInfo(element)
    # ELEMENT_INFOS[i] = info
    # return info










print "module metascribe.introspection loaded from",__file__
