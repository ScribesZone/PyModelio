# -*- coding: utf-8 -*-


import os
import sys

#FIXME constant
EDITOR              = 'c:\\S\\Notepad++\\notepad++.exe'
EDITOR_OPEN_FILE    = [EDITOR, '{file}']
EDITOR_OPEN_FILE_AT = [EDITOR, '{file}', '-n{line}]']

from subprocess import Popen
# DETACHED_PROCESS = 0x00000008

def edit(file=None, line=None):
    def replace(pattern):
        return pattern.format(file=file,line=line)

    if file is None \
            or EDITOR_OPEN_FILE is None \
            or EDITOR_OPEN_FILE_AT is None:
        if EDITOR is not None:
            cmd = [EDITOR]
        else:
            print 'WARNING: The Python Variable EDITOR is not defined.'
            print '         Cannot launch an editor.'
            return
    elif line is None:
        cmd = map (replace, EDITOR_OPEN_FILE)
    else:
        cmd = map (replace, EDITOR_OPEN_FILE_AT)
    Popen(cmd, shell=False, stdin=None, stdout=None, stderr=None,
          close_fds=True)  #, creationflags=DETACHED_PROCESS)

