import os

from dash import html
from dash.dependencies import Input, Output

from dashboard.database.functions.generic import run_query
from dashboard.settings import DATABASE_PATH

CREATION_QUERY = """
            CREATE TABLE IF NOT EXISTS saved_stocks
            ([symbol] TEXT, [datetime] TEXT)
            """


GET_SAVED_STOCKS = """
                SELECT symbol FROM saved_stocks
                """
import sqlite3
from sqlite3 import Error


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
        print(n_interval)
        # TODO: draw data from database
        saved_stocks = ["First", "Second", "Third", "This is a demo...", "fix in stocks_box.py"]

        db_location = os.path.join(root_path, DATABASE_PATH)

        print(db_location)

        with lock:
            run_query(CREATION_QUERY, db_location)
            results = run_query(GET_SAVED_STOCKS, db_location)

        print(results)

        if n_interval is not None:
            return html.Ul([html.Li(stock_symbol) for stock_symbol in saved_stocks])
