# coding=utf-8


def macro_coexplorer(context):
    print "importing explorer ...",
    import explorer
    print "done"
    selected_elements = context.getSelectedElements()
    n = len(selected_elements)
    print "explore ",n,"element",("" if n <= 1 else "s")
    try:
        coexplorer = explorer.explore(selected_elements)
    except Exception as e:
        print e


def macro_script_remote_edit(context):
    import pymodelio.core.scripts
    if 'ONLINE_PY_SCRIPT' not in globals():   #FIXME
        ONLINE_PY_SCRIPT = pymodelio.core.scripts.OnlinePyScript(globals())
    ONLINE_PY_SCRIPT.edit()  #FIXME


def macro_script_remote_new(context):
    import pymodelio.core.scripts
    if 'ONLINE_PY_SCRIPT' not in globals():  #FIXME
        ONLINE_PY_SCRIPT = pymodelio.core.scripts.OnlinePyScript(globals())
    print 'Creating a new script on collabedit.com ...',
    editUrl = ONLINE_PY_SCRIPT.new()
    print 'done'
    print 'Your script is available at %s' % editUrl
    print 'Remember to change the language to "python"' \
          ' when visiting this address.'

def macro_script_remote_run(context):
    import pymodelio.core.scripts
    if 'ONLINE_PY_SCRIPT' not in globals():  #FIXME
        ONLINE_PY_SCRIPT = pymodelio.core.scripts.OnlinePyScript(globals())
    ONLINE_PY_SCRIPT.run()
