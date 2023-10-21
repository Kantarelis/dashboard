from multiprocessing.synchronize import Lock as LockType
from typing import List, Tuple

from dash import Dash, callback_context, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from dashboard.database.functions.generic import get_api_key, run_query
from dashboard.engine.finnhubwrapper import FinnhubWrapper
from dashboard.settings import DATABASE_PATH

SELECT_QUERY = "SELECT symbol FROM saved_stocks"
CREATION_QUERY = """
                 CREATE TABLE IF NOT EXISTS saved_stocks
                 ([pid] INTEGER PRIMARY KEY AUTOINCREMENT, [symbol] TEXT UNIQUE NOT NULL, [name] TEXT, [country] TEXT,
                 [currency] TEXT, [estimateCurrency]  TEXT, [exchange] TEXT, [finnhubIndustry] TEXT, [ipo] TEXT,
                 [logo] TEXT, [marketCapitalization] TEXT, [phone] TEXT, [shareOutstanding] TEXT, [ticker] TEXT,
                 [weburl] TEXT)
                 """


def stocks_portfolio_modal(app: Dash):
    @app.callback(
        Output("stocks_portfolio_modal", "is_open"),
        [
            Input("stocks_portfolio_button", "n_clicks"),
            Input("close_portfolio", "n_clicks"),
        ],
        State("stocks_portfolio_modal", "is_open"),
    )
    def stocks_portfolio_modal_function(n_clicks_open: int, n_clicks_close: int, open_modal: bool) -> bool:
        """Callback function for opening-closing stocks portfolio modal."""
        if (
            callback_context.triggered_id == "stocks_portfolio_button"
            or callback_context.triggered_id == "close_portfolio"
        ):
            return not open_modal
        return open_modal


def right_body_of_stocks_portfolio_modal(app: Dash):
    @app.callback(
        Output("all_stocks", "children"),
        [
            Input("stocks_portfolio_button", "n_clicks"),
        ],
    )
    def right_body_of_stocks_portfolio_modal_function(n_clicks: int) -> dcc.Dropdown:
        """Callback function for creating a dynamic dropdown menu with all available stocks a user
        potentially can select from finhub sources."""
        stocks: List[dict] = []
        if callback_context.triggered_id == "stocks_portfolio_button":
            fin = FinnhubWrapper(get_api_key())
            all_stocks = fin.stocks_to_list()
            all_stocks_symbols = [stock["symbol"] for stock in all_stocks]
            stocks = [{"label": symbol, "value": symbol} for symbol in all_stocks_symbols]
        return dcc.Dropdown(
            id="all_stocks_dropdown",
            options=stocks,
            placeholder="Search for stocks...",
            style={"width": "100%", "color": "black"},
            optionHeight=55,
            searchable=True,
            multi=True,
        )


def left_body_of_stocks_portfolio_modal(app: Dash, lock: LockType):
    @app.callback(
        Output("saved_stocks", "children"),
        [
            Input("stocks_portfolio_button", "n_clicks"),
            Input("add_stocks_to_portfolio", "n_clicks"),
            Input("remove_stocks_from_portfolio", "n_clicks"),
            Input("saved_stocks_add_list", "value"),
            Input("saved_stocks_remove_list", "value"),
        ],
    )
    def left_body_of_stocks_portfolio_modal_function(
        n_clicks_portfolio: int,
        n_clicks_add_stocks: int,
        n_clicks_remove_stocks: int,
        saved_stocks_add_list: list,
        saved_stocks_remove_list: list,
    ) -> dcc.Dropdown:
        """Callback function for creating a dynamic dropdown menu with all saved stock in local database."""
        results: list = []
        saved_stocks: list = []
        if callback_context.triggered_id == "stocks_portfolio_button":
            with lock:
                results = run_query(SELECT_QUERY, DATABASE_PATH)
            if results:
                saved_stocks = [result[0] for result in results]
        elif callback_context.triggered_id == "add_stocks_to_portfolio":
            results = saved_stocks_add_list
            if results:
                saved_stocks = results
        elif callback_context.triggered_id == "remove_stocks_from_portfolio":
            results = saved_stocks_remove_list
            if results:
                saved_stocks = results

        return dcc.Dropdown(
            id="saved_stocks_dropdown",
            options=saved_stocks,
            placeholder="Search for stocks...",
            style={"width": "100%", "color": "black"},
            optionHeight=55,
            searchable=True,
            multi=True,
        )


