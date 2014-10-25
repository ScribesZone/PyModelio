# coding=utf-8

import os
import fnmatch

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

def findFile(name,path):
    for root,dirs,files in os.walk(path):
        if name in files:
            return os.path.join(root,name)
    return None


def findFiles(pattern,path):
    """
    Find the list of files matching a given unix-like glob pattern.

    To search a particular file, do not includes wildcards in the pattern.
    But in all cases, a set of files is returned (various files can have the same
    name). Use findFile if only one file has to be returned.

    :param pattern: A unix glob pattern (e.g. '*.py')
    :type pattern: str
    :param path: The directory where to start.
    :type path: str
    :return: The list of file names matching the pattern.
    :rtype: list[str]
    """
    result = []
    for root,dirs,files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name,pattern):
                result.append(os.path.join(root,name))
    return result

