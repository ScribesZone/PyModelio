# coding=utf-8

from metascribe.introspection import explore


def macro_coexplorer(context):
  selected_elements = context.getSelectedElements()
  n = len(selected_elements)
  print "explore ",n,"element",("" if n<=1 else "s")
  coexplorer = explore(selected_elements)