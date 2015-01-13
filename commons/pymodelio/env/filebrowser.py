# -*- coding: utf-8 -*-


#FIXME constant
FILEBROWSER_OPEN_PATH = ['explorer','{path}']
FILEBROWSER_SHOW_PATH = ['explorer', '/select,{path}']

from subprocess import Popen


def openBrowser(path,open=True):
    def replace(pattern):
        return pattern.format(path=path)
    if open:
        pattern = FILEBROWSER_OPEN_PATH
    else:
        pattern = FILEBROWSER_SHOW_PATH
    if pattern is None:
        print 'WARNING: Variable %s not defined.' % pattern
        print '         Cannot %s directory %s.' % (
            ('open' if open else 'show'), path )
        return
    else:
        cmd = map(replace, pattern)
    Popen(cmd, shell=False, stdin=None, stdout=None, stderr=None,
          close_fds=True)  #, creationflags=DETACHED_PROCESS)

