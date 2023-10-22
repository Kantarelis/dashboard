import logging

from dash import Dash, Input, Output, html

from dashboard.interfaces.dashboard_main import dashboard_main
from dashboard.interfaces.init_page import init_page
from dashboard.settings import INIT_PAGE_PATH, MAIN_PAGE_PATH


def navigation_callback(app: Dash):
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname"),
    )
    def display_page(pathname: str) -> html.Div:
        logging.debug(f"The pathname is changes into: {pathname}.")
        if pathname == INIT_PAGE_PATH:
            # ======================================= Clear Auto Generated Data ====================================
            # ======================================================================================================
            logging.debug(f"The pathname '{pathname}' is matched with a server-page.")
            return init_page
        elif pathname == MAIN_PAGE_PATH:
            logging.debug(f"The pathname '{pathname}' is matched with a server-page.")
            return dashboard_main
        else:
            logging.error(f"Pathname Error: This path {pathname} does not correspond to any know application path.")
            raise Exception(f"Pathname Error: This path {pathname} does not correspond to any know application path.")
