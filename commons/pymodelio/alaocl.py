# -*- coding: utf-8 -*-

"""
Collection of classes and functions to ease the translation of OCL expressions into python.

.. moduleauthor:: jeanmariefavre

* =   -> ==
* x.isUndefined() -> isUndefined(x)
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
    """ Return the largest integer which is not greater than the parameter.
    """
    import math

    return math.floor(r)


def isUndefined(value):
    """
    Indicates if the given parameter is undefined (None) or not.
    :param value: any kind of value.
    :type value: any
    :return: True if the value is None.
    :rtype: bool

    Examples:
        >>> print isUndefined(3)
        False
        >>> print isUndefined(None)
        True
    """
    try:
        return value is None
    except:
        return True  # see OCL 11.3.4


def oclIsUndefined(value):
    return isUndefined(value)


class Invalid(Exception):
    def __init__(self,msg):
        super(Invalid,self).__init__(msg)


def oclIsKindOf(value,aType):
    """
    Evaluates to True if the type of the value is *exactly* the type given as a second parameter
    is an instance of type or one of its subtypes directly or indirectly. Use the method
    oclIsTypeOf if you want to check if a value is exactly of a given type.
    
    :param value: A scalar value, a collection or an object.
    :type value; Any
    :param aType: The type to check the value against
                  (e.g. int, float, str, unicode, bool or a class)
    :type aType: type
    :return: True if value is compatible with the type aType.
    :rtype: bool
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
    """
    Return True if the type of the value is *exactly* the type given as a second parameter. This function does not take into account sub-typing relationships. If this is what is intended, use oclIsKindOf instead.
    
    :param value: A scalar value, a collection or an object.
    :type value; Any
    :param aType: The type to check the value against
                  (e.g. int, float, str, unicode, bool or a class)
    :type aType: type
    :return: True if value is compatible with the type aType.
    :rtype: bool
    Examples:
        >>> print oclIsTypeOf("hello",str)    # in python2 we have str for ascii string
        True
        >>> print oclIsTypeOf("hello",basestring)    # basestring is the supertype of string/unicode
        False
        >>> print oclIsTypeOf(u"çüabè",unicode)   # note u"..." for unicode string
        True
    """
    return type(value) == aType


from collections import deque

