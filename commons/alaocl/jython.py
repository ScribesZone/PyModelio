from alaocl import *
import types


#=====================================================================================
#   Functions and decorators to instrument existing classes
#=====================================================================================

def addSuperclass(superclassOrSuperclasses,subclassOrSubclasses):
    """
    Add a (list of) superclasses to a(list of) subclass(es) and this after the fact.

    See the @superclassof decorator for more information. This version is more
    general as it can take various superclasses and it can be used both after
    the definition of subclasses but also superclasses.

    :param superclassOrSuperclasses: A class or a list of classes to be added as
    superclass(es) to the subclasses.
    :type superclassOrSuperclasses: objectclass|list[objectclass]
    :param subclassOrSubclasses: A class or a list of classes to be instrumented.
    :type subclassOrSubclasses: type|tuple[type]
    :return: Nothing
    :rtype: NoneType
    """
    # print superclassOrSuperclasses,type(superclassOrSuperclasses)
    if isinstance(superclassOrSuperclasses,(types.TypeType, types.ClassType)):
        superclasses = (superclassOrSuperclasses,)
    else:
        superclasses = tuple(superclassOrSuperclasses)
    if isinstance(subclassOrSubclasses,(types.TypeType, types.ClassType)):
        subclasses = [subclassOrSubclasses]
    else:
        subclasses = list(subclassOrSubclasses)
    for subclass in subclasses:
        # print "adding %s to %s with %s" % (superclasses,subclass,subclass.__bases__)
        if object in subclass.__bases__:
            others = list(subclass.__bases__)
            others.remove(object)
            subclass.__bases__ = tuple(others) + superclasses + (object,)
        else:
            subclass.__bases__ = subclass.__bases__ + superclasses
        # print "    = %s " % str(subclass.__bases__)



def superclassof(subclassOrSubclasses):
    """
    Class decorator allowing to add *after the fact* a super class to one
    or various classes given as parameter.

    This decorator is useful to add behavior to existing libraries or classes
    that cannot be modified. Python builtin classes cannot be modified.
    In the context of jython it works well, but only on direct concrete class.
    That is, java implement and inheritance graph is not followed.
    :param subclassOrSubclasses: the class or the list of class to add the
    superclass to. That is this (these) class(es) become subclasses of the
    superclass decorated. See the examples provided below.
    :param subclassOrSubclasses: class|tuple[class]|list[class]

    This decorator must be applied to a class that do not inherits *directly* from
    'object'. In this case just use old class style.

    Example
    -------

    In the example below two classes *Kangaroo* and *ColoredKangaroo* are assumed
    to be defined in a (weired) library. For some reasons their source codes cannot
    modified. We want however to add *Animal* as a superclass of *Kangaroo*
    and *ColoredAnimal* as a superclass of *ColoredKangaroo* .

    First let's start with the existing library:

        >>> class Kangaroo(object):
        ...     def who(self):
        ...         return "kangaroo"
        >>> class ColoredKangaroo(Kangaroo):
        ...     def __init__(self,color):
        ...         self.color = color
        ...     def who(self):
        ...         return self.color+" "+super(ColoredKangaroo,self).who()

    This library being defined somewhere, the *Animal* (old-style) class
    is added after the fact to the existing class; here to *Kangaroo* because
    this is the root class in the library.

        >>> @superclassof(Kangaroo)
        ... class Animal:                       # not class Animal(object)
        ...     def who(self):
        ...         return "animal"
        ...     def babies(self):
        ...         return "babies are %ss" % self.who()

    Then a superclass is defined for all colored animals. Here we have only
    one subclass to instrument be we still use [ ] to show that the decorator
    accept a list of classes to be instrumented.

        >>> @superclassof([ColoredKangaroo])
        ... class ColoredAnimal(Animal):
        ...     def getColor(self):
        ...         return self.color

    Now it is time to play with animals and kangaroos.

        >>> k = Kangaroo()
        >>> print k.who()
        kangaroo

    Using the method *babies* added in the *Animal* superclass shows that
    polymorphism work properly. Otherwise it would say that babies are "animals".

        >>> print k.babies()
        babies are kangaroos

    Now we can check that subclasses work properly as well.

        >>> bk = ColoredKangaroo("blue")
        >>> print bk.who()
        blue kangaroo
        >>> print bk.babies()
        babies are blue kangaroos

    In particular is is important to check what happen when a superclass
    has been added to a subclass. This is the case for *ColoredAnimal* and the
    method *getColor*.

        >>> print bk.color
        blue
        >>> print bk.getColor()
        blue
    """
    def decorate(superclass):
        # if isinstance(subclassOrSubclasses,type):
        #     subclasses = [subclassOrSubclasses]
        # else:
        #     subclasses = list(subclassOrSubclasses)
        # for subclass in subclasses:
        #     if object in subclass.__bases__:
        #         subclass.__bases__ = (superclass,object)
        #     else:
        #         subclass.__bases__ = subclass.__bases__ + (superclass,)
        addSuperclass(superclass,subclassOrSubclasses)
        return superclass
    return decorate






