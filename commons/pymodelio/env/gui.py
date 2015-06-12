# coding=utf-8
#
# gui
#
# Helpers for building Graphical User Interfaces (GUI)
#
# Licence: GPL
# Author: jmfavre
#
# Useful resources about SWT can be found on the link below:
#               http://www.eclipse.org/swt/widgets/

#---------------------

import traceback


#----- graphical user interface -----------------------------------------------

# noinspection PyUnresolvedReferences
from org.eclipse.swt import SWT
# noinspection PyUnresolvedReferences
from org.eclipse.swt.widgets import \
    Shell,Display,Label,Button,Listener,Text,Menu,MenuItem,FileDialog
# noinspection PyUnresolvedReferences
from org.eclipse.swt.widgets import ToolBar,ToolItem
# noinspection PyUnresolvedReferences
from org.eclipse.swt.browser import Browser
# noinspection PyUnresolvedReferences
from org.eclipse.swt.layout import GridData,GridLayout,FillLayout

import os
# noinspection PyUnresolvedReferences
from org.eclipse.swt.graphics import Color,Image
# noinspection PyUnresolvedReferences
from org.eclipse.swt.widgets import Display

import re


#---- workbench ---------------------------------------------------------------
def getWorkbench():
    """
    Returns the Eclipse UI workbench.
    ATTENTION: This method currently does not work with modelio 3 (BUG).
    :return: The modelio workbench
    :rtype: IWorkbench
    """
    # noinspection PyUnresolvedReferences
    from org.eclipse.ui import PlatformUI
    return PlatformUI.getWorkbench()



#---- display and shells  -----------------------------------------------------

def getDisplay():
    """
    Return the default Eclipse display.
    :return: The eclipse display.
    :rtype: Display
    """
    return Display.getDefault()

def getActiveShell():
    """
    Return the active shell.
    :return: The active shell.
    :rtype: Shell
    """
    return Display.getDefault().getActiveShell()

def getShells():
    """
    Return the list of eclipse shells.
    :return: The list of shells.
    :rtype: list
    """
    return Display.getDefault().getShells()



def getMainShell():
    """
    Returns the main modelio shell. This should be the only windowd that ends
    with somethin like ' - Modelio 3.3'
    :return: the main shell of modelio
    :rtype: Shell
    """
    for shell in Display.getDefault().shells:
        if re.match('.* - Modelio \d+\.\d+$', shell.text):
            return shell
    raise Exception('Error. Cannot find the main modelio window')



def shell(  parent=getActiveShell(),
            options=SWT.CLOSE | SWT.RESIZE,
            layout = FillLayout):
    """
    Create a new shell.
    :param parent:
    :type parent:
    :param options:
    :type options:
    :param layout:
    :type layout:
    :return:
    :rtype:
    """
    s = Shell(parent, options)
    layout = layout
    return s










#--- introspection ------------------------------------------------------------

def _getAttributeValue(x, name):
    """
    Return tha value of the attribute if this is a simple attribute or
    the result of the execution of the attribute if this is a function/method.
    If no such attribute exist, an exception is raised.
    If the function execution raise an error, raise it.
    """
    if not hasattr(x, name):
        raise Exception(
            "No attribute %s on %s"
            % (name, x))
    else:
        attr = getattr(x, name)
        if not hasattr(attr, '__call__'):
            return attr
        else:
            return attr()

def _succ(x, names):
    _ = []
    if isinstance(names, basestring):
        names = [names]
    for name in names:
        if hasattr(x, name):
            try:
                output = _getAttributeValue(x, name)
            except:
                print("Warning. Exception for .%s/() on %s"
                      % (name,x))
                results = []
            else:
                try:
                    # get a tuple if iterable
                    results = [r for r in output]
                except TypeError:
                    # not iterable, make the tuple
                    results = [output]
            _.extend(results)
    return _

def _succ1(x, names):
    successors = _succ(x, names)
    size = len(successors)
    if size == 0:
        return None
    elif size == 1:
        return successors[0]
    else:
        raise Exception('ERROR: more than one successors for .%s on %s'
            % (str(names),str(x)))