class Collection(object):
    """
    Abstract class trying to mimic OCL collections.
    Collections are either:
    * sets (Set),
    * ordered set (OrderedSet)
    * bags (Bag),
    * sequences (Seq)
    """
    __metaclass__ = abc.ABCMeta


    def __getattr__(self,name):
        """

        :param name:
        :return:

        Examples:
            >>> class P(object):
            ...      def __init__(self,x):
            ...         self.a = x
            >>> P1 = P(1)
            >>> P4 = P(4)
            >>> P1.a
            1
            >>> P4.a
            4
            >>> Set(P1,P4).a == Bag(1,4)
            True
        """
        return self.collect(lambda e:getattr(e,name))

    def __len__(self):
        """
        Return the size of the collection.

        Not in OCL but  pythonic.
        :return: The number of elements in the collection
        :rtype: int

        Examples:
            >>> len(Set(2,2,3))
            2
            >>> len(Bag(1,1,1))
            3
            >>> len(Set(Set()))
            1
        """
        return self.size()

    @abc.abstractmethod
    def size(self):
        """
        Return the total number of elements in the collection.
        """
        pass

    def isEmpty(self):
        return self.size() == 0

    def notEmpty(self):
        return not self.isEmpty()

    @abc.abstractmethod
    def count(self,element):
        pass

    def includes(self,value):
        """
        Return True if the value is in the collection.
        :param value: Any kind of value.
        :type value: any
        :return: True if the element is in set, False otherwise.
        :rtype: bool
        Examples:
            >>> Set(1,3,"a").includes("3")
            False
            >>> Set(1,3,"a").includes(3)
            True
            >>> Set(Set()).includes(Set())
            True
            >>> Set().includes(Set())
            False
            >>> 3 in Set(2,3,1)
            True
            >>> "hello" in Set("a","b")
            False

            >>> Bag(10,"a",3,3,10,10).includes(10)
            True
            >>> Bag(2).includes(5)
            False
            >>> 2 in Bag(2,2)
            True

            >>> Seq(10,2,2,3).includes(3)
            True
            >>> 2 in Seq(1,0,1)
            False

        """
        return value in self

    def excludes(self,value):
        return value not in element

    def includesAll(self,elements):
        for e in elements:
            if e not in self:
                return False
        return True

    def excludesAll(self,elements):
        for e in elements:
            if e in self:
                return False
        return True

    @abc.abstractmethod
    def excluding(self,value):
        pass

    def any(self,predicate):
        """
        Return any element in the collection that satisfy the predicate.

        This operation is non deterministic as various elements may satisfy
        the predicate.
        If not element satisfies the predicate an exception is raised.
        See OCL-11.9.1
        :param predicate: A predicate, that is a function returning a boolean.
        :type predicate: X->bool
        :return: Any element satisfying the predicate.
        :rtype X:

        Examples:
            >>> Set(1,2,-5,-10).any(lambda x:x<0) in [-5,-10]
            True
            >>> Set(1,2).any(lambda x:x<0)
            Traceback (most recent call last):
              ...
            Invalid: .any(...) failed: No such element.
        """
        for e in self:
            if predicate(e):
                return e
        raise Invalid(".any(...) failed: No such element.")

    def max(self):
        return max(self)

    def min(self):
        return min(self)

    def sum(self):
        """
        Sum of the number in the collection.
        Examples:
            >>> Set(1,0.5,-5).sum()
            -3.5
            >>> Set().sum()
            0
        """
        return sum(self)

    @abc.abstractmethod
    def select(self,expression):
        pass

    def selectByKind(self,aType):
        return self.select(lambda e:oclIsKindOf(aType))

    def selectByType(self,aType):
        return self.select(lambda e:oclIsTypeOf(aType))

    def reject(self,expression):
        """
        Discard from the set all elements that satisfy the expression.

        :param expression: A predicate, that is a function returning a boolean.
        :return: The set without the rejected elements.
        :rtype set:

        Examples:
            >>> Set(2,3,2.5,-5).reject(lambda e:e>2) == Set(2,-5)
            True
            >>> Set(Set(1,2,3,4),Set()).reject(lambda e:e.size()>3) == Set(Set())
            True
        """
        return self.select(lambda e:not expression(e))

    @abc.abstractmethod
    def flatten(self):
        pass

    @abc.abstractmethod
    def collectNested(self,expression):
        pass

    def collect(self,expression):
        return self.collectNested(expression).flatten()

    def forAll(self,predicate):
        """
        Return True if the predicate given as parameter is satisfied by all
        elements of the collection.

        :param predicate: A predicate, that is a function returning a boolean.
        :type predicate: X->bool
        :return: Whether or not the predicate is satisfied by all elements.
        :rtype bool:

        Examples:
            >>> Set(2,3,5,-5).forAll(lambda e:e>=0)
            False
            >>> Set(2,3,5).forAll(lambda e:e>=0)
            True
            >>> Set().forAll(lambda e:e>=0)
            True
            >>> Bag(4,4,4).forAll(lambda e:e==4)
            True
            >>> Seq(Bag(1),Set(2),Seq(3)).forAll(lambda e:e.size()==1)
            True
        """
        for e in self:
            if not predicate(e):
                return False
        return True

    def exists(self,predicate):
        """
        Return True if the predicate given as parameter is satisfied by at
        least one element of the collection.

        :param predicate: A predicate, that is a function returning a boolean.
        :type predicate: X->bool
        :return: Whether or not the predicate is satisfied by at least one element.
        :rtype bool:

        Examples:
            >>> Set(2,3,5,-5).exists(lambda e:e<0)
            True
            >>> Set(2,3,5).exists(lambda e:e<0)
            False
            >>> Set().exists(lambda e:e>=0)
            False
            >>> Bag(Set(),Set(),Set(2),Set(3)).exists(lambda e:e.size()==1)
            True
        """
        for e in self:
            if predicate(e):
                return True
        return False

    def one(self,predicate):
        """
        Return True if the predicate given as parameter is satisfied by at
        one and only one element in the collection.

        :param predicate: A predicate, that is a function returning a boolean.
        :type predicate: X->bool
        :return: Whether or not the predicate is satisfied by exactly one element.
        :rtype bool:

        Examples:
            >>> Set(2,3,5,-5).one(lambda e:e<0)
            True
            >>> Bag(2,3,5,-5,-5).one(lambda e:e<0)
            False
            >>> Set().one(lambda e:e>=0)
            False
            >>> Seq().one(lambda e:e>=0)
            False
            >>> Seq(1).one(lambda e:e>=0)
            True
            >>> Bag(Set(2),Set(),Set(3),Set()).one(lambda e:e.size()==0)
            False
        """
        foundOne = False
        for e in self:
            found = predicate(e)
            if found and foundOne:
                return False
            elif found:
                foundOne = True
        return foundOne

    @abc.abstractmethod
    def sortedBy(self,expression):
        pass


    def closure(self,expression):
        """
        Return the transitive closure of the expression for all element in
        the collection.

        See OCL (section 7.6.5.

        FIXME: Here closure returns always a sequence, but the type changes in OCL.

        :param expression: The expression to be applied again and again.
        :type: X->X
        :return: A set representing the transitive closure including the source elements/
        :type: Seq[X]
        Examples:

            >>> def f(x):
            ...     successors = {1:[2],2:[1,2,3],3:[4],4:[],5:[5],6:[5],7:[5,7]}
            ...     return successors[x]
            >>> Set(1).closure(f) == Seq(1,2,3,4)
            True
            >>> Set(5).closure(f) == Seq(5)
            True
            >>> Seq(6,6,3).closure(f) == Seq(6,3,5,4)
            True
        """

        # We cannot have Counter here. So list is ok (see Converter.listAll)
        sources = list(self)
        to_visit = deque(sources)
        visited = []
        while len(to_visit) != 0:
            current = to_visit.popleft()
            if current not in visited:
                result = expression(current)
                if isAnyCollection(result):
                    successors = Converter.listAll(result)
                else:
                    successors = [result]
                # print "visited %s -> %s" % (current,successors)
                for s in successors:
                    if s not in visited:
                        to_visit.append(s)
                visited.append(current)
        return asSeq(visited)


    def iterate(self):
        # FIXME: Not implemented (See 7.6.6)
        raise NotImplementedError()

    def isUnique(self,expression):
        return self.asSet().collect(expression).hasDuplicates()

    @abc.abstractmethod
    def asSet(self):
        pass

    @abc.abstractmethod
    def asBag(self):
        pass

    @abc.abstractmethod
    def asSeq(self):
        pass

    @abc.abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()

    @abc.abstractmethod
    def __eq__(self,value):
        pass

    def __ne__(self,value):
        return not self.__eq__(value)

    @abc.abstractmethod
    def __hash__(self):
        pass

    @abc.abstractmethod
    def __contains__(self,item):
        pass

    @abc.abstractmethod
    def __iter__(self):
        pass


