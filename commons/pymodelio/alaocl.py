# -*- coding: utf-8 -*-

"""
Collection of classes and functions to ease the translation of OCL expressions into python.

.. moduleauthor:: jeanmariefavre

* =   -> ==
* x.isUndefined() -> isUndefined(x)

Number
------
* x.abs() -> abs(x)
* x.min(y) -> min(x,y)
* x.max(y) -> max(x,y)

Integer
-------
* div   /
* mod   %

Real
----
* x.floor() ->   floor(x)
* x.round() ->   round(x) 

String
------
* s1.size()             -> len(s1)
* s1.contact(s2)        -> s1+s2
* s1.substring(i1,i2)   -> s1[i1,i2]   TODO: check
* s1.toUpper()          -> s1.upper()
* s1.toLower()          -> s1.lower()

Boolean
-------
* true                  -> True
* false                 -> False
* xor                   -> TODO: implement it as xor(a,b)  or  a \|xor| b with Infix
* implies               -> TODO: like xor
* if c then a else b    -> a if c else b

Enumeration
-----------
* E::x                  -> E.x

Collection
----------
* coll                  C(coll)
* coll->op(...)         C(coll).op(...)
                    
* Set{ ... }            -> Set( ... )
* Bag{ ... }            -> Bag( ... )
* OrderedSet{ ... }     -> OrderedSet( ... )
* Sequence{ ... }       -> Seq( ... )
* Sequence {1..5, 10..20} -> Seq{range(1,5)+range(10,20)}

UML based features
------------------
* oclIsNew              -> Not available. Can be use only with postcondition
* oclAsType             -> Not necessary thanks for dynamic typing in python.




from org.modelio.vcore.smkernel import SmList
def select(self,f): return [x for x in self if f(x) ]
a = selectedElements[0].getOwnedAttribute()
print type(a),type(a[0])
print select(a,lambda x:x.isModifiable())
SmList.select = select
print a.select(Attribute.isModifiable)

"""

import abc      


def floor(r):
    """ Return the largest integet which is not greater than the parameter.
    """
    import math
    return math.floor(r)

def isUndefined(x):
    """
    Indicates if the given parameter is undefined or not.

    Examples:
        >>> print isUndefined(3)
        False
        >>> print isUndefined(None)
        True
    """
    return x is None

def oclIsKindOf(value,aType):
    """
    Evaluates to True if the type of the value is *exactly* the type given as a second parameter. an instance of type or one of its subtypes directly or indirectly. Use ocl To check if a value is exactly of a given type.
    
    Arguments:
        value (any):    A scalar value, a collection or an object.
        
        type (aType):    A type (e.g. int, float, basestring, bool or a class)
    Returns:
        bool:           True if value is compatible with the type aType.
    Examples:
        >>> print oclIsKindOf(3,int)
        True
        >>> print oclIsKindOf("3",int)
        False
        >>> print oclIsKindOf(2.5,float)
        True
        >>> print oclIsKindOf("hello",basestring)
        True
        >>> print oclIsKindOf(True,bool)
        True
        >>> class Person(object): pass
        >>> print oclIsKindOf(Person(),Person)
        True
        >>> print oclIsKindOf(Person(),object)
        True
        >>>
    """
    return isinstance(value,aType)   
    
def oclIsTypeOf(value,aType):
    """ Evaluates to True if the type of the value is *exactly* the type given as a second parameter. This function does not take into account sub-typing relationships. If this is what is intended, use oclIsKindOf instead.
    
    Arguments:
        value (any):    A scalar value, a collection or an object.
        
        type (aType):    A type (e.g. int, float, str, unicode, bool or a class)
    Returns:
        bool:           True if value is compatible with the type aType.
    Examples:
        >>> print oclIsTypeOf("hello",str)    # in python2 we have str for ascii string
        True
        >>> print oclIsTypeOf("hello",basestring)    # basestring is the supertype of string/unicode
        False
        >>> print oclIsTypeOf(u"çüabè",unicode)   # note u"..." for unicode string
        True
    """
    return type(value) == aType
    
 
    
class Collection(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def size(self):
        """
        """
    def isEmpty(self):
        return self.size(self)==0
    def notEmpty(self):
        return not self.isEmpty()
    def count(self,element):
        pass  # FIXME
    def includes(self,element):
        return element in self.elements         # check if ok
    def excludes(self,element):
        return not self.includes(element)
    def includesAll(self,elements):
        for e in elements:
            if not self.includes(e):
                return False
        return True
    def excludesAll(self,elements):
        for e in elements:
            if not self.excludes(e):
                return False
        return True
    def sum(self):
        return sum(self.elements)           # TODO: check if ok with bag
        
class Set(Collection):
    def __init__(self,*args):
        """
        Create a set from some elements.
        
        Examples:
           >>> print Set(10,"a",3,10,10) == Set(10,"a",3)
           True
           >>> print Set() <> Set(10,"a",3)
           True
        """
        self.theSet = set(args)           # FIXME: conversion should apply if collection
    def size(self):
        return len(self.theSet)
    def including(self,element):
        return Set(self.theSet | set(element))
    def excluding(self,element):
        return Set(self.theSet - set(element))
    def union(self,coll):
        return Set(self.theSet | set(coll))
    def intersection(self,coll):
        return Set(self.theSet & set(coll))
    def difference(self,coll):                  # - in ocl
        return Set(self.theSet - set(coll))
    def flatten(self):  
        r = set()
        for s in self.theSet:
            r |= s
        return Set(r)
    def asBag(self):
        return Bag(self.theSet)
    def asSequence(self):
        return Sequence(self.theSet)
    def __str__(self):
        return str(self.theSet)
    def __eq__(self,value):
        if not isinstance(value,Set):
            return False
        return self.theSet == value.theSet
    
    
class Bag(Collection):
    def __init__(self,*args):
        self.theCounter = Counter(*args)
    def size(self):
        return sum(self.theCounter.values())
    def including(self,elem):
        return Bag( self.theCounter + Counter([elem]) )
    def excluding(self,elem):
        r = Bag(self.theCounter)
        if elem in r:
            del r[elem]
        return
    def union(self,coll):
        raise ValueError("not implemented")    # FIXME
    def intersection(self,coll):
        raise ValueError("not implemented")    # FIXME
    def flatten(self,coll):
        raise ValueError("not implemented")    # FIXME
    def asSet(self,coll):
        raise ValueError("not implemented")    # FIXME
    def asSequence(self,coll):
        raise ValueError("not implemented")    # FIXME


class Seq(Collection):
    pass
    
class OrderedSet(Collection):
    pass



# execute tests if launched from command line
if __name__ == "__main__":
    import doctest
    doctest.testmod()