def ancestors(x, names=('getParent', )):
    ancestor = _succ1(x, names)
    if ancestor is None:
        return ()
    else:
        return ancestors(ancestor, names) + (ancestor, )


def _checkItemKind(object, kind=None):
    # if a string is provided then this is the fully qualified exact type
    # of the object to get. For some strange reasons some java types do not
    # have name attributes. It this case the type representation is used.
    if kind is None:
        return True
    elif isinstance(kind, basestring):
        t = type(object)
        if hasattr(t,'name'):
            type_name = t.name
        else:
            type_name = str(t)
            # print "WARNING: The type has no name attribute %s" % type_name
        return kind == type_name
    else:
        return isinstance(object, kind)

def _checkItemAttribute(object, attribute=None, value=None):
    if attribute is None:
        return True
    elif not hasattr(object, attribute):
        return False
    else:
        try:
            attribute_value = _getAttributeValue(object, attribute)
        except:
            return False
        else:
            return value == attribute_value

def _checkItem(object, kind=None, attribute=None, value=None):
    return (
        _checkItemKind(object, kind=kind)
        and _checkItemAttribute(object, attribute=attribute, value=value)
    )









def allWidgets(root=getMainShell(), kind=None, attribute=None, value=None,
               successors=('getChildren', 'getItems', 'getContents')):
    """
    Return all the elements contained in the root element according to
    the given successors, ('getChildren', 'getItems', 'getContents') by default.
    """
    _ = []
    if _checkItem(root, kind=kind, attribute=attribute, value=value):
        _.append(root)
    for child in _succ(root, successors):
        _.extend(allWidgets(
            root=child, kind=kind, attribute=attribute, value=value,
            successors=successors))
    return _




def printWidgetTree(root=getMainShell(),  indent='',
                    successors=('getChildren', 'getItems', 'getContents')):
    print indent, root, ':', type(root)
    for child in _succ(root, successors):
        printWidgetTree(root=child, indent=indent + '    ')


# example: printWidgetTree(getModelioShell())


def getMainMenu():
    return getMainShell().menuBar

def printMenuTree(shell=getMainShell()):
    print '*** WARNING: works only for two levels for now (enough for modelio)'
    print '*** WARNING: only works if submenu have been displayed before'
    for menuItem in shell.menuBar.items:
        print menuItem
        if menuItem.menu is not None:
            for subI in menuItem.menu.items:
                print '    ', subI

import inspect
# noinspection PyUnresolvedReferences
from org.eclipse.swt.events import SelectionListener

def newMenuItem(text, fun, menu=getMainMenu()):
    """
    Add a new menu item into an existing menu (the main modelio menu by
    default). Just provide a label and a call back function.
    :param text: the label to be used for the menu item
    :type text: basestring
    :param fun: the function that will be called when the menu item is
        selected. This function must have one or zero argument. In the later
        case the event will be given as the first parameter.
    :type fun: callable
    :param menu: the menu where to insert to menu item. By default this is
        the main menu of modelio.
    :type menu: Menu
    :return: the menu item just created.
    :rtype: MenuItem
    """
    menu_item = MenuItem(menu, SWT.PUSH)
    menu_item.setText(text)
    #-- define the call back using fun and passing even/removing event as necessary
    fun_args = inspect.getargspec(fun).args
    if len(fun_args) == 0:
        def call_back(event):
            fun()
    elif len(fun_args) == 1:
        def call_back(event):
            fun(event)
    else:
        raise Exception(
            'The function provided has more that one argument:  %s' % str(
                fun_args))

    class _Listener(SelectionListener):
        def widgetSelected(self, event):
            call_back(event)

        def widgetDefaultSelected(self, event):
            call_back(event)

    menu_item.addSelectionListener(_Listener())
    return menu_item






def getCTabItems():
    """
    Return the list of all CTabItem s. Use the .control attribute to get
    the content of each tab.
    :return: the list of all CTabItem widgets
    :rtype: list(org.eclipse.swt.custom.CTabItem)
    """
    return allWidgets(
        kind='org.eclipse.swt.custom.CTabItem')