def add_stocks_to_database(app: Dash, lock: LockType):
    @app.callback(
        Output("all_stocks_dropdown", "value"),
        Output("saved_stocks_add_list", "value"),
        [
            Input("add_stocks_to_portfolio", "n_clicks"),
            Input("all_stocks_dropdown", "value"),
        ],
        prevent_initial_call=True,
    )
    def add_stocks_to_database_function(n_clicks: int, selected_stocks: list) -> Tuple[list, list]:
        """Callback function that saves multiple selected stock, user selected, in local database."""
        results: list = []
        saved_stocks: list = []

        if callback_context.triggered_id == "add_stocks_to_portfolio":
            fin = FinnhubWrapper(get_api_key())
            for symbol in selected_stocks:
                cp = fin.company_profile(symbol)
                stock = f"('{symbol}', 'None', 'None', 'None', "
                stock += "'None', 'None', 'None', "
                stock += "'None', 'None', 'None', 'None', "
                stock += "'None', 'None', 'None');"
                if cp:
                    stock = f"('{symbol}', '{cp['name']}', '{cp['country']}', '{cp['currency']}', "
                    stock += f"'{cp['estimateCurrency']}', '{cp['exchange']}', '{cp['finnhubIndustry']}', "
                    stock += f"'{cp['ipo']}', '{cp['logo']}', '{cp['marketCapitalization']}', '{cp['phone']}', "
                    stock += f"'{cp['shareOutstanding']}', '{cp['ticker']}', '{cp['weburl']}')"
                insert_query = f"""
                           INSERT INTO saved_stocks (symbol, name, country, currency, estimateCurrency, exchange,
                           finnhubIndustry, ipo, logo, marketCapitalization, phone, shareOutstanding, ticker, weburl)
                           VALUES {stock}
                           ON CONFLICT (symbol) DO NOTHING;
                           """

                with lock:
                    run_query(CREATION_QUERY, DATABASE_PATH)
                    run_query(insert_query, DATABASE_PATH)

            with lock:
                results = run_query(SELECT_QUERY, DATABASE_PATH)

            if results:
                saved_stocks = [result[0] for result in results]

            # Restart Selected stocks values
            selected_stocks.clear()

            return selected_stocks, saved_stocks
        raise PreventUpdate


def remove_stocks_from_database(app: Dash, lock: LockType):
    @app.callback(
        Output("saved_stocks_dropdown", "value"),
        Output("saved_stocks_remove_list", "value"),
        [
            Input("remove_stocks_from_portfolio", "n_clicks"),
            Input("saved_stocks_dropdown", "value"),
        ],
        prevent_initial_call=True,
    )
    def remove_stocks_from_database_function(n_clicks: int, selected_stocks: list) -> Tuple[list, list]:
        """Callback function for removing selected stocks, user selected, from local database alongside with their
        corresponding data.
        """
        # Restart Selected stocks values
        results: list = []
        saved_stocks: list = []

        if callback_context.triggered_id == "remove_stocks_from_portfolio":
            for symbol in selected_stocks:
                delete_query = f"""
                                DELETE FROM saved_stocks
                                WHERE symbol='{symbol}';
                                """
                with lock:
                    run_query(CREATION_QUERY, DATABASE_PATH)
                    run_query(delete_query, DATABASE_PATH)

            with lock:
                results = run_query(SELECT_QUERY, DATABASE_PATH)
            if results:
                saved_stocks = [result[0] for result in results]

            # Restart Selected stocks values
            selected_stocks.clear()

            return selected_stocks, saved_stocks
        raise PreventUpdate
