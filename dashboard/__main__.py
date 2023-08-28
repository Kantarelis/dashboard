import os
from multiprocessing import Lock

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

from dashboard.callbacks.modals.add_stocks import add_stocks_modal
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
    def __init__(self):
        pass

    def run(self):
        # ================================== Define relative root position =============================================
        root_path: str = os.getcwd()

        # ================================== Create db file if not exists ==============================================
        create_connection(DATABASE_PATH)

        # ============================== Define a global lock for io operations ========================================
        lock = Lock()

        # ===================================== Create necessary paths =================================================
        local_data_paths_constructor(root_path)

        # ========================================= Define the app =====================================================
        app: dash.Dash = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

        # ================================ Define the layout of the app ================================================
        app.layout = html.Div(
            [dcc.Location(id="url", refresh=False), html.Div(id="page-content")],
        )

        # =============================== Define the title of the application ==========================================
        app.title = "Dashboard"

        # ==============================================================================================================
        # ==================================== Clearing Paths Callbacks ================================================
        # ==============================================================================================================
        # clearing_paths_callbacks(app, root_path)

        # ==============================================================================================================
        # ==================================== Pages Navigation Callback ===============================================
        # ==============================================================================================================
        @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
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
        init_page_clock(app)

        # ========================================= Object Callbacks ===================================================
        # ==============================================================================================================
        # ==============================================================================================================
        stocks_box(app, root_path, lock)

        # ========================================== Modal Callbacks ===================================================
        # ==============================================================================================================
        # ==============================================================================================================
        add_stocks_modal(app)
        remove_stocks_modal(app)

        # ==============================================================================================================
        # =============================== User Inputs Dictionaries Callbacks ===========================================
        # ==============================================================================================================
        # user_settings_callbacks(app, root_path)

        # ==============================================================================================================
        # ======================================== Server Initiation ===================================================
        # ==============================================================================================================
        browser_app(app, argv=["", "--no-sandbox"])
