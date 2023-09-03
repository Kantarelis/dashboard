import os
import sqlite3
from sqlite3 import Error

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


def create_connection(db_file):
    """create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def stocks_box(app, root_path, lock):
    @app.callback(
        Output("stocks_box", "children"),
        [Input("refresh_stocks_box", "n_intervals")],
    )
    def stocks_box_def(n_interval):
        db_location: str = os.path.join(root_path, DATABASE_PATH)
        results: list = []
        with lock:
            run_query(CREATION_QUERY, db_location)
            results = run_query(GET_SAVED_STOCKS, db_location)
        saved_stocks = [result[0] for result in results]
        if n_interval is not None:
            return html.Ul([html.Li(stock_symbol) for stock_symbol in saved_stocks])
