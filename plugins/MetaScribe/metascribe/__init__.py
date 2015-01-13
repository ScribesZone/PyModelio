# coding=utf-8

import explorer

def macro_coexplorer(context):
    selected_elements = context.getSelectedElements()
    n = len(selected_elements)
    print "explore ",n,"element",("" if n <= 1 else "s")
    try:
        coexplorer = explorer.explore(selected_elements)
    except Exception as e:
        print e
