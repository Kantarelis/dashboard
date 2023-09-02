import os
from multiprocessing import Lock

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

from dashboard.callbacks.modals.add_stocks import add_stocks_modal, body_of_add_stocks_modal
from dashboard.callbacks.modals.remove_stocks import remove_stocks_modal
from dashboard.callbacks.objects.stocks_box import stocks_box
from dashboard.callbacks.utilities.init_page_clock import init_page_clock
from dashboard.callbacks.utilities.local_data_paths_constructor import local_data_paths_constructor
from dashboard.database.functions.generic import create_connection
from dashboard.interfaces.dashboard_main import dashboard_main
from dashboard.interfaces.init_page import init_page
from dashboard.pyqt5_browser.browser import browser_app
from dashboard.settings import DATABASE_PATH


class Dashboard:
    def __init__(self, app_title="Dashboard"):
        self.app_title = app_title
        self.app: dash.Dash = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
        self.root_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
        self.lock = Lock()
        create_connection(DATABASE_PATH)

    def run(self):
        # ===================================== Create necessary paths =================================================
        local_data_paths_constructor(self.root_path)

        # ================================ Define the layout of the app ================================================
        self.app.layout = html.Div(
            [dcc.Location(id="url", refresh=False), html.Div(id="page-content")],
        )

        # =============================== Define the title of the application ==========================================
        self.app.title = self.app_title

        # ==============================================================================================================
        # ==================================== Clearing Paths Callbacks ================================================
        # ==============================================================================================================
        # clearing_paths_callbacks(app, root_path)

        # ==============================================================================================================
        # ==================================== Pages Navigation Callback ===============================================
        # ==============================================================================================================
        @self.app.callback(Output("page-content", "children"), [Input("url", "pathname")])
        def display_page(pathname: str):
            if pathname == "/":
                # ======================================= Clear Auto Generated Data ====================================
                # ======================================================================================================
                return init_page
            elif pathname == "/dashboard_main":
                return dashboard_main
            else:
                print("Pathname Error")

        # ==============================================================================================================
        # ========================================= Utilities Callbacks ================================================
        # ==============================================================================================================
        init_page_clock(self.app)

        # ========================================= Object Callbacks ===================================================
        # ==============================================================================================================
        # ==============================================================================================================
        stocks_box(self.app, self.root_path, self.lock)

        # ========================================== Modal Callbacks ===================================================
        # ==============================================================================================================
        # ==============================================================================================================
        add_stocks_modal(self.app)
        body_of_add_stocks_modal(self.app)
        remove_stocks_modal(self.app)

        # ==============================================================================================================
        # =============================== User Inputs Dictionaries Callbacks ===========================================
        # ==============================================================================================================
        # user_settings_callbacks(app, root_path)

        # ==============================================================================================================
        # ======================================== Server Initiation ===================================================
        # ==============================================================================================================
        browser_app(self.app, argv=["", "--no-sandbox"], window_title=self.app_title)
