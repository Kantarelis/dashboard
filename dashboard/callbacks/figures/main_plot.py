import re
from multiprocessing.synchronize import Lock as LockType
from typing import Any, Tuple, Union

import plotly.graph_objs as go
from dash import ALL, Dash, Input, Output, callback_context, no_update

from dashboard.callbacks.settings import STOCK_BUTTON_REGEX
from dashboard.figures.stock_candles import stock_candles_figure


def stock_candles_plot(app: Dash, root_path: str, lock: LockType):
    @app.callback(
        Output("stock_candle_plot", "figure"),
        Output("last_stock_selected", "value"),
        Input({"type": "stock_button", "index": ALL}, "n_clicks"),
        Input("refresh_figure", "n_intervals"),
        Input("last_stock_selected", "value"),
        prevent_initial_call=True,
    )
    def stock_candles_plot_function(
        stocks_n_clicks: list, n_intervals: int, previous_stock: str
    ) -> Tuple[Union[go.Figure, Any], Union[str, Any]]:
        """Callback for Updating Main Graph.

        Args:
            stocks_n_clicks (list): A list containing integers; the numbers of clicks performed of every stock symbol
                                    button.
            n_intervals (int): An integer counter measuring how many dt - intervals of time passed. The dt is defined in
                               /dashboard.settings.py and named as 'MAIN_GRAPH_REFRESH_RATE' constant.
            previous_stock (str): This is the last stock selected by the user or with automatic selection (when you
                                  start the application for the first time, it automatically selects the first saved
                                  stock, if any in local database.)

        Returns:
            figure: Union[go.Figure, Any]: Returns either an updated figure or a dash command to not update the figure.
            previous_stock: Union[str, Any]: Returns either None, in case no saved stock exists in local
                                  database, str to save last used stock in a dcc.Store object, or a dash command to not
                                  update the last used stock.

        """
        # If regex find a match, save stock_symbol. If stock_symbol is different from last used stock, update figure.
        if bool(re.match(STOCK_BUTTON_REGEX, f"{callback_context.triggered_id}")):
            stock_symbol = re.findall(STOCK_BUTTON_REGEX, f"{callback_context.triggered_id}")[0]
            if stock_symbol != previous_stock:
                return stock_candles_figure(root_path, lock, stock_symbol), stock_symbol

        # A list of ALL saved stocks.
        saved_stocks = [
            callback_context.inputs_list[0][n_click]["id"]["index"]
            for n_click in range(len(callback_context.inputs_list[0]))
        ]

        # If there is at least one saved stock in local database:
        if saved_stocks:
            # If previous stock exist is deleted from the local database -> update figure and saved stock with the
            # first saved stock from database.
            if previous_stock not in saved_stocks:
                return stock_candles_figure(root_path, lock, saved_stocks[0]), saved_stocks[0]
        return no_update, no_update
