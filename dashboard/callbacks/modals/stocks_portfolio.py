from dash import callback_context, dcc, no_update
from dash.dependencies import Input, Output, State

from dashboard.database.functions.generic import run_query
from dashboard.engine.finnhubwrapper import FinnhubWrapper
from dashboard.settings import API_KEY, DATABASE_PATH

SELECT_QUERY = "SELECT symbol FROM saved_stocks"
CREATION_QUERY = """
                 CREATE TABLE IF NOT EXISTS saved_stocks
                 ([pid] INTEGER PRIMARY KEY AUTOINCREMENT, [symbol] TEXT UNIQUE NOT NULL, [name] TEXT, [country] TEXT,
                 [currency] TEXT, [estimateCurrency]  TEXT, [exchange] TEXT, [finnhubIndustry] TEXT, [ipo] TEXT,
                 [logo] TEXT, [marketCapitalization] TEXT, [phone] TEXT, [shareOutstanding] TEXT, [ticker] TEXT,
                 [weburl] TEXT)
                 """


def stocks_portfolio_modal(app):
    @app.callback(
        Output("stocks_portfolio_modal", "is_open"),
        [
            Input("stocks_portfolio_button", "n_clicks"),
            Input("close_portfolio", "n_clicks"),
        ],
        State("stocks_portfolio_modal", "is_open"),
    )
    def stocks_portfolio_modal_function(n_clicks_open, n_clicks_close, open_modal):
        if (
            callback_context.triggered_id == "stocks_portfolio_button"
            or callback_context.triggered_id == "close_portfolio"
        ):
            return not open_modal
        return open_modal


def right_body_of_stocks_portfolio_modal(app):
    @app.callback(
        Output("all_stocks", "children"),
        [
            Input("stocks_portfolio_button", "n_clicks"),
        ],
    )
    def right_body_of_stocks_portfolio_modal_function(n_clicks):
        stocks = []
        if callback_context.triggered_id == "stocks_portfolio_button":
            fin = FinnhubWrapper(API_KEY)
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


def left_body_of_stocks_portfolio_modal(app, lock):
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
        n_clicks_portfolio, n_clicks_add_stocks, n_clicks_remove_stocks, saved_stocks_add_list, saved_stocks_remove_list
    ):
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


def add_stocks_to_database(app, lock):
    @app.callback(
        Output("all_stocks_dropdown", "value"),
        Output("saved_stocks_add_list", "value"),
        [
            Input("add_stocks_to_portfolio", "n_clicks"),
            Input("all_stocks_dropdown", "value"),
        ],
        prevent_initial_call=True,
    )
    def add_stocks_to_database_function(n_clicks, selected_stocks):
        results: list = []
        saved_stocks: list = []

        if callback_context.triggered_id == "add_stocks_to_portfolio":
            fin = FinnhubWrapper(API_KEY)
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
            selected_stocks = []

            return selected_stocks, saved_stocks
        return no_update, no_update


def remove_stocks_from_database(app, lock):
    @app.callback(
        Output("saved_stocks_dropdown", "value"),
        Output("saved_stocks_remove_list", "value"),
        [
            Input("remove_stocks_from_portfolio", "n_clicks"),
            Input("saved_stocks_dropdown", "value"),
        ],
        prevent_initial_call=True,
    )
    def remove_stocks_from_database_function(n_clicks, selected_stocks):
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
            selected_stocks = []

            return selected_stocks, saved_stocks
        return no_update, no_update