def asSet(collection):
    """
    Convert the given collection to a Set
    :param collection:
    :return:
    :rtype: Set
    """
    if isinstance(collection,Set):
        return collection
    try:
        return collection.asSet()
    except AttributeError:
        return Set() | collection


class Set(Collection):
    """
    Set of elements.

    This class mimics OCL Sets. Being a set, there are no duplicates and no ordering of elements.
    By contrast to OCL Sets, here a set can contain any kind of elements at the same time.
    OCL sets are homogeneous, all elements being of the same type (or at least same supertype).
    """

    def __init__(self,*args):
        """
        Create a set from some elements.

        Eliminate duplicates if any.
        Examples:
           >>> Set(10,"a",3,10,10) == Set(10,"a",3)
           True
           >>> Set() <> Set(10,"a",3)
           True
           >>> Set(10,10).size()
           1
           >>> Set(Set()).size()
           1
           >>> Set("hello").size()
           1
           >>> Set(Set(2),Set(2)).size()
           1
        """
        # We cannot have Counter here. So list is ok (see Converter.listAll)
        self.theSet = set(list(args))

    def size(self):
        """
        Return the size of the set.
        :return: The size of the set.
        :rtype: int
        Examples:
            >>> Set(1,4,2,1,1).size()
            3
            >>> Set().size()
            0
        """
        return len(self.theSet)

    def isEmpty(self):
        return True if self.theSet else False

    def count(self,value):
        """
        Return the number of occurrence of the value in the set (0 or 1).
        :param value: The element to search in the set.
        :type value: any
        :return: 1 if the element is in the set, 0 otherwise.
        :rtype: bool
        Examples:
            >>> Set(1,3,"a").count("3")
            0
            >>> Set(1,3,3,3).count(3)
            1
        """
        return 1 if value in self.theSet else 0

    def includes(self,value):
        return value in self.theSet

    def including(self,value):
        """
        Add the element to the set if not already there.
        :param value: The element to add to the set.
        :type value: any
        :return: A set including this element.
        :rtype: Set
        Examples:
            >>> Set(1,3,"a").including("3") == Set(1,"3",3,"a")
            True
            >>> Set(1,3,3,3).including(3) == Set(3,1)
            True
        """
        self.theSet.add(value)
        return self

    def excluding(self,value):
        """
        Excludes a value from the set (if there).
        :param value: The element to add to the set.
        :type value: any
        :return: A set including this element.
        :rtype: Set
        Examples:
            >>> Set(1,3,"a").excluding("3") == Set(1,3,"a")
            True
            >>> Set(1,3,3,3).excluding(3) == Set(1)
            True
        """
        self.theSet.discard(value)
        return self

    def union(self,anyCollection):
        """
        Add all elements from the collection given to the set.
        :param anyCollection: A collection of values to be added to this set.
        :type anyCollection: collection
        :return: A set including all values added plus previous set elements.
        :rtype: Set
        Examples:
            >>> Set(1,3,'a').union([2,3,2]) == Set(1,3,"a",2)
            True
            >>> Set(1,3,3,3).union(Set(2,1,8)) == Set(1,2,3,8)
            True
            >>> Set().union(Set()) == Set()
            True
            >>> Set(1,3) | [2,3] == Set(1,2,3)
            True
        """
        assert isAnyCollection(anyCollection), \
            'Any collection expected, but found %s' % anyCollection
        # We don't need to take special care with Counter as we remove duplicates
        self.theSet = self.theSet | set(anyCollection)
        return self

    def __or__(self,anyCollection):
        return self.union(anyCollection)

    def intersection(self,anyCollection):
        """
        Retain only elements in the intersection between this set and the given collection.
        :param anyCollection: A collection of values to be added to this set.
        :type anyCollection: collection
        :return: A set including all values added plus previous set elements.
        :rtype: Set
        Examples:
            >>> Set(1,3,"a").intersection(["a","a",8]) == Set("a")
            True
            >>> Set(1,3,3,3).intersection(Set(1,3)) == Set(1,3)
            True
            >>> Set(2).intersection(Set()) == Set()
            True
            >>> Set(2) & Set(3,2) == Set(2)
            True
        """

        assert isAnyCollection(anyCollection), \
            'Any collection expected, but found %s' % anyCollection
        # We don't need to take special care with Counter as we remove duplicates
        self.theSet = self.theSet & set(anyCollection)
        return self

    def __and__(self,anyCollection):
        return self.intersection(anyCollection)

    def difference(self,anyCollection):
        """
        Remove from the set all values in the collection.
        :param anyCollection: Any collection of values to be discarded from this set.
        :type anyCollection: collection
        :return: This set without the values in the collection.
        :rtype: Set
        Examples:

            >>> Set(1,3,"a").difference([2,3,2,'z']) == Set(1,"a")
            True
            >>> Set(1,3,3,3).difference(Set(1,3)) == Set()
            True
            >>> Set().difference(Set()) == Set()
            True
            >>> Set(1,3) - [2,3] == Set(1)
            True
        """
        assert isAnyCollection(anyCollection), \
            'Any collection expected, but found %s' % anyCollection
        # We don't need to take special care with Counter as we remove duplicates
        self.theSet = self.theSet - set(anyCollection)
        return self

    def __sub__(self,anyCollection):
        return self.difference(anyCollection)

    def symmetricDifference(self,anyCollection):
        """
        Return the elements that are either in one set but not both sets.

        In fact this method accept any collection, but it is first converted
        to a set.
        
        :param anyCollection: A collection to make the difference with.
        :type anyCollection: collection
        :return: The symmetric difference.
        :rtype: Set
        Examples:
            >>> Set(1,2).symmetricDifference(Set(3,2)) == Set(1,3)
            True
            >>> Set(Set()).symmetricDifference(Set()) == Set(Set())
            True
        """
        assert isAnyCollection(anyCollection), \
            'Any collection expected, but found %s' % anyCollection
        other_set = set(anyCollection)
        self.theSet = (self.theSet | other_set) - (self.theSet & other_set)
        return self

    def flatten(self):
        """
        If the set is a set of collections, then return the set-union of all
        its elements.

        :return: Set
        :rtype: Set
        Examples:
            >>> Set(Set(2)).flatten() == Set(2)
            True
            >>> Set(Set(Set(2)),Set(2)).flatten() == Set(2)
            True
            >>> Set(Set(2,3),Set(4),Set(),Bag("a"),Bag(2,2)).flatten() == Set(2,3,4,"a")
            True
            >>> Set().flatten() == Set()
            True
            >>> Set(2,3).flatten() == Set(2,3)
            True
            >>> Set(2,Set(3),Set(Set(2))).flatten() == Set(2,3)
            True
        """
        r = set()
        for e in self.theSet:
            if isAnyCollection(e):
                flat_set = set(flatten(e))
            else:
                flat_set = {e}
            r = r | flat_set
        self.theSet = r
        return self

    def select(self,predicate):
        """
        Retain in the set only the elements satisfying the expression.

        :param expression: A predicate, that is a function returning a boolean.
        :return: The set with only the selected elements.
        :rtype Set:

        Examples:
            >>> Set(2,3,2.5,-5).select(lambda e:e>2) == Set(3,2.5)
            True
            >>> Set(Set(1,2,3,4),Set()).select(lambda e:e.size()>3) == Set(Set(1,2,3,4))
            True
        """
        self.theSet = set([e for e in self if predicate(e)])
        return self

    def collectNested(self,expression):
        """
        Return a bag of values resulting from the evaluation of the given expression
        on all elements of the set.

        The transformation from this set to a bag is due to the fact that
        the expression can generate duplicates.

        :param expression: A function returning any kind of value.
        :type expression: X -> Y
        :return: The bag of values produced.
        :rtype Bag[Y]:

        Examples:
            >>> Set(2,3,5,-5).collectNested(lambda e:e*e) == Bag(25,25,4,9)
            True
            >>> Set(2,3).collectNested(lambda e:Bag(e,e)) == Bag(Bag(2,2),Bag(3,3))
            True
        """
        return asBag(map(expression,self.theSet))

    def sortedBy(self,expression):
        # FIXME: should return a OrderedSet
        return asSeq(sorted(self.theSet,key=expression))

    def asSet(self):
        return self

    def asBag(self):
        return asBag(self.theSet)

    def asSeq(self):
        return asSeq(self.theSet)


    def __str__(self):
        """
        Return a string representation of the set where elements are separated by ", ".

        The result is non deterministic as there is no ordering between elements.

        :return: A string.
        :rtype: str

        Examples:
            >>> str(Set())
            'Set()'
            >>> str(Set(3))
            'Set(3)'
            >>> str(Set(3,2)).startswith('Set(')
            True
        """
        body = ", ".join(map(str,self.theSet))
        return "Set(%s)" % body

    def __repr__(self):
        return self.__str__()

    def __eq__(self,value):
        """
        Return true if the value given is a Set and has exactly the same elements.

        :param value: Any value, but succeed only for sets.
        :type value: any
        :return: True if "value" is a set with the same elements.
        :rtype: bool

        Examples:
            >>> Set() == []
            False
            >>> Set() == Set()
            True
            >>> Set(2,3,3) == Set(3,2)
            True
            >>> Set(2,"3",4) == Set(2,4,3)
            False
            >>> Set("hello") == Set("hello")
            True
            >>> Set(Set(1)) == Set(Set(1))
            True
            >>> Set(Set(1),Set(2,1)) == Set(Set(1,2),Set(1))
            True
        """
        if not isinstance(value,Set):
            return False
        # print "check %s == %s -> %s" % (self.theSet,value.theSet,self.theSet == value.theSet)
        return self.theSet == value.theSet


    def __ne__(self,value):
        return not self.__eq__(value)

    def __hash__(self):
        return hash(frozenset(self.theSet))

    def __iter__(self):
        """ Make Sets iterable for pythonic usage.
        :return: the iterator for this Set
        """
        return self.theSet.__iter__()

    def __contains__(self,item):
        return item in self.theSet




