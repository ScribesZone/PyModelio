# coding=utf-8




# noinspection PyUnresolvedReferences
from org.eclipse.swt.browser import Browser

class CustomFunctionData(object):
    def __init__(self, browser):
        self.browser = browser

# noinspection PyUnresolvedReferences
from org.eclipse.swt import SWT
# noinspection PyUnresolvedReferences
from org.eclipse.swt.browser import Browser, ProgressEvent, ProgressListener
# noinspection PyUnresolvedReferences
from org.eclipse.swt.widgets import Composite
# noinspection PyUnresolvedReferences
from org.eclipse.ui.part import ViewPart

class BrowserView(ViewPart):
    ID = "de.vogella.javascript.simple.view"

    def createPartControl(self, parent):
        b = Browser(parent, SWT.NONE)
        b.setUrl("http://www.vogella.de")
        class MyProgressListener(ProgressListener):
            def completed(self, event):
                print "Page loaded"
                # try {
                #        Thread.sleep(2000);
                #    } catch (InterruptedException e) {
                #        e.printStackTrace();
                #    }
                #  // Execute JavaScript in the browser
                b.execute("alert(\"JavaScript, called from Java\");");

            def changed(self, event):
                pass
        b.addProgressListener(MyProgressListener())

    # Passing the focus request to the viewer's control.
    def setFocus(self):
        pass


# noinspection PyUnresolvedReferences
from java.io import File
# noinspection PyUnresolvedReferences
from org.eclipse.swt import SWT
# noinspection PyUnresolvedReferences
from org.eclipse.swt.browser import Browser, BrowserFunction
# noinspection PyUnresolvedReferences
from org.eclipse.swt.custom import SashForm
# noinspection PyUnresolvedReferences
from org.eclipse.swt.events import ControlEvent, ControlListener,\
    SelectionAdapter, SelectionEvent
# noinspection PyUnresolvedReferences
from org.eclipse.swt.layout import GridData, GridLayout
# noinspection PyUnresolvedReferences
from org.eclipse.swt.widgets import Button, Composite, List
# noinspection PyUnresolvedReferences
from org.eclipse.ui.part import ViewPart

class MapView(ViewPart):

    ID = "de.vogella.javascript.maps.view"
    locations = None # org.eclipse.swt.widgets.List



    def createPartControl(self, parent):
        sash = SashForm(parent, SWT.HORIZONTAL)

        local_file = File("C:/temp/demofile/map.html");
        browser =  Browser(parent, SWT.NONE)

        class ThisControlListener(ControlListener):
            def controlResized(self, e):
                # Use Javascript to set the browser width and height
                browser.execute(
                    "document.getElementById('map_canvas').style.width=%i;"
                    % (browser.getSize().x - 20))

                browser.execute(
                    "document.getElementById('map_canvas').style.height=%i;"
                    % (browser.getSize().y - 20))

            def controlMoved(self, e):
                pass

        browser.addControlListener(ThisControlListener())

        # Called by JavaScript
        class __CustomFunction(BrowserFunction):
            def __init__(self, browser, name):
                BrowserFunction.__init__(self, browser, name)
                self.data = CustomFunctionData(None)
                self.data.browser(browser)

            def function(self, arguments):
                lat = arguments[0]
                lng = arguments[1]
                MapView.locations.add("%s : %s" % (lat, lng))
                self.data.browser.execute(
                    "document.getElementById('map_canvas').style.width=%i;"
                    % (self.data.browser.getSize().x - 20))
                self.data.browser.execute(
                    "document.getElementById('map_canvas').style.height=%i;"
                    % (self.data.browser.getSize().y - 20))
                return None
        __CustomFunction(browser, "theJavaFunction")

        c = Composite(sash, SWT.BORDER)
        c.setLayout(GridLayout(2, True))


        where_button = Button(c, SWT.PUSH)
        where_button.setText("Where Am I ?")
        class __Where_SelectionAdapter(SelectionAdapter):
            def widgetSelected(self, e):
                lat = browser.evaluate("return map.getCenter().lat();")
                lng = browser.evaluate("return map.getCenter().lng();")
                MapView.locations.add("%s : %s" % (lat,lng))
        where_button.addSelectionListener(__Where_SelectionAdapter())

        add_button = Button(c, SWT.PUSH)
        add_button.setText("Add Marker")
        class __Add_SelectionAdapter(SelectionAdapter):
            def widgetSelected(self, e):
                browser.evaluate('createMarker')
        add_button.addSelectionListener(__Add_SelectionAdapter())

        locations = List(c, SWT.BORDER | SWT.V_SCROLL | SWT.H_SCROLL)
        grid_data = GridData(SWT.FILL, SWT.FILL, True, True)
        grid_data.horizontalSpan = 2
        locations.setLayoutData(grid_data)

        browser.setUrl(local_file.toURI().toString())
        # sash.setWeights(new int[] {4,1});


    # Passing the focus request to the viewer's control
    def setFocus(self):
        pass





