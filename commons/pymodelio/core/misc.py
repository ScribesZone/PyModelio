# coding=utf-8

from collections import OrderedDict

def isConstant(name):
    import re
    return re.match(r"^[A-Z][A-Z_]*$",name) is not None


def getConstantMap(entity):
    constants = filter(isConstant,(entity.__dict__.keys()))
    return OrderedDict(sorted({c:getattr(entity,c) for c in constants}.items()))