def asBag(anyCollection):
    """
    :param anyCollection:
    :return:
    """
    if isinstance(anyCollection,Bag):
        return anyCollection
    try:
        return anyCollection.asBag()
    except AttributeError:
        return Bag() | anyCollection


from collections import Counter

class Bag(Collection):

    def __init__(self,*args):
        """
        Create a bag from some elements.

        Examples:
           >>> Bag(10,"a",3,10,10) == Bag(10,10,"a",3,10)
           True
           >>> Bag(2) <> Bag(2,2,2)
           True
           >>> Bag(3,3,4) == Bag(3,4,3)
           True
           >>> Bag(2,3) == Bag(3,2)
           True
           >>> Bag(Set(2,3),Set(3,2)).size()
           2
        """
        # We cannot have Counter here. So list is ok (see Converter.listAll)
        self.theCounter = Counter(list(args))

    def size(self):
        """
        Return the total number of elements in the bag.
        :rtype! int
        Examples:
           >>> Bag(10,"a",3,3,10,10).size()
           6
           >>> Bag(2).size()
           1
           >>> Bag().size()
           0
        """
        return sum(self.theCounter.values())

    def count(self,value):
        """
        Return the number of occurrences of a given value within the bag.

        Examples:
           >>> Bag(10,"a",3,3,10,10).count(10)
           3
           >>> Bag(2).count(5)
           0
           >>> Bag().count(2)
           0
           >>> Bag(Set(1),Set(1)).count(Set(1))
           2
        """
        return self.theCounter[value]

    def __getitem__(self,key):
        return self.theCounter[key]

    def __setitem__(self,key,value):
        self.theCounter[key] = value

    def __delitem__(self,key):
        del self.theCounter[key]


    def including(self,value):
        """
        Add a value into the bag.

        :param value: The value to be added.
        :type: any
        :return: The bag with one more occurrence of the value.
        :rtype: Bag

        Examples:
            >>> Bag(10,10,2,10).including(10) == Bag(10,10,10,10,2)
            True
            >>> Bag(10,10,2,10).including("a") == Bag(10,10,10,2,'a')
            True
            >>> Bag().including(34) == Bag(34)
            True
        """
        self.theCounter[value] += 1
        return self

    def excluding(self,value):
        """
        Remove *all* elements corresponding to the given value from the bag.

        :param value: Any value within the bag or not.
        :type: any
        :return: The bag without any occurrence of 'value'.
        :rtype: Bag

        Examples:
            >>> Bag(10,10,2,10).excluding(10) == Bag(2)
            True
            >>> Bag(10,10,2,10).excluding("a") == Bag(10,10,10,2)
            True
            >>> Bag().excluding(34) == Bag()
            True
        """
        del self.theCounter[value]
        return self

    def union(self,anyCollection):
        """
        Add to the bag all values in the collection given as a parameter.

        Examples:
           >>> Bag(10,"a",3,3,10,10).union(Bag(10,10,"b")) == Bag("b","a",3,3,10,10,10,10,10)
           True
           >>> Bag(2,4).union([2,4]) == Bag(2,2,4,4)
           True
           >>> Bag().union([1]) == Bag(1)
           True
           >>> Bag(3,3) | Set(3,3,3,2) == Bag(3,3,3,2)
           True
           >>> Bag(2,3,1) | Bag(3,3,2,4) == Bag(3,3,3,2,2,1,4)
           True
           >>> Bag(2,3,1) | Counter([3,3,2,4]) == Bag(3,3,3,2,2,1,4)
           True

        """
        assert isAnyCollection(anyCollection), \
            'Any collection expected, but found %s' % anyCollection

        self.theCounter.update(Converter.listAll(anyCollection))
        return self

    def __or__(self,anyCollection):
        return self.union(anyCollection)

    def intersection(self,anyCollection):
        """
        Retain only elements that are in common with the given collection.

        Examples:
            >>> Bag(10,"a",3,3,10,10).intersection(Bag(10,10,"b")) == Bag(10,10)
            True
            >>> Bag(2,4).intersection(Bag(2,4)) == Bag(2,4)
            True
            >>> Bag() & [1] == Bag()
            True
            >>> Bag(3,3) & Set(3,3,3,2) == Bag(3)
            True
        """
        assert isAnyCollection(anyCollection), \
            'Any collection expected, but found %s' % anyCollection
        self.theCounter = self.theCounter & Counter(list(anyCollection))
        return self

    def __and__(self,anyCollection):
        return self.intersection(anyCollection)

    def sum(self):
        """
        Return the sum of all elements in a bag including duplicates.

        :return: the sum of all elements .
        :rtype: int

        Examples:
            >>> Bag().sum()
            0
            >>> Bag(3,3,2,3).sum()
            11
        """
        return sum([e * n for (e,n) in self.theCounter.items()])

    def flatten(self):
        """
        If the bag is a bag of collection then return the bag union of all its elements.

        :return: the sum of all elements .
        :rtype: int

        Examples:
            >>> Bag(Bag(2),Bag(3,3)).flatten() == Bag(2,3,3)
            True
            >>> Bag(Bag(),Bag(),Bag(3,2),Set(3)).flatten()  == Bag(3,2,3)
            True
        """
        counter = Counter()
        for (e,n) in self.theCounter.items():
            if isAnyCollection(e):
                coll = e.flatten()
            else:
                coll = [e]
            for x in coll:
                counter[x] += n
        self.theCounter = counter
        return self

    def select(self,predicate):
        """
        Retain in the bag only the elements that satisfy the predicate.

        :param predicate: A predicate, that is a function returning a boolean.
        :return: The bag with only the selected elements.
        :rtype Bag:

        Examples:
            >>> Bag(2,3,2,3,-1,-2).select(lambda e:e>=0) == Bag(2,2,3,3)
            True
            >>> Bag().select(lambda e:True) == Bag()
            True
        """
        self.theCounter = \
            Counter(dict([(e,n) for (e,n) in self.theCounter.items() if predicate(e)]))
        return self

    def collectNested(self,expression):
        """
        Return a bag of values resulting from the evaluation of the given expression
        on all elements of the bag.

        It is assumed that the expression has no side effect; this expression is not
        called for each occurrence but only one for a given value. This is an
        optimisation for bags.

        :param expression: A function returning any kind of value.
        :type expression: X -> Y
        :return: The bag of values produced.
        :rtype Bag[Y]:

        Examples:
            >>> Bag(2,2,3,5,-5).collectNested(lambda e:e*e) == Bag(4,4,9,25,25)
            True
            >>> Bag(2,2).collectNested(lambda e:Bag(e,e)) == Bag(Bag(2,2),Bag(2,2))
            True
        """
        results = [(expression(e),n) for (e,n) in self.theCounter.items()]
        self.theCounter = Counter()
        for (r,n) in results:
            self.theCounter[r] += n
        return self

    def hasDuplicates(self):
        """
        Return True if this bag has at least one element with more than one occurrence.

        This is not an OCL operation. It is provided here just for convenience.
        :return: True if there are some duplicates.
        :rtype: bool

        Examples:
            >>> Bag().hasDuplicates()
            False
            >>> Bag(2,3).hasDuplicates()
            False
            >>> Bag(2,2,1,3,3).hasDuplicates()
            True
        """
        for n in self.theCounter.values():
            if n > 1:
                return True
        return False

    def sortedBy(self,expression):
        r = []
        for key in sorted(self.theCounter.keys(),key=expression):
            r += [key] * self.theCounter[key]
        return r

    def asSet(self):
        return asSet(self.theCounter.keys())

    def asBag(self):
        return self

    def asSeq(self):
        # A list with duplicates is wanted, so use elements().
        return asSeq(list(self.elements()))

    def __str__(self):
        return "Bag(%s)" % str(self.theCounter)

    def __repr__(self):
        return self.__str__()

    def __eq__(self,value):
        """
        Return True only if the value is a Bag with the same elements and number of occurrences.
        :param value: Any value.
        :type value: any
        :return: True if the value is equals to this bag.
        :rtype: bool

        Examples:
            >>> Bag(1,2,2) == Bag(2,2,1)
            True
            >>> Bag() == Bag()
            True
            >>> Bag(Bag(2,2)) == Bag(2,2)
            False
            >>> Bag(Set(2))==Bag(Set(2))
            True
        """
        if not isinstance(value,Bag):
            return False
        return self.theCounter == value.theCounter

    def __ne__(self,value):
        return not self.__eq__(value)

    def __hash__(self):
        return hash(frozenset(self.theCounter.items()))

    def __iter__(self):
        """ Make Bags iterable for pythonic usage.
        :return: the iterator for this Bag
        :rtype: iterator

        Examples:
            >>> list(Bag())
            []
            >>> sorted(list(Bag(1,1,"a","b",1)))
            [1, 1, 1, 'a', 'b']
        """
        return self.theCounter.elements()

    def __contains__(self,value):
        return self.theCounter[value] > 0




