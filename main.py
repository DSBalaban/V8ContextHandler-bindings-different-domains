# Tutorial example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v57.0+

from cefpython3 import cefpython as cef
import base64
import platform
import sys
import threading
import time

def main():
    global browser
    check_versions()
    sys.excepthook = cef.ExceptHook
    settings = {
        'log_file': 'cefpython3.log'
    }

    switches = {}

    cef.Initialize(settings=settings, switches=switches)
    browser = cef.CreateBrowserSync(url="about:blank", window_title="Tutorial")
    set_client_handlers(browser)
    browser.LoadUrl("http://localhost:8080/test/index.html")
    browser.ShowDevTools()

    # Wait 5 seconds, then change domains
    r = threading.Timer(5.0, another_app)
    r.start()

    cef.MessageLoop()
    cef.Shutdown()

def another_app():
    global browser
    browser.LoadUrl("http://localhost:8081/test/index.html")

def check_versions():
    ver = cef.GetVersion()
    print("[tutorial.py] CEF Python {ver}".format(ver=ver["version"]))
    print("[tutorial.py] Chromium {ver}".format(ver=ver["chrome_version"]))
    print("[tutorial.py] CEF {ver}".format(ver=ver["cef_version"]))
    print("[tutorial.py] Python {ver} {arch}".format(
           ver=platform.python_version(),
           arch=platform.architecture()[0]))
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"


def set_client_handlers(browser):
    v8ContextHandler = CefV8ContextHandler(lambda: set_javascript_bindings(browser))
    browser.clientCallbacks["OnContextCreated"] = v8ContextHandler.OnContextCreated


def set_javascript_bindings(browser):
    external = External(browser)
    bindings = cef.JavascriptBindings(bindToFrames=False, bindToPopups=False)
    bindings.SetProperty("python_property", "This property was set in Python")
    bindings.SetProperty("cefpython_version", cef.GetVersion())
    bindings.SetObject("_external", external)
    browser.SetJavascriptBindings(bindings)


class External(object):
    def __init__(self, browser):
        self.browser = browser

    def print_goodness(self):
        print "Goodness!"


class CefV8ContextHandler(object):
    def __init__(self, bind_api):
        self.bind_api = bind_api

    def OnContextCreated(self, browser, frame):
        print "V8 Context created"
        self.bind_api()


if __name__ == '__main__':
    main()
