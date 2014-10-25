# coding=utf-8
"""
Get elements of metamodel documentation using modelio web as a resources.

This module reads a web page from modelio web site and use it to compute
the URL of web pages for:

* the documentation of a metaclass
* the javadoc API of the metaclass

Since various the web structure is not always the same for all modelio versions,
an explicit mapping should be maintain when new versions of modelio are delivered.
If an error is generated by this module for a given version this is most
probably that the mapping is not defined. So please add it...
"""
__all__ = [
    'getMetaclassMetamodelURL',
    'getMetaclassJavadocURL',
]



from pymodelio.core.env import PyModelioEnv

# noinspection PyUnresolvedReferences
from org.modelio.api.modelio import Modelio
import re
from metascribe.introspection import getNameFromMetaclass
from pymodelio.misc import getWebPage



def getModelioSimpleVersion():
    v = Modelio.getInstance().getContext().getVersion()
    return '%s.%s' % (v.getMajorVersion(),v.getMinorVersion())


def getMetaclassJavadocURL(metaclass):
    """ Return the url of the javadoc for the given metaclass or None if not found
    """


    try:
        name = metaclass.getCanonicalName()
        if name.startswith('org.modelio.'):
            return '%s/%s.html' \
                   % (PyModelioEnv.MODELIO_WEB_DOC_JAVADOC,name.replace(".","/"))
        else:
            return None
    except:
        return None


METAMODEL_ROOT_ENTRY_REGEXPR = {
    '3.0':'<img src="img/elt_1470811194701554859.png"/><a href="([0-9]+\.html#[\-_0-9A-Za-z]+)"> ([A-Za-z0-9]+)</a>',
    '3.1':'<img src="img/elt_2201401863446517728.png"/><a href="([0-9]+\.html#[\-_0-9A-Za-z]+)"> ([A-Za-z0-9]+)</a>',
}

# A map that for each metaclass name return the local url in the metamodel documentation
# This map is computed by reading the index web page of the metamodel.
# A resulting entry is something like:
#       "Term" :"15.html#_00080b08-0000-1cb6-0000-000000000000"
# This map is computed on demand and only once
METACLASS_NAME_TO_LOCAL_PAGE_MAP = None





def _getMetaclassNameToLocalPageMap():
    global METACLASS_NAME_TO_LOCAL_PAGE_MAP
    if METACLASS_NAME_TO_LOCAL_PAGE_MAP is None:
        regexpr = METAMODEL_ROOT_ENTRY_REGEXPR[getModelioSimpleVersion()]
        html = getWebPage(PyModelioEnv.MODELIO_WEB_DOC_METAMODEL + '/modelbrowser.html')
        METACLASS_NAME_TO_LOCAL_PAGE_MAP = {}
        for match in re.findall(regexpr,html):
            (local_url,metaclass_name) = match
            METACLASS_NAME_TO_LOCAL_PAGE_MAP[metaclass_name] = local_url
    return METACLASS_NAME_TO_LOCAL_PAGE_MAP


def getMetaclassMetamodelURL(metaclass,relative=False):
    map = _getMetaclassNameToLocalPageMap()
    metaclass_name = getNameFromMetaclass(metaclass)
    if metaclass_name is None:
        return None
    else:
        if metaclass_name in map:
            url = map[metaclass_name]
            if relative:
                return url
            else:
                return "%s/%s" % (PyModelioEnv.MODELIO_WEB_DOC_METAMODEL,url)
        else:
            return None