def asSeq(anyCollection):
    """
    Convert the given collection to a Seq
    :param anyCollection:
    :return:
    :rtype: Seq
    """
    if isinstance(anyCollection,Seq):
        return anyCollection
    try:
        return anyCollection.asSeq()
    except AttributeError:
        return Seq() | anyCollection


class Seq(Collection):
    def __init__(self,*args):
        """
        Create a Seq from some elements or from one collection.

        Examples:
           >>> Seq(10,"a",3,10,10) == Seq(10,10,"a",3,10)
           False
           >>> Seq(2) <> Seq(2,2,2)
           True
           >>> Seq(3,3,4) == Seq(3,4,3)
           False
           >>> Seq() == Seq()
           True
           >>> Seq() == Set()
           False
           >>> Seq(Seq(1,2)) == Seq(Seq(1),Seq(2))
           False
        """
        # no worry with args being a Counter
        self.theList = list(args)

    def size(self):
        return len(self.theList)

    def isEmpty(self):
        return True if self.theList else False

    def count(self,element):
        return self.theList.count(element)

    def includes(self,element):
        return element in self.theList

    def including(self,value):
        self.theList.append(value)
        return self

    def excluding(self,value):
        """
        Excludes all occurrence of the value from the sequence (if there).
        :param value: The element to add to the set.
        :type value: any
        :return: A set including this element.
        :rtype: Set
        Examples:
            >>> Seq(1,3,"a").excluding("3") == Seq(1,3,"a")
            True
            >>> Seq(1,3,3,2,3).excluding(3) == Seq(1,2)
            True
            >>> Seq().excluding(23) == Seq()
            True
        """
        self.theList = [e for e in self.theList if e != value]
        return self

    def select(self,expression):
        self.theList = [e for e in self.theList if expression(e)]
        return self

    def flatten(self):
        r = []
        for e in self.theList:
            if isAnyCollection(e):
                flat_list = Converter.listAll(flatten(e))
            else:
                flat_list = [e]
            r = r | flat_list
        self.theList = r
        return self


    def collectNested(self,expression):
        self.theList = map(expression,self.theList)
        return self

    def sortedBy(self,expression):
        self.theList = sorted(self.theList,key=expression)
        return self

    def union(self,anyCollection):
        assert isAnyCollection(anyCollection), \
            'Any collection expected, but found %s' % anyCollection
        self.theList = self.theList + Converter.listAll(anyCollection)
        return self

    def __or__(self,anyCollection):
        return self.union(anyCollection)

    def __add__(self,anyCollection):
        return self.union(anyCollection)

    def append(self,value):
        self.theList.append(value)
        return self

    def prepend(self,value):
        self.theList.insert(0,value)
        return self

    def subSequence(self,lower,upper):
        try:
            self.theList = self.theList[lower - 1:upper]
        except:
            raise Invalid(".subSequence(%s,%s) failed: No such element."%(lower,upper))
        return self

    def at(self,index):
        """
        Return the nth element of the sequence starting from 1.

        Note: In OCL the 1st element is at the index 1 while in python this is at 0.
        Both the OCL 'at' and python [] operators can be used, but remember the
        different way to index elements.

        Examples:
            >>> Seq(1,2,3,4).at(1)
            1
            >>> Seq(1,2,3,4)[0]
            1

        :param index: The index of the element to return, starting at:

         * 1 for the OCL 'at' operator.
         * 0 for the [] python operator.

        :type: int
        :return: The element at that position.
        :rtype: any
        """
        try:
            return self.theList[index - 1]
        except:
            raise Invalid(".at(%s) failed: No such element." % index)


    def __getitem__(self,item):
        return self.theList[item]

    def __setitem__(self,item,value):
        self.theList[item] = value

    def __delitem__(self,item):
        del self.theList[item]

    def asSet(self):
        return Set(self.theList)

    def asBag(self):
        return Bag(self.theList)

    def asSeq(self):
        return self

    def first(self):
        try:
            return self.theList[0]
        except:
            raise Invalid(".first() failed: No such element.")


    def last(self):
        try:
            return self.theList[-1]
        except:
            raise Invalid(".last() failed: No such element.")


    def __str__(self):
        return 'Seq(%s)' % self.theList

    def __repr__(self):
        return self.__str__()

    def __eq__(self,value):
        if not isinstance(value,Seq):
            return False
        return self.theList == value.theList

    def __hash__(self):
        return hash(tuple(self.theList))

    def __contains__(self,item):
        return item in self.theList

    def __iter__(self):
        return self.theList.__iter__()


