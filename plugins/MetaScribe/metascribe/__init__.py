# coding=utf-8

from metascribe.explorer import explore,exp


def macro_coexplorer(context):
    selected_elements = context.getSelectedElements()
    n = len(selected_elements)
    print "explore ",n,"element",("" if n <= 1 else "s")
    try:
        coexplorer = explore(selected_elements)
    except Exception as e:
        print e