def getCTabItem(name):
    """
    Select a CTabItem by name. Raise an exception if there is no such tab
    or more than one tab with this name.
    :param name: the name that
    :type name: str
    :return: the selected CTabItem
    :rtype: org.eclipse.swt.custom.CTabItem
    """
    ws = allWidgets(
        kind='org.eclipse.swt.custom.CTabItem', attribute='text', value=name)
    if len(ws) != 1:
        raise Exception(
                'Not exactly one getCTabItem: %s.'
                'The windows might be closed or in another window'
                % str(len(ws)))
    return ws[0]


def squatCTab(ctabName, newCTabName=None):
    """
    find by name a CTab to squat. Return the top control of this squat.
    Rename the tab if newCTabName is given.
    :param ctabName:
    :type ctabName:
    :param newCTabName:
    :type newCTabName:
    :return:
    :rtype:
    """
    ctab = getCTabItem(ctabName)
    top_control = ctab.control
    if newCTabName is not None:
        ctab.text = newCTabName
    return top_control


# squat = squatCTab('Audit')
# b = Button(squat, SWT.PUSH)
# b.text ="x"
# squat.layout()
# squat.children[0].hidden = True ?
# squat.parent.pack()
# squat.layout()




#---- modelio script widget ---------------------------------------------------

 # SashForm {} : <type 'org.eclipse.swt.custom.SashForm'>
 #     OutputView {} : <type 'org.modelio.script.view.OutputView'>
 #     Canvas {} : <type 'org.eclipse.swt.widgets.Canvas'>
 #         StyledText {} : <type 'org.eclipse.swt.custom.StyledText'>
 #         CompositeRuler$CompositeRulerCanvas {} : <type 'org.eclipse.jface.text.source.CompositeRuler$CompositeRulerCanvas'>
 #             LineNumberRulerColumn$4 {} : <type 'org.eclipse.jface.text.source.LineNumberRulerColumn$4'>
 #     Sash {} : <type 'org.eclipse.swt.widgets.Sash'>

def getScriptCTabItem():
    return getCTabItem('Script')

def modelioScriptOutputWidget():
    widgets = allWidgets(kind='org.modelio.script.view.OutputView')
    return widgets[0]

def modelioScriptWidget():
    return modelioScriptOutputWidget().parent

def modelioScriptInputWidget():
    """
    the textual part of the input (not the line number in another widget)
    """
    return allWidgets(modelioScriptWidget(),
                      kind='org.eclipse.swt.custom.StyledText')[0]

def modelioCTabFolderContainingScriptView():
    return modelioScriptWidget().parent.parent.parent

# scriptViewFolder = allWidgets(kind='org.eclipse.swt.custom.CTabFolder')[0]




#------ views composites ------------------------------------------------------


def getOutlineCTabItem():
    """
    Return the CTabItem of modelio "Outline" view.
    :return:
    :rtype: CTabItem
    """
    return getCTabItem('Outline')

def getOutlineComposite():
    return getOutlineCTabItem().control.children[0].children[0]


def demoAddBrowserInOutlineView():
    # noinspection PyUnresolvedReferences
    from org.eclipse.swt.widgets import Button
    # noinspection PyUnresolvedReferences
    from org.eclipse.swt.browser import Browser
    # noinspection PyUnresolvedReferences
    from org.eclipse.swt import SWT

    c = getOutlineComposite()
    b = Browser(c, SWT.BORDER)
    b.setUrl('http://modelio.org/')
    c.layout()


# Button(sw,SWT.PUSH).setText("toto")


#
# x = allWidgets(kind=StaticDiagramFigure)
# toolboxCanvas = x[0]
# diagramCanvas = x[1]

#x =allWidgets(kind="org.modelio.diagram.editor.statik.elements.staticdiagram.StaticDiagramFigure")
#diagramFigure=x[0]
#printWidgetTree(diagramFigure)
#y = diagramFigure.children[1]
#explore(y)






