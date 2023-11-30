import os
from multiprocessing import Lock
from multiprocessing.synchronize import Lock as LockType

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from dashboard.callbacks.figures.main_plot import stock_candles_plot
from dashboard.callbacks.modals.stocks_portfolio import (
    add_stocks_to_database,
    left_body_of_stocks_portfolio_modal,
    remove_stocks_from_database,
    right_body_of_stocks_portfolio_modal,
    stocks_portfolio_modal,
)
from dashboard.callbacks.objects.stocks_box import stocks_box
from dashboard.callbacks.utilities.init_page_clock import init_page_clock
from dashboard.callbacks.utilities.local_data_paths_constructor import local_data_paths_constructor
from dashboard.callbacks.utilities.page_navigation import navigation_callback
from dashboard.callbacks.utilities.run_stock_analysis import analyse_stocks
from dashboard.database.functions.generic import configure_environment, create_connection
from dashboard.engine.stocks_data_feed import StocksDataFeed
from dashboard.pyqt5_browser.browser import BrowserApp
from dashboard.settings import DATABASE_PATH


class Dashboard:
    def __init__(self, app_title: str = "Dashboard"):
        self.app_title = app_title
        self.app: dash.Dash = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
        self.root_path: str = os.getcwd()
        self.lock: LockType = Lock()
        configure_environment()
        create_connection(DATABASE_PATH)

    def run(self):
        # ===================================== Start Main Engine ======================================================
        stocks_data_feed_engine = StocksDataFeed(self.lock)
        stocks_data_feed_engine.start()
        datafeed_pid = stocks_data_feed_engine.pid

        # ===================================== Create necessary paths =================================================
        local_data_paths_constructor(self.root_path)

        # ================================ Define the layout of the app ================================================
        self.app.layout = html.Div(
            [dcc.Location(id="url", refresh=False), html.Div(id="page-content")],
        )

        # =============================== Define the title of the application ==========================================
        self.app.title = self.app_title

        # ==============================================================================================================
        # ==================================== Pages Navigation Callback ===============================================
        # ==============================================================================================================
        navigation_callback(self.app)

        # ==============================================================================================================
        # ========================================= Utilities Callbacks ================================================
        # ==============================================================================================================
        init_page_clock(self.app)
        analyse_stocks(self.app, self.root_path, self.lock)

        # ========================================= Object Callbacks ===================================================
        # ==============================================================================================================
        # ==============================================================================================================
        stocks_box(self.app, self.root_path, self.lock)

        # ========================================== Modal Callbacks ===================================================
        # ==============================================================================================================
        # ==============================================================================================================
        stocks_portfolio_modal(self.app)
        left_body_of_stocks_portfolio_modal(self.app, self.lock)
        right_body_of_stocks_portfolio_modal(self.app)
        add_stocks_to_database(self.app, self.lock)
        remove_stocks_from_database(self.app, self.lock)
        stock_candles_plot(self.app, self.root_path, self.lock)

        # ==============================================================================================================
        # ======================================== Server Initiation ===================================================
        # ==============================================================================================================
        browser = BrowserApp(datafeed_pid, argv=["", "--no-sandbox"], window_title=self.app_title)
        browser.run(self.app)
