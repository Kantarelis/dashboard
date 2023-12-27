import os
from multiprocessing import Lock

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
        """A demo dashboard application. This mini project is implemented as a show-case-scenario. It is a fully
        functional, yet minimal, application for automatic stock tracking. The user can easily select his/hers
        stocks-to-watch from a pool of stocks (for the sake of this demo these stocks are only from US). The user can
        watch his/hers stocks, which are listing as interactive buttons on the left side of the dashboard, on the main
        area of the application with interactive line and candle plots. There is also an analysis button with which one
        can see, which stock needs to be sold based to an algorithm. This decision-making algorithm that runs in the
        background is a simple application of the well known Black-Scholes equation. If a stock has no data, then the
        verdict is it be sold, due to the fact that, with no data the stock cannot be trusted.

        Args:
            app_title (str, optional): The name of the application. Defaults to "Dashboard".
        """
        self.app_title = app_title
        self.app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
        self.root_path = os.getcwd()
        self.lock = Lock()
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