class OrderedSet(Collection):
    pass













import platform
WITH_JYTHON = (platform.python_implementation() == 'Jython')

if WITH_JYTHON:
    # noinspection PyUnresolvedReferences
    import java.util
    # noinspection PyUnresolvedReferences
    from java.util import Collection as JavaCollection
    # noinspection PyUnresolvedReferences
    from java.util import List as JavaList
    # noinspection PyUnresolvedReferences
    from java.util import Set as JavaSet
    # noinspection PyUnresolvedReferences
    from java.lang import Iterable as JavaIterable


import collections

class Converter(object):

    #--- Python ----------------------------------------------------------
    PYTHON_CONVERSION_RULES = (
        (set,Set,asSet),
        (frozenset,Set,asSet),
        (collections.Counter,Bag,asBag),
        (list,Seq,asSeq),
        (tuple,Seq,asSeq),
        (collections.deque,Seq,asSeq),
        (collections.Iterable,Seq,asSeq),
    )
    PYTHON_COLLECTIONS = tuple([j for (j,o,c) in PYTHON_CONVERSION_RULES])


    #--- Java ------------------------------------------------------------
    if WITH_JYTHON:
        # noinspection PyUnresolvedReferences
        from java.util import Collection as JavaCollection
        # noinspection PyUnresolvedReferences
        from java.util import List as JavaList
        # noinspection PyUnresolvedReferences
        from java.util import Set as JavaSet
        # noinspection PyUnresolvedReferences
        from java.lang import Iterable as JavaIterable
        JAVA_CONVERSION_RULES = (
            (JavaSet,Set,asSet),
            (JavaList,Seq,asSeq),
            (JavaIterable,Seq,asSeq)
        )
    else:
        JAVA_CONVERSION_RULES = ()
    JAVA_COLLECTIONS = tuple([j for (j,o,c) in JAVA_CONVERSION_RULES])


    #--- OCL -------------------------------------------------------------
    OCL_CONVERSION_RULES = (
        (Set,Set,None),
        (Bag,Bag,None),
        (Seq,Seq,None),
    )
    OCL_COLLECTIONS = tuple([j for (j,o,c) in OCL_CONVERSION_RULES])

    EXTERNAL_CONVERSION_RULES = JAVA_CONVERSION_RULES+PYTHON_CONVERSION_RULES
    @classmethod
    def isPythonCollection(cls,value):
        return not isinstance(value,basestring) \
               and isinstance(value,cls.PYTHON_COLLECTIONS)

    @classmethod
    def isJavaCollection(cls,value):
        return isinstance(value,cls.JAVA_COLLECTIONS)

    @classmethod
    def isCollection(cls,value):
        return isinstance(value,Collection)

    @classmethod
    def isAnyCollection(cls,value):
        return cls.isCollection(value) \
               or cls.isJavaCollection(value) \
               or cls.isPythonCollection(value)

    @classmethod
    def asCollection(cls,anyCollection):
        if cls.isCollection(anyCollection):
            return anyCollection
        else:
            for (collection_type,target,fun) in cls.EXTERNAL_CONVERSION_RULES:
                if isinstance(anyCollection,collection_type):
                    return fun(anyCollection)
            raise ValueError("asCollection(): Can't convert a value of type %s." \
                             % type(anyCollection))

    @classmethod
    def listAll(cls,anyCollection):
        """
        Return all the elements of the collection as a list.

        This takes into account the Counter specificity: instead of using list and the
        standard enumeration on this collection this function use the "elements()"
        method. Otherwise occurrences are eliminated.
        """
        if isinstance(anyCollection,collections.Counter):
            return list(anyCollection.elements())
        else:
            return list(anyCollection)




