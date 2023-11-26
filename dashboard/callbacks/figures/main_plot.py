import re
from multiprocessing.synchronize import Lock as LockType
from typing import Literal, Optional, Tuple, Type, Union

import plotly.graph_objs as go
from dash import ALL, Dash, Input, Output, callback_context, no_update

# from dashboard.callbacks.figures.functions import define_mode_and_previous_mode
from dashboard.callbacks.settings import STOCK_BUTTON_REGEX
from dashboard.figures.stock_candles import stock_candles_figure


def stock_candles_plot(app: Dash, root_path: str, lock: LockType):
    @app.callback(
        Output("stock_candle_plot", "figure"),
        Output("last_stock_selected", "value"),
        Output("last_mode_selected", "value"),
        Input({"type": "stock_button", "index": ALL}, "n_clicks"),
        Input("refresh_figure", "n_intervals"),
        Input("last_stock_selected", "value"),
        Input("all_mode", "n_clicks"),
        Input("candlesticks_mode", "n_clicks"),
        Input("close_line_mode", "n_clicks"),
        Input("last_mode_selected", "value"),
        prevent_initial_call=True,
    )
    def stock_candles_plot_function(
        stocks_n_clicks: list,
        n_intervals: Optional[int],
        previous_stock: str,
        all_n_clicks: int,
        candlesticks_n_clicks: int,
        close_line_n_clicks: int,
        previous_mode: Optional[Literal["all", "candlesticks", "close_line"]],
    ) -> Tuple[Union[go.Figure, Type], Union[str, Type], Optional[Literal["all", "candlesticks", "close_line"]]]:
        """Callback for Updating Main Graph.

        Args:
            stocks_n_clicks (list): A list containing integers; the numbers of clicks performed of every stock symbol
                                    button.
            n_intervals (Optional[int]): An integer counter measuring how many dt - intervals of time passed. The dt is
                                    defined in /dashboard.settings.py and named as 'MAIN_GRAPH_REFRESH_RATE' constant.
            previous_stock (str): This is the last stock selected by the user or with automatic selection (when you
                                  start the application for the first time, it automatically selects the first saved
                                  stock, if any in local database.)

        Returns:
            figure: Union[go.Figure, Type]: Returns either an updated figure or a dash command to not update the figure.
            previous_stock: Union[str, Type]: Returns either None, in case no saved stock exists in local
                                  database, str to save last used stock in a dcc.Store object, or a dash command to not
                                  update the last used stock.

        """

        mode: Optional[Literal["all", "candlesticks", "close_line"]]
        if callback_context.triggered_id == "all_mode":
            mode = "all"
        elif callback_context.triggered_id == "candlesticks_mode":
            mode = "candlesticks"
        elif callback_context.triggered_id == "close_line_mode":
            mode = "close_line"
        else:
            mode = None

        if previous_mode is None:
            mode = "all"
            previous_mode = "all"

        # If regex find a match, save stock_symbol. If stock_symbol is different from last used stock, update figure.
        if bool(re.match(STOCK_BUTTON_REGEX, f"{callback_context.triggered_id}")):
            stock_symbol = re.findall(STOCK_BUTTON_REGEX, f"{callback_context.triggered_id}")[0]
            if stock_symbol != previous_stock:
                return stock_candles_figure(root_path, lock, stock_symbol, previous_mode), stock_symbol, previous_mode

        if (mode != previous_mode) and (mode is not None):
            return stock_candles_figure(root_path, lock, previous_stock, mode), previous_stock, mode

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
                return (
                    stock_candles_figure(root_path, lock, saved_stocks[0], previous_mode),
                    saved_stocks[0],
                    previous_mode,
                )
        return no_update, no_update, previous_mode