#--- model tree ---------------------------------------------------------------

# noinspection PyUnresolvedReferences
import org.eclipse.swt.widgets

def getModelTree():
    """
    Returns the eclipse SWT Tree displaying the model.
    :return: The tree view corresponding to the model in the modelio
    :rtype: org.eclipse.swt.widgets.Tree
    """
    modelCTab = getCTabItem('Model')
    tree = modelCTab.control.children[0].children[0]
    assert isinstance(tree, org.eclipse.swt.widgets.Tree)
    return tree


def getModelTreeSelection(typeFilter=None):
    """
    Returns the list of selected elements in the ModelTree. This may contains
    model elements but also other kinds of elements such as fragments.
    :return: The list of selected elements.
    :rtype: list
    """
    _ = []
    for item in getModelTree().selection:
        if typeFilter is None or isinstance(item.data, typeFilter):
            _.append(item.data)
    return _

# noinspection PyUnresolvedReferences
import org.eclipse.swt.events


class TreeSelectionListener(org.eclipse.swt.events.SelectionListener):
    def __init__(self, processFun):
        self.processFun = processFun

    def widgetSelected(self, selectionEvent):
        self.processFun(selectionEvent)

    def widgetDefaultSelected(self, selectionEvent):
        self.processFun(selectionEvent)


def SampleListener(e):
    print getModelTreeSelection()


# x = TreeSelectionListener(SampleListener())
# tree.addSelectionListener(x)



#----- image ------------------------------------------------------------------

def test():
    # adapted from http://stackoverflow.com/questions/4447455/how-to-show-up-an-image-with-swt-in-java
    # noinspection PyUnresolvedReferences
    from org.eclipse.swt.layout import GridData,GridLayout,FillLayout
    # noinspection PyUnresolvedReferences
    from org.eclipse.swt.graphics import Image
    # noinspection PyUnresolvedReferences
    from org.eclipse.swt.widgets import \
        Shell,Display,Label,Button,Listener,Text,Menu,MenuItem,FileDialog
    s = shell(options=SWT.SHELL_TRIM | SWT.DOUBLE_BUFFERED | SWT.RESIZE)
    img = Image(Display.getDefault(),'C:/DOWNLOADS/SCREENSHOTS/screenshot.002.jpg')
    class mylistener(Listener):
        def handleEvent(self, event):
           gc = event.gc
           gc.drawImage(img, 20, 20)
           gc.dispose()

    s.addListener(SWT.Paint, mylistener())
    s.open()
#
# does not work inside figure. Where should it be done
# ifig = ImageFigure(img)
# diags = allWidgets(kind="org.modelio.diagram.editor.statik.elements.staticdiagram.StaticDiagramFigure")
# diags[0].add(ifig)
# diags[0].repaint()








# noinspection PyUnresolvedReferences
from org.eclipse.swt.graphics import Color, Rectangle, Point, GC



def highlightWidget(widget, color=Color(Display.getDefault(), 255, 0, 0)):

    gc = GC(widget)
    gc.setLineWidth(4)
    gc.setForeground(color)
    size = widget.size
    gc.drawRectangle(Rectangle(0, 0, size.x, size.y))
    gc.dispose()



# ----------------------------------------------
# TO BE INTEGRATED - SEE DETAILS
# http://stackoverflow.com/questions/5842190/how-to-detect-ctrl-f-in-my-swt-application
# from org.eclipse.swt import SWT
# from org.eclipse.swt.widgets import Listener, Display
#
#
# class KeyDownListener(Listener):
#     def handleEvent(self, event):
#         # IT SEEMS THAT THE CODE IS NOT A CHARACTER BUT AN INTEGER
#         if event.stateMask & SWT.CTRL == SWT.CTRL and event.keyCode == ord('f'):
#             print "Key", event.keyCode, event.stateMask
#
#
# listener = KeyDownListener()
# display = Display.getDefault()
# display.addFilter(SWT.KeyDown, KeyDownListener())
# print SWT.CTRL


