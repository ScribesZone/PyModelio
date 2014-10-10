from metascribe_introspection import explore


def macro_coexplorer(scribeExecution):
  n = len(scribeExecution.selectedElements)
  print "explore ",n,"element",("" if n<=1 else "s")
  coexplorer = explore(scribeExecution.selectedElements)
