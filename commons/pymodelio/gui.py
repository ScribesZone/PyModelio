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

#----- graphical user interface ---------------------------------------------------------

from org.eclipse.swt import SWT
from org.eclipse.swt.widgets import Shell,Display,Label,Button,Listener,Text,Menu,MenuItem,FileDialog
from org.eclipse.swt.widgets import ToolBar,ToolItem
from org.eclipse.swt.browser import Browser
from org.eclipse.swt.layout import GridData,GridLayout


import os    
from org.eclipse.swt.graphics import Color, Image
from org.eclipse.swt.widgets import Display

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
        image = Image(Display.getCurrent(),os.path.join(self.resourcePath,name+self.extension))
      except:
        image = None
      self.imageMap[name] = image
    return self.imageMap[name]


    
class FileDialogWindow(object):
  def __init__(self, extensions=[],path="",multiple=False):
    """ Select one or various files (if multiple is choosen)
        with some extensions parameters and a path.
        For instance FileDialogWindow(["*.html"],"c:\\temp",True)
    """    
    parent = Display.getDefault().getActiveShell()
    self.multiple = multiple
    options = SWT.OPEN | SWT.MULTI if self.multiple else SWT.OPEN
    self.dialog = FileDialog(parent, options)
    self.dialog.setFilterExtensions(extensions)
    self.dialog.setFilterPath(path)
    self.result = self.dialog.open()
  def getFile(self):
    if self.multiple:
      return list(self.dialog.getFileNames())
    else:
      return self.result

class _Test_TextAreaWindowWithMenuBar(object):
  def __init__(self, text="",width=800,height=800):      
    parent = Display.getDefault().getActiveShell()
    self.window = Shell(parent, SWT.CLOSE | SWT.RESIZE| SWT.MIN)
    self.window.setLayout(FillLayout())
    self.textarea = Text(self.window, SWT.BORDER | SWT.MULTI | SWT.V_SCROLL)
    self.textarea.setText (text)
    
    bar = Menu(self.window, SWT.BAR)
    self.window.setMenuBar (bar)
    editItem = MenuItem (bar, SWT.CASCADE)
    editItem.setText ("Edit")
    submenu = Menu (self.window, SWT.DROP_DOWN)
    editItem.setMenu (submenu)
    item = MenuItem (submenu, SWT.PUSH)
    # item.addListener (SWT.Selection, new Listener () {
    #  @Override
    #  public void handleEvent (Event e) {
    #    self.textarea.selectAll();
    #  }
    # });
    item.setText ("Select &All\tCtrl+A")
    # item.setAccelerator (SWT.MOD1 + "A")

    self.window.setSize(width, height);
    self.window.open();
  def setText(self,text):
    self.textarea.setText(text)
  def getText(self):
    return self.textarea.getText()  
    
class _Test_ToolBarWindow(object):
  def __init__(self):
    parent = Display.getDefault().getActiveShell()
    self.window=Shell (parent)
    bar = ToolBar (self.window, SWT.BORDER)
    for i in range(0,7):
      item = ToolItem (bar, SWT.PUSH)
      item.setText ("Item " + str(i))
    clientArea = self.window.getClientArea ();
    bar.setLocation(clientArea.x, clientArea.y);
    bar.pack ();
    self.window.open ();
  
  
  
class TextAreaWindow(object):
  def __init__(self, text="",title="",width=800,height=800,headerlabel=""):  
    self.initialText = text
    parent = Display.getDefault().getActiveShell()
    self.window = Shell(parent, SWT.CLOSE | SWT.RESIZE | SWT.MIN)
    # give minimum size, location and size
    # self.window.setMinimumSize(width, height)
    # parentBounds = parent.getBounds()
    # self.window.setLocation( \
    #  (parentBounds.width-width)/2+parentBounds.x, \
    #  (parentBounds.height-height)/2+parentBounds.y )
    # self.window.setSize(width, height)
    
    # layout
    gridLayout = GridLayout(2, False)
    self.window.setLayout(gridLayout)
    if len(title)>0:
      self.window.setText(title)
    if len(headerlabel)>0:
      self._createHeaderLabel(headerlabel)
    self._createContent()
    self._createButtons()
    # self._listenSelection()
    self.window.open()
  def _createHeaderLabel(self,headerlabel):
    data = GridData(SWT.FILL, SWT.TOP, True, False, 2, 1)
    # data = GridData(GridData.FILL_HORIZONTAL)
    data.verticalIndent = 5;
    self.label = Label(self.window, SWT.WRAP)
    self.label.setLayoutData(data)
    self.label.setText(headerlabel)
    self.label.setLocation(10, 40)
  def _createContent(self):
    data = GridData(SWT.FILL,SWT.FILL,True, True,2,1)
    # data.verticalIndent = 10;
    self.textarea = Text(self.window, SWT.BORDER | SWT.MULTI | SWT.V_SCROLL)
    self.textarea.setLayoutData(data)
    self.textarea.setText(self.initialText)
  def _createButtons(self):    
    data = GridData(GridData.HORIZONTAL_ALIGN_END)
    data.widthHint = 50
    button1 = Button(self.window, SWT.FLAT)    
    button1.setLayoutData(data)    
    button1.setText("OK")
    button2 = Button(self.window, SWT.FLAT)    
    button2.setLayoutData(data)    
    button2.setText("KO")
    button3 = Button(self.window, SWT.FLAT)    
    button3.setLayoutData(data)    
    button3.setText("KO")
         
    class MyListener(Listener):
       def handleEvent(self, event):        
        if (event.widget == button):
           button.getShell().close()
    button1.addListener(SWT.Selection, MyListener())
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
    self.textarea.setText(text)

