def isAnyCollection(value):
        return Converter.isAnyCollection(value)

def asCollection(anyCollection):
    """
    Convert any collection either from python or java, into the proper (OCL) collection.

    :param anyCollection: A python, java or ocl collection.
    :return: The OCL collection
    :rtype: Collection

    Examples:
        >>> asCollection({2,3}) == Set(3,2)
        True
        >>> asCollection(frozenset({1,5,1})) == Set(1,5)
        True
        >>> asCollection(Counter([1,1,3,1])) == Bag(1,1,1,3)
        True
        >>> asCollection(Counter({'hello':2,-1:0})) == Bag('hello','hello')
        True
        >>> asCollection([1,2,3,4]) == Seq(1,2,3,4)
        True
        >>> asCollection((1,2,3,4)) == Seq(1,2,3,4)
        True
        >>> asCollection(deque([1,2,3,4])) == Seq(1,2,3,4)
        True
    """
    return Converter.asCollection(anyCollection)




# def asCollection(anyCollection):
#     if isCollection(anyCollection):
#         return anyCollection
#     elif isJavaCollection(anyCollection):
#         pass


def flatten(collection):
    """
    Return an OCL collection with all the elements at the first level.

    :param collection: The collection to be flatten
    :rtype collection: iterable[iterable]
    :return: A flatten collection.
    :rtype: Seq
    """
    try:
        return collection.flatten()
    except:
        return Seq([item for sub_collection in collection for item in sub_collection])


