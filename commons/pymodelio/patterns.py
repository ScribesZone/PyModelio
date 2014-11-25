# coding=utf-8

import pymodelio.misc
from pymodelio.misc import withCapital

# split a potentially prefixed string in two parts:
# (1) the prefix (or "" if not found)
# (2) the body capitalized
# (3) the original string
def splitWithPrefix(prefix,name):
  if name.startswith(prefix):
    return (prefix,withCapital(name[len(prefix):]),name)
  else:
    return ("",withCapital(name),name)

# just like splitWithPrefix but tries with various prefixes
# and return the first one that match     
def splitWithPrefixes(prefixes,name):
  for prefix in prefixes:
    (prefixFound,body,nameAsIs) = splitWithPrefix(prefix,name)
    if prefixFound is not "":
      return (prefixFound,body,nameAsIs)
  return ("",withCapital(name),name)

# return a map with for each body strings, the set of prefixes
# x = ["getA","setB","b","g","setG","getB","u"]
# print prefixedPatterns(["get","set","card"],x)
# >>> {'U': [""], 'B': ["", 'get', 'set'], 'G': ["", 'set'], 'A': ['get']}
def prefixedPatterns(prefixes,names):
  splittedNames = map(lambda n: splitWithPrefixes(prefixes,n), names)
  patterns = {}
  for (prefix,body,nameAsIs) in splittedNames:
    if body in patterns:
      patterns[body]=sorted(patterns[body]+[(prefix,nameAsIs)])
    else:
      patterns[body]=[(prefix,nameAsIs)]
  return patterns


ACCESSOR_PREFIXES = ["get","card","is"]
MODIFIER_PREFIXES = ["set","add","remove"]
PATTERN_PREFIXES = ACCESSOR_PREFIXES+MODIFIER_PREFIXES
PATTERN_PROFILE_PROPERTIES = {
    ""                         : ("Derived","",""),
    " get"                     : ("Stored","RO",""),
    " is"                      : ("Stored","RO","[1]"),
    "is"                       : ("Derived","","[1]"),
    " is set"                  : ("Stored","","[1]"),
    " get set"                 : ("Stored","RW","[1]"),
    " add card get remove"     : ("Stored","RW","[*]"),
    "get remove"               : ("Derived","RW","[*]"),      # this is strange
    "add remove"               : ("Derived","RW","[*]") }
    
def patternProperties(patternProfile):
  return PATTERN_PROFILE_PROPERTIES[" ".join(patternProfile)]