# see http://git.eclipse.org/c/platform/eclipse.platform.swt.git/tree/examples/org.eclipse.swt.snippets/src/org/eclipse/swt/snippets/Snippet128.java to improve this window with more feature
class HtmlWindow(object):
  def __init__(self, url=None, html=None,title="information",width=800,height=800,labeltext=""):  
    parent = Display.getDefault().getActiveShell()
    self.window = Shell(parent, SWT.CLOSE | SWT.RESIZE | SWT.MIN)
    # give minimum size, location and size
    self.window.setMinimumSize(width, height)
    parentBounds = parent.getBounds()
    self.window.setLocation( \
      (parentBounds.width-width)/2+parentBounds.x, \
      (parentBounds.height-height)/2+parentBounds.y )
    self.window.setSize(width, height)
    # layout
    gridLayout = GridLayout(1, 1)
    self.window.setLayout(gridLayout)
    self.window.setText(title)
    self._createLabel(labeltext)
    self._createBrowser(url=url,html=html)
    self._createOkButton()
    self._listenSelection()
    self.window.open()
  def _createLabel(self,labeltext):
    data = GridData(GridData.FILL_HORIZONTAL)
    data.verticalIndent = 5;
    self.label = Label(self.window, SWT.WRAP)
    self.label.setLayoutData(data)
    self.label.setText(labeltext)
    self.label.setLocation(10, 40)
  def _createBrowser(self,html=None,url=None):
    data = GridData(SWT.FILL,SWT.FILL,1,1)
    data.verticalIndent = 10;
    self.browser = Browser(self.window, SWT.BORDER)
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
    button = Button(self.window, SWT.FLAT)    
    button.setLayoutData(data)    
    button.setText("OK")        
    class MyListener(Listener):
       def handleEvent(self, event):        
        if (event.widget == button):
           button.getShell().close()
    button.addListener(SWT.Selection, MyListener())
    self.okButton = button
  def _listenSelection(self):
    thebrowser = self.browser
    from org.modelio.api.modelio import Modelio
    from org.modelio.api.app.navigation import INavigationListener
    class SelectionListener(INavigationListener):
      #def navigateTo(self):
      #  thebrowser.setText("selection is "+str(target.getName()))
      pass
    Modelio.getInstance().getNavigationService().addNavigationListener(SelectionListener())
  def setText(self,html):  
    self.browser.setText( \
      "<html><header></header><body>" + html + "</body></html>")
  def setURL(self,url):
    self.browser.setUrl(url)
  def setLabel(self,text):
    self.label.setText(text)
  

  
from org.eclipse.swt import *
from org.eclipse.swt.layout import FillLayout
#from org.eclipse.swt.graphics import *
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
        node = TreeItem(self.tree, 0)
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
          # print "not none"
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
      def handleEvent(self, event):         
        node = event.item
        # print "expanding node "+str(node.getData()),
        items = node.getItems()
        # print ": ",len(items),"children"
        # check if this subtree has already been expanded before
        # if so there is nothing to do, otherwise remove dummy nodes
        for item in items:
          # print "  object",item.getData(),type(item.getData()),
          if item.getData() is not None:
            # print "already visited. Stop"
            return
          else:
            # print "remove this node"
            item.dispose()
        # get the children and add them to the tree
        for childDataObject in getChildrenFun(node.getData()):
          item = TreeItem(node,0)
          _decorateTreeItem(item,childDataObject)
          if not isLeafFun(childDataObject):
            # create a dummy node 
            TreeItem(item, 0)
            
    class ThisTreeSelectionListener(Listener):
      def handleEvent(self, event):
        node = event.item
        # print "item selected",node,type(node)
        # print "details",event.detail
        if onSelectionFun is not None:
          onSelectionFun(node.getData())        
        
    parentShell = Display.getDefault().getActiveShell()
    self.window = Shell(parentShell, SWT.CLOSE | SWT.RESIZE)
    self.window.setText(title)
    self.window.setLayout(FillLayout())
    self.tree = Tree(self.window, SWT.BORDER)
    self.tree.addListener(SWT.Expand, ThisTreeExpandListener())
    self.tree.addListener(SWT.Selection,ThisTreeSelectionListener())
    _addRootDataObjects()
    size = self.tree.computeSize(300, SWT.DEFAULT)
    width = max (300, size.x)
    height = max (300, size.y)
    self.window.setSize (self.window.computeSize(width, height))
    self.window.open ()
    
        

#----- web  ---------------------------------------------------------


from encodings import iso8859_1
import urllib2
  
def getWebPage(url):
  """ read the content of the given url and throws an exception in case of error
  """
  return urllib2.urlopen(url).read()
  
  

  
print "module gui loaded from",__file__
