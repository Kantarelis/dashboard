import os

import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output


from dashboard.database.functions.generic import run_query
from dashboard.settings import DATABASE_PATH

CREATION_QUERY = """
                 CREATE TABLE IF NOT EXISTS saved_stocks
                 ([pid] INTEGER PRIMARY KEY AUTOINCREMENT, [symbol] TEXT UNIQUE NOT NULL, [name] TEXT, [country] TEXT,
                 [currency] TEXT, [estimateCurrency]  TEXT, [exchange] TEXT, [finnhubIndustry] TEXT, [ipo] TEXT,
                 [logo] TEXT, [marketCapitalization] TEXT, [phone] TEXT, [shareOutstanding] TEXT, [ticker] TEXT,
                 [weburl] TEXT)
                 """


GET_SAVED_STOCKS = """
                SELECT symbol FROM saved_stocks
                """


def stocks_box(app, root_path, lock):
    @app.callback(
        Output("stocks_box", "children"),
        Input("stocks_portfolio_modal", "is_open"),
    )
    def stocks_box_def(is_modal_open: bool):
        db_location: str = os.path.abspath(os.path.join(root_path, DATABASE_PATH))
        results: list = []
        with lock:
            run_query(CREATION_QUERY, db_location)
            results = run_query(GET_SAVED_STOCKS, db_location)
        saved_stocks = [result[0] for result in results]
        if is_modal_open is False:
            return html.Div(
                [
                    dbc.Button(
                        [stock_symbol],
                        id={"type": "stock_button", "index": stock_symbol},
                        size="sm",
                        color="secondary",
                    )
                    for stock_symbol in saved_stocks
                ],
                style={"display": "flex", "flex-flow": "column"},
            )