class ImageProvider(object):
    """ provide some images for given name (extension is added)
    """

    def __init__(self,resourcePath="",extension=".gif"):
        self.extension = extension
        if resourcePath != "":
            self.resourcePath = resourcePath
        else:
            self.resourcePath = os.path.join(os.path.dirname(__file__),'res')
        # imageMap contains a mapping   name -> image|None
        # this mapping is built on demand
        self.imageMap = {}

    def getImageFromName(self,name):
        if name not in self.imageMap:
            try:
                image = Image(Display.getCurrent(),
                              os.path.join(self.resourcePath,name + self.extension))
            except:
                image = None
            self.imageMap[name] = image
        return self.imageMap[name]


class FileDialogWindow(object):
    def __init__(self,extensions=(),path="",multiple=False):
        """ Select one or various files (if multiple is chosen)
            with some extensions parameters and a path.
            For instance FileDialogWindow(["*.html"],"c:\\temp",True)
        """
        parent = Display.getDefault().getActiveShell()
        self.multiple = multiple
        options = SWT.OPEN | SWT.MULTI if self.multiple else SWT.OPEN
        self.dialog = FileDialog(parent,options)
        self.dialog.setFilterExtensions(extensions)
        self.dialog.setFilterPath(path)
        self.result = self.dialog.open()

    def getFile(self):
        if self.multiple:
            return list(self.dialog.getFileNames())
        else:
            return self.result


class _Test_TextAreaWindowWithMenuBar(object):
    def __init__(self,text="",width=800,height=800):
        parent = Display.getDefault().getActiveShell()
        self.window = Shell(parent,SWT.CLOSE | SWT.RESIZE | SWT.MIN)
        self.window.setLayout(FillLayout())
        self.text_area = Text(self.window,SWT.BORDER | SWT.MULTI | SWT.V_SCROLL)
        self.text_area.setText(text)

        bar = Menu(self.window,SWT.BAR)
        self.window.setMenuBar(bar)
        editItem = MenuItem(bar,SWT.CASCADE)
        editItem.setText("Edit")
        submenu = Menu(self.window,SWT.DROP_DOWN)
        editItem.setMenu(submenu)
        item = MenuItem(submenu,SWT.PUSH)
        # item.addListener (SWT.Selection, new Listener () {
        #  @Override
        #  public void handleEvent (Event e) {
        #    self.textarea.selectAll();
        #  }
        # });
        item.setText("Select &All\tCtrl+A")
        # item.setAccelerator (SWT.MOD1 + "A")

        self.window.setSize(width,height)
        self.window.open()

    def setText(self,text):
        self.text_area.setText(text)

    def getText(self):
        return self.text_area.getText()


class _Test_ToolBarWindow(object):
    def __init__(self):
        parent = Display.getDefault().getActiveShell()
        self.window = Shell(parent)
        bar = ToolBar(self.window,SWT.BORDER)
        for i in range(0,7):
            item = ToolItem(bar,SWT.PUSH)
            item.setText("Item " + str(i))
        clientArea = self.window.getClientArea()
        bar.setLocation(clientArea.x,clientArea.y)
        bar.pack()
        self.window.open()


