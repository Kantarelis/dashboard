from dash import callback_context, dcc
from dash.dependencies import Input, Output, State

from dashboard.engine.finnhubwrapper import FinnhubWrapper
from dashboard.settings import API_KEY


def add_stocks_modal(app):
    @app.callback(
        Output("add_stocks_modal", "is_open"),
        [
            Input("add_stocks", "n_clicks"),
        ],
        State("add_stocks_modal", "is_open"),
    )
    def add_stocks_modal_function(n_clicks, open_modal):
        if callback_context.triggered_id == "add_stocks":
            return not open_modal
        return open_modal


def body_of_add_stocks_modal(app):
    @app.callback(
        Output("all_stocks", "children"),
        [
            Input("add_stocks", "n_clicks"),
        ],
    )
    def body_of_add_stocks_modal_function(n_clicks):
        stocks = []
        if callback_context.triggered_id == "add_stocks":
            fin = FinnhubWrapper(API_KEY)
            all_stocks = fin.stocks_to_list()
            all_stocks_symbols = [stock["symbol"] for stock in all_stocks]

            stocks = [{"label": symbol, "value": symbol} for symbol in all_stocks_symbols]
        return dcc.Dropdown(
            id="stocks_dropdown",
            options=stocks,
            value=[],
            placeholder=["Stocks"],
            style={"width": "100%", "color": "black"},
            optionHeight=55,
            searchable=True,
        )
