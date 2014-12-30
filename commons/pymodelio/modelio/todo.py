# coding=utf-8

import os
import re

import pymodelio.env.filewatcher


def todoListener(changes):
    for line in changes.split('\n'):
        m = re.match('^select (?P<id>\w+)$', line)
        if m:
            print 'SELECT',m.group('if')
            # TODO: to be implemented
        else:
            print 'IGNORED', line



def registerTodoListener():
    TODO_FILE = os.path.join(
        os.path.expanduser('~'),'.modelio', 'pymodelio_todo_list.txt')

    watcher = pymodelio.env.filewatcher.FileWatcher(0.5)
    watcher.watchFile(TODO_FILE, todoListener)
    return watcher


WATCHER = registerTodoListener()