class TextAreaWindow(object):
    def __init__(self,text="",title="",width=800,height=800,headerLabel=""):
        self.initialText = text
        parent = Display.getDefault().getActiveShell()
        self.window = Shell(parent,SWT.CLOSE | SWT.RESIZE | SWT.MIN)
        # give minimum size, location and size
        # self.window.setMinimumSize(width, height)
        # parentBounds = parent.getBounds()
        # self.window.setLocation( \
        #  (parentBounds.width-width)/2+parentBounds.x, \
        #  (parentBounds.height-height)/2+parentBounds.y )
        # self.window.setSize(width, height)

        # layout
        gridLayout = GridLayout(2,False)
        self.window.setLayout(gridLayout)
        if len(title) > 0:
            self.window.setText(title)
        if len(headerLabel) > 0:
            self._createHeaderLabel(headerLabel)
        self._createContent()
        self._createButtons()
        # self._listenSelection()
        self.window.open()

    def _createHeaderLabel(self,headerLabel):
        data = GridData(SWT.FILL,SWT.TOP,True,False,2,1)
        # data = GridData(GridData.FILL_HORIZONTAL)
        data.verticalIndent = 5
        self.label = Label(self.window,SWT.WRAP)
        self.label.setLayoutData(data)
        self.label.setText(headerLabel)
        self.label.setLocation(10,40)

    def _createContent(self):
        data = GridData(SWT.FILL,SWT.FILL,True,True,2,1)
        # data.verticalIndent = 10;
        self.text_area = Text(self.window,SWT.BORDER | SWT.MULTI | SWT.V_SCROLL)
        self.text_area.setLayoutData(data)
        self.text_area.setText(self.initialText)

    def _createButtons(self):
        data = GridData(GridData.HORIZONTAL_ALIGN_END)
        data.widthHint = 50
        button1 = Button(self.window,SWT.FLAT)
        button1.setLayoutData(data)
        button1.setText("OK")
        button2 = Button(self.window,SWT.FLAT)
        button2.setLayoutData(data)
        button2.setText("KO")
        button3 = Button(self.window,SWT.FLAT)
        button3.setLayoutData(data)
        button3.setText("KO")

        class MyListener(Listener):
            def handleEvent(self, event):
                # FIXME:!
                if (event.widget == button1):
                    button1.getShell().close()

        button1.addListener(SWT.Selection,MyListener())
        self.okButton = button1
        #def _listenSelection(self):
        # thebrowser = self.browser
        # from org.modelio.api.modelio import Modelio
        # from org.modelio.api.app.navigation import INavigationListener
        # class SelectionListener(INavigationListener):
        #def navigateTo(self):
        #  thebrowser.setText("selection is "+str(target.getName()))
        #  pass
        # Modelio.getInstance().getNavigationService().addNavigationListener(SelectionListener())

    def setText(self,text):
        self.text_area.setText(text)


# see http://git.eclipse.org/c/platform/eclipse.platform.swt.git/tree/examples/org.eclipse.swt.snippets/src/org/eclipse/swt/snippets/Snippet128.java to improve this window with more feature
class HtmlWindow(object):
    def __init__(self,url=None,html=None,title="information",width=800,height=800,labelText=""):
        parent = Display.getDefault().getActiveShell()
        self.window = Shell(parent,SWT.CLOSE | SWT.RESIZE | SWT.MIN)
        # give minimum size, location and size
        self.window.setMinimumSize(width,height)
        parentBounds = parent.getBounds()
        self.window.setLocation(
            (parentBounds.width - width) / 2 + parentBounds.x,
            (parentBounds.height - height) / 2 + parentBounds.y)
        self.window.setSize(width,height)
        # layout
        gridLayout = GridLayout(1,1)
        self.window.setLayout(gridLayout)
        self.window.setText(title)
        self._createLabel(labelText)
        self._createBrowser(url=url,html=html)
        self._createOkButton()
        self._listenSelection()
        self.window.open()

    def _createLabel(self,labelText):
        data = GridData(GridData.FILL_HORIZONTAL)
        data.verticalIndent = 5
        self.label = Label(self.window,SWT.WRAP)
        self.label.setLayoutData(data)
        self.label.setText(labelText)
        self.label.setLocation(10,40)

    def _createBrowser(self,html=None,url=None):
        data = GridData(SWT.FILL,SWT.FILL,1,1)
        data.verticalIndent = 10
        self.browser = Browser(self.window,SWT.BORDER)
        self.browser.setLayoutData(data)
        if url is not None:
            self.setURL(url)
        else:
            if html is not None:
                self.setText(html)
            else:
                pass

    def _createOkButton(self):
        data = GridData(GridData.HORIZONTAL_ALIGN_END)
        data.widthHint = 50
        button = Button(self.window,SWT.FLAT)
        button.setLayoutData(data)
        button.setText("OK")

        class MyListener(Listener):
            def handleEvent(self,event):
                if (event.widget == button):
                    button.getShell().close()

        button.addListener(SWT.Selection,MyListener())
        self.okButton = button

    def _listenSelection(self):
        the_browser = self.browser
        # noinspection PyUnresolvedReferences
        from org.modelio.api.modelio import Modelio
        # noinspection PyUnresolvedReferences
        from org.modelio.api.app.navigation import INavigationListener

        class SelectionListener(INavigationListener):
            #def navigateTo(self):
            #  the_browser.setText("selection is "+str(target.getName()))
            pass

        Modelio.getInstance().getNavigationService().addNavigationListener(SelectionListener())

    def setText(self,html):
        self.browser.setText(
            "<html><header></header><body>" + html + "</body></html>")

    def setURL(self,url):
        if url is not None:
            self.browser.setUrl(url)
        else:
            self.setText('')

    def setLabel(self,text):
        self.label.setText(text)

