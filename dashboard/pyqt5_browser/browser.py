import socket
import sys
from typing import List, Optional

from dash import Dash
from PyQt5 import QtCore, QtWebEngineWidgets, QtWidgets

from dashboard.engine.functions.process_functions import terminate_process
from dashboard.pyqt5_browser.settings import (
    DEFAULT_HEIGHT,
    DEFAULT_MINIMUM_HEIGHT,
    DEFAULT_MINIMUM_WIDTH,
    DEFAULT_PORT,
    DEFAULT_WIDTH,
    LOCAL_HOST,
    SERVER_PORT,
)


class ApplicationThread(QtCore.QThread):
    """ApplicationThread of QtCore.QThread."""

    def __init__(self, application: Dash, port: int = DEFAULT_PORT):
        super(ApplicationThread, self).__init__()
        self.application: Dash = application
        self.port: int = port

    def __del__(self):
        self.wait()

    # Rewrite run method
    def run(self):
        self.application.run(port=f"{self.port}", host=LOCAL_HOST, threaded=True)


class WebPage(QtWebEngineWidgets.QWebEnginePage):
    """WebPage."""

    def __init__(self, root_url: str):
        super(WebPage, self).__init__()
        self.root_url: str = root_url

    def home(self):
        self.load(QtCore.QUrl(self.root_url))


class BrowserApp:
    """The main browser app."""

    server_thread: ApplicationThread

    def __init__(
        self,
        process_pid: Optional[int],
        port: int = SERVER_PORT,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        min_width: int = DEFAULT_MINIMUM_WIDTH,
        min_height: int = DEFAULT_MINIMUM_HEIGHT,
        window_title: str = "Dashboard D&D",
        argv: Optional[List[str]] = None,
    ):
        self.process_pid = process_pid
        self.port = port
        self.width = width
        self.height = height
        self.min_width = min_width
        self.min_height = min_height
        self.window_title = window_title
        self.argv = argv

    def _exit_handler(self):
        terminate_process(self.process_pid)
        self.server_thread.terminate

    def run(self, application: Dash):
        """
        Init Dashboard GUI.
        """
        if self.argv is None:
            self.argv = sys.argv

        # if port set to 0 grab dynamically a random free port
        if self.port == 0:
            sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((LOCAL_HOST, 0))
            self.port = sock.getsockname()[1]
            sock.close()

        # Application Level
        browser: QtWidgets.QApplication = QtWidgets.QApplication(self.argv)
        self.server_thread = ApplicationThread(application, self.port)
        self.server_thread.start()

        browser.aboutToQuit.connect(self._exit_handler)

        # Main Window Level
        window: QtWidgets.QMainWindow = QtWidgets.QMainWindow()
        window.resize(self.width, self.height)
        window.setMinimumHeight(self.min_height)
        window.setMinimumWidth(self.min_width)
        window.setWindowTitle(self.window_title)

        # WebView Level
        webView: QtWebEngineWidgets.QWebEngineView = QtWebEngineWidgets.QWebEngineView(window)
        window.setCentralWidget(webView)

        # WebPage Level
        page: WebPage = WebPage(f"http://{LOCAL_HOST}:{self.port}")
        page.home()
        webView.setPage(page)

        # --------- ToolBar ----------
        # creating QToolBar for navigation
        navtb: QtWidgets.QToolBar = QtWidgets.QToolBar()

        # adding this tool bar tot he main window
        window.addToolBar(QtCore.Qt.ToolBarArea.BottomToolBarArea, navtb)

        # Reload action
        reload_btn: QtWidgets.QAction = QtWidgets.QAction("Unstuck", window)
        reload_btn.setStatusTip("Reload page")

        # adding action to the reload button
        # making browser to reload
        reload_btn.triggered.connect(webView.reload)
        navtb.addAction(reload_btn)

        navtb.setStyleSheet("background-color:rgb(70, 70, 70); font: bold 14px; color:white")

        # adding a separator in the tool bar
        navtb.addSeparator()

        window.showMaximized()

        return browser.exec_()