def flattenIfNeeded(c):
    if len(c) == 0 or not isAnyCollection(c[0]):
        return Seq(c)
    else:
        return flatten(c)


# JavaCollection.flatten = flatten
# JavaCollection.flattenIfNeeded = flattenIfNeeded
# JavaCollection.select = lambda c,f:Seq(filter(f,c))
# JavaCollection.reject = lambda c,f:Seq(filter(lambda x:not f(x),c))
# JavaCollection.collect = lambda c,f:Seq(map(f,c)).flattenIfNeeded()

if WITH_JYTHON:
    class JavaCollectionExtension(JavaCollection):
        # size()  java native
        # __len__ jython
        #        empty
        # isEmpty()  java native
        # __contains__ jython
        # contains
        # containsAll
        @staticmethod
        def includes(javaCollection,value):
            return javaCollection.contains(value)
        @staticmethod
        def excludes(javaCollection):
            return not javaCollection.contains(value)
        @staticmethod
        def includesall(javaCollection,anyCollection):
            return javaCollection.containsAll(anyCollection)


def notEmpty(anyCollection):
    return not anyCollection.isEmpty()

def count(anyCollection):
    pass


def excludesAll(anyCollection,anyCollection2):
    for value in anyCollection2:
        if anyCollection.includes(e):
            return False
    return True

def excluding(javaCollection,value):
    collection = asCollection(javaCollection)
    return collection.excluding(value)

def any(javaCollection,value):
    pass


# add
# addAll
# remove
# removalAll
# retainAll
# clear
#
# iterator
# toArray
# equals
# hashCode



# execute tests if launched from command line
if __name__ == "__main__":
    import doctest
    doctest.testmod()