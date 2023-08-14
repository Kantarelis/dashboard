import sys
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from typing import Optional
import socket
from flask import Flask


LOCAL_HOST: str = "localhost"
SERVER_PORT: int = 0
DEFAULT_PORT: int = 8050
DEFAULT_WIDTH: int = 1920
DEFAULT_HEIGHT: int = 1080
DEFAULT_MINIMUM_HEIGHT: int = 880
DEFAULT_MINIMUM_WIDTH: int = 1200


class ApplicationThread(QtCore.QThread):
    """
    ApplicationThread of QtCore.QThread.
    """

    def __init__(self, application: Flask, port: int = DEFAULT_PORT):
        super(ApplicationThread, self).__init__()
        self.application: Flask = application
        self.port: int = port

    def __del__(self):
        self.wait()

    # Rewrite run method
    def run(self):
        self.application.run(port=self.port, host=LOCAL_HOST, threaded=True)


class WebPage(QtWebEngineWidgets.QWebEnginePage):
    """
    WebPage.
    """

    def __init__(self, root_url: str):
        super(WebPage, self).__init__()
        self.root_url: str = root_url

    def home(self):
        self.load(QtCore.QUrl(self.root_url))


# Exit handler
def _exit_handler(server_thread: ApplicationThread):
    server_thread.terminate


# Download Requests
def _on_downloadRequested(file):
    suggested_file = "plot.png"
    path, _ = QtWidgets.QFileDialog.getSaveFileName(None, None, suggested_file)
    if path:
        file.setPath(path)
        file.accept()


def browser_app(
    application: Flask,
    port: int = SERVER_PORT,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    min_width: int = DEFAULT_MINIMUM_WIDTH,
    min_height: int = DEFAULT_MINIMUM_HEIGHT,
    window_title: str = "Dashboard D&D",
    argv: Optional[list] = None,
):
    """
    Init Dashboard GUI.
    """
    if argv is None:
        argv = sys.argv

    # if port set to 0 grab dynamically a random free port
    if port == 0:
        sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((LOCAL_HOST, 0))
        port = sock.getsockname()[1]
        sock.close()

    # Application Level
    browser: QtWidgets.QApplication = QtWidgets.QApplication(argv)
    server_thread: ApplicationThread = ApplicationThread(application, port)
    server_thread.start()
    browser.aboutToQuit.connect(_exit_handler)

    # Main Window Level
    window: QtWidgets.QMainWindow = QtWidgets.QMainWindow()
    window.resize(width, height)
    window.setMinimumHeight(min_height)
    window.setMinimumWidth(min_width)
    window.setWindowTitle(window_title)
    # window.setWindowIcon(QtGui.QIcon(icon))

    # WebView Level
    webView: QtWebEngineWidgets.QWebEngineView = QtWebEngineWidgets.QWebEngineView(
        window
    )
    window.setCentralWidget(webView)

    # WebPage Level
    page: WebPage = WebPage(f"http://{LOCAL_HOST}:{port}")
    page.home()
    webView.setPage(page)

    # --------- ToolBar ----------
    # creating QToolBar for navigation
    navtb: QtWidgets.QToolBar = QtWidgets.QToolBar()

    # adding this tool bar tot he main window
    window.addToolBar(QtCore.Qt.BottomToolBarArea, navtb)

    # Reload action
    reload_btn: QtWidgets.QAction = QtWidgets.QAction("Unstuck", window)
    reload_btn.setStatusTip("Reload page")

    # adding action to the reload button
    # making browser to reload
    reload_btn.triggered.connect(webView.reload)
    navtb.addAction(reload_btn)

    navtb.setStyleSheet(
        "background-color:rgb(70, 70, 70); font: bold 14px; color:white"
    )

    # adding a separator in the tool bar
    navtb.addSeparator()

    webView.page().profile().downloadRequested.connect(_on_downloadRequested)

    window.showMaximized()

    return browser.exec_()
