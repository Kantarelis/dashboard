import os
from multiprocessing.synchronize import Lock as LockType

from dash import Dash, Input, Output, callback_context, html

from dashboard.database.functions.generic import run_query
from dashboard.engine.portfolio_objects import Portfolio, Stock
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


def analyse_stocks(app: Dash, root_path: str, lock: LockType):
    @app.callback(
        Output("analysis_result", "children"),
        Input("analyse_stocks", "n_clicks"),
    )
    def analyse_stocks_function(n_clicks: int) -> html.Div:
        stocks_to_sell = []
        if (n_clicks is not None) and (callback_context.triggered_id == "analyse_stocks"):
            db_location: str = os.path.abspath(os.path.join(root_path, DATABASE_PATH))
            results: list = []
            with lock:
                run_query(CREATION_QUERY, db_location)
                results = run_query(GET_SAVED_STOCKS, db_location)
            saved_stocks = [result[0] for result in results]
            list_of_stocks = [Stock(root_path, lock, symbol) for symbol in saved_stocks]
            portfolio = Portfolio(list_of_stocks)
            stocks_to_sell = portfolio.check_stocks_for_sell()

            if stocks_to_sell:
                return html.Div(
                    [
                        html.H5("Sell these stocks:"),
                        html.Ul(children=[html.Li(stock.symbol) for stock in stocks_to_sell]),
                    ]
                )
            else:
                return html.Div([html.H5("Keep them all!")])
        return html.Div([html.H5("No analysis yet...")])
