# coding=utf-8

import os
from collections import OrderedDict

def isConstant(name):
    import re
    return re.match(r"^[A-Z][A-Z_]*$",name) is not None


def getConstantMap(entity):
    constants = filter(isConstant,(entity.__dict__.keys()))
    return OrderedDict(sorted({c:getattr(entity,c) for c in constants}.items()))

def ensureDirectory(directory):
    """
    Create a directory if not existing.
    :param directory: The directory to check.
    :type: str
    :return: True if a new directory has been created
    :rtype: bool
    """
    if not os.path.isdir(directory):
        os.mkdir(directory)
        return True
    else:
        return False