# noinspection PyUnresolvedReferences
from org.eclipse.swt import *
# noinspection PyUnresolvedReferences
from org.eclipse.swt.layout import FillLayout
# noinspection PyUnresolvedReferences
from org.eclipse.swt.widgets import Tree,TreeItem


class TreeWindow(object):
    def __init__(self,rootDataObjects,getChildrenFun,isLeafFun,
                 getImageFun=None,getTextFun=None,title="Explorer",
                 getGrayedFun=None,getBackgroundFun=None,getForegroundFun=None,
                 onSelectionFun=None
    ):

        def _addRootDataObjects():
            # add the roots to the tree
            for rootDataObject in rootDataObjects:
                node = TreeItem(self.tree,0)
                _decorateTreeItem(node,rootDataObject)
                # add a dummy node if this is not a leaf
                if not isLeafFun(rootDataObject):
                    TreeItem(node,0)

        def _decorateTreeItem(node,dataObject):
            node.setData(dataObject)
            if getTextFun is not None:
                text = getTextFun(dataObject)
            else:
                text = unicode(dataObject)
            if text is not None:
                node.setText(text)
            if getImageFun is not None:
                image = getImageFun(dataObject)
                if image is not None:
                    node.setImage(image)
            if getGrayedFun is not None:
                grayed = getGrayedFun(dataObject)
                if grayed is not None:
                    node.setGrayed(grayed)
            if getBackgroundFun is not None:
                background = getBackgroundFun(dataObject)
                if background is not None:
                    node.setBackground(background)
            if getForegroundFun is not None:
                foreground = getForegroundFun(dataObject)
                if foreground is not None:
                    node.setForeground(foreground)

        class ThisTreeExpandListener(Listener):
            def handleEvent(self,event):
                try:
                    node = event.item
                    items = node.getItems()
                    # check if this subtree has already been expanded before
                    # if so there is nothing to do, otherwise remove dummy nodes
                    for item in items:
                        if item.getData() is not None:
                            return
                        else:
                            item.dispose()
                        # get the children and add them to the tree
                    for childDataObject in getChildrenFun(node.getData()):
                        item = TreeItem(node,0)
                        _decorateTreeItem(item,childDataObject)
                        if not isLeafFun(childDataObject):
                            # create a dummy node
                            TreeItem(item,0)
                except Exception as e:
                    traceback.print_exc()

        class ThisTreeSelectionListener(Listener):
            def handleEvent(self,event):
                node = event.item
                if onSelectionFun is not None:
                    onSelectionFun(node.getData())

        parentShell = Display.getDefault().getActiveShell()
        self.window = Shell(parentShell,SWT.CLOSE | SWT.RESIZE)
        self.window.setText(title)
        self.window.setLayout(FillLayout())
        self.tree = Tree(self.window,SWT.BORDER)
        self.tree.addListener(SWT.Expand,ThisTreeExpandListener())
        self.tree.addListener(SWT.Selection,ThisTreeSelectionListener())
        _addRootDataObjects()
        size = self.tree.computeSize(300,SWT.DEFAULT)
        width = max(300,size.x)
        height = max(300,size.y)
        self.window.setSize(self.window.computeSize(width,height))
        self.window.open()
