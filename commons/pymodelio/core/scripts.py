# coding=utf-8

"""
This module allows to manage scripts, that is python script executed in
the context of modelio. Scripts can either be local files or remote files
available (and possibly editable) online. This is useful for collaborative
scripting and in particular collaborative production of model transformations
or text generators. Script can be editable, with the editor specified
in the case of local script and with online service (if available) in
the case of remote script. Currently collabedit.com is used as a
collaborative editor, but this can easily be changed.
"""

# noinspection PyUnresolvedReferences
import encodings
import urllib2
import cookielib
import re
import os
import collections

import pymodelio.env.webbrowser
import pymodelio.env.editor
import pymodelio.core.env

COLLAB_HOST = 'http://collabedit.com/'
COLLAB_NEW = 'http://collabedit.com/new'
COLLAB_GET = 'http://collabedit.com/download?id=%s'
COLLAB_EDIT = 'http://collabedit.com/%s'

class Script(object):
    def __init__(self, code):
        self.code = code

    def run(self):
        exec self.code in ScriptRegistry.executionScope


class ScriptRegistry(object):
    defaultDirectory = pymodelio.core.env.PyModelioEnv.LOCAL_SCRIPTS
    executionScope = None
    scripts = collections.OrderedDict()

    @classmethod
    def add(cls, name, script):
        cls.scripts[name] = script


class LocalScript(Script):

    def __init__(self, fileName):
        Script.__init__(self, None)
        self._computeFileName(fileName)
        self.name = os.path.splitext(os.path.basename(fileName))[0]
        ScriptRegistry.add(self.name, self)

    def edit(self):
        pymodelio.env.editor.edit(self.fileName)

    def run(self):
        self._getCode()
        Script.run(self)

    def _getCode(self):
        with open(self.fileName, mode='r') as f:
            self.code = f.read()

    def _computeFileName(self, fileName):
        if os.path.isabs(fileName):
            self.fileName = fileName
        else:
            self.fileName = \
                os.path.join(ScriptRegistry.defaultDirectory, fileName)

class RemoteScript(Script):
    def __init__(self, executionScope, name, url=None, editUrl=None):
        """
        Define a new online pyscript.
        :param executionScope: The scope in which the script is executed.
        This is most probably the globals() from the top level.
        :type executionScope:
        :param url: The url of the online script or None.
        This url could be set later.
        :type url: str|None
        :param editUrl: The url that allows to edit this script if any.
        If None, the script is not editable.
        :type editUrl: str|None
        :rtype: NoneType
        """
        Script.__init__(self, None)
        self.name = name
        self.url = url
        self.editUrl = editUrl
        self.cookieJar = cookielib.CookieJar()
        self.webOpener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self.cookieJar))
        ScriptRegistry.add(self.name, self)

    def set(self, collabIdOrAnyURL, editUrl=None):
        """
        Set the url/edit url of the py script.
        :param collabIdOrAnyURL:  The url of the online script.
        :type collabIdOrAnyURL: str
        :param editUrl: The url to edit the script or none.
        :type editUrl: str|None
        :rtype: NoteType
        """
        (url, edit_url) = self._computeURL(collabIdOrAnyURL, editUrl)
        try:
            self.webOpener.open(url)
        except:
            print 'ERROR: cannot read script at %s' % url
            raise
        self.url = url
        self.editUrl = edit_url


    def new(self):
        try:
            newurl = self.webOpener.open(COLLAB_NEW).geturl()
            document_id = re.match(
                COLLAB_HOST + r'(?P<id>\w+)', newurl).group('id')
            (url, edit_url) = self._computeURL(document_id)
            self.url = url
            self.editUrl = edit_url
            return newurl
        except:
            print 'ERROR: Cannot get the reference to a new document '
            raise


    def edit(self):
        """
        Open a web browser to edit the py script. If the url for edition
        is not defined then just display a message in the console.
        :rtype:
        """
        if self._ifURLIsDefined():
            if self.editUrl is None:
                print 'No url defined for editing the script'
            else:
                pymodelio.env.webbrowser.open(self.editUrl)

    def run(self):
        """
        Execute the py script
        :return:
        :rtype:
        """
        self._getCode()
        if self.code is not None:
            Script.run(self)

    #----------------------------------------------------------
    #   Class implementation
    #----------------------------------------------------------

    def _computeURL(self, collabIdOrAnyURL, editUrl=None):
        if collabIdOrAnyURL.startswith(COLLAB_HOST):
            collab_id = re.match(
                COLLAB_HOST + r'(?P<id>\w+)', collabIdOrAnyURL).group('id')
            return (COLLAB_GET % collab_id,
                    COLLAB_EDIT % collab_id)
        elif collabIdOrAnyURL.startswith('http'):
            return (collabIdOrAnyURL, editUrl)
        else:
            return (COLLAB_GET % collabIdOrAnyURL,
                    COLLAB_EDIT % collabIdOrAnyURL)

    def _getCode(self):
        if self._ifURLIsDefined():
            self.code = self.webOpener.open(self.url).read()
        else:
            self.code = None

    def _ifURLIsDefined(self):
        if self.url is None:
            print 'No online document has been defined.'
            print 'You can either create a new document'
            print 'with the button  "Online > New" or if you'
            print 'the document already exist you can type'
            print 'OnlinePyScript.set("<url>") in the'
            print 'python console'
        return self.url is not None

    # def getSettingsFile(self):
    #     return os.path.join(
    #         os.path.expanduser('~'),
    #         '.modelio',
    #         'pymodelio',
    #         'settings.py')
    #
    #     # execfile(settings_file)