#=====================================================================================
#   Functions and decorators to instrument existing classes
#=====================================================================================

# noinspection PyUnresolvedReferences
import java.util



class JavaCollectionExtension(GenericCollection):
    """

    """
    # size()  java native
    # __len__ jython
    #        empty
    # isEmpty()  java native
    # __contains__ jython
    # contains
    # containsAll

    def includes(self,value):
        """
            >>> java.util.ArrayList([1,2]).includes(2)
            True
            >>> java.util.ArrayList([1,2]).includes(8)
            False
        """
        return self.contains(value)

    def excludes(self,value):
        """

        """
        return not self.contains(value)

    def includesAll(self,anyCollection):
        """
        """
        return self.containsAll(anyCollection)

    def including(self,value):
        self.add(value)
        return self

    def excluding(self,value):
        self.remove(value)
        return self

    def union(self,anyCollection):
        self.addAll(anyCollection)
        return self

    def intersection(self,anyCollection):
        self.retainAll(anyCollection)
        return self

    def __and__(self,anyCollection):
        return self.intersection(anyCollection)


    def count(self,element):
        pass

    def select(self,expression):
        pass

    def flatten(self):
        pass

    def collectNested(self,expression):
        pass

    def sortedBy(self,expression):
        pass

    def asSet(self):
        return asSet(self)

    def asBag(self):
        return asBag(self)

    def asSeq(self):
        return asSeq(self)


class JavaSetExtension(JavaCollectionExtension):

    def count(self,value):
        return 1 if value in self.theSet else 0

    def difference(self,anyCollection):
        self.removeAll(anyCollection)
        return self

    def symmetricDifference(self,anyCollection):
        assert isAnyCollection(anyCollection), \
            'Any collection expected, but found %s' % anyCollection
        other_set = set(anyCollection)
        this_set = set(self)
        self.addAll(other_set)
        self.removeAll(this_set & other_set)
        # FIXME: to be checked and tested
        return self

    def flatten(self):
        r = set()
        for e in self:
            if isAnyCollection(e):
                flat_set = set(flatten(e))
            else:
                flat_set = {e}
            r = r | flat_set
        self.theSet = r
        return self


class JavaListExtension(JavaCollectionExtension):
    def toto(self):
        print "toto"


# noinspection PyUnresolvedReferences
import java.util

JAVA_JDK_LISTS = [
    java.util.ArrayList,
    java.util.Vector,
    java.util.LinkedList,
]

JAVA_JDK_SETS = [
    java.util.EnumSet,
    java.util.HashSet,
    java.util.TreeSet,
]

JAVA_JDK_COLLECTIONS = JAVA_JDK_SETS + JAVA_JDK_LISTS

# addSuperclass(JavaCollectionExtension,JAVA_JDK_COLLECTIONS)
addSuperclass(JavaSetExtension,JAVA_JDK_SETS)
addSuperclass(JavaListExtension,JAVA_JDK_LISTS)



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