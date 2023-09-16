import re
from dash import Input, Output, ALL, callback_context, no_update
from dashboard.callbacks.settings import STOCK_BUTTON_REGEX
from dashboard.figures.stock_candles import stock_candles_figure

# from dashboard.figures.empty_plot import empty_plot


def stock_candles_plot(app, root_path, lock):
    @app.callback(
        Output("stock_candle_plot", "figure"),
        Output("last_stock_selected", "value"),
        Input({"type": "stock_button", "index": ALL}, "n_clicks"),
        Input("refresh_figure", "n_intervals"),
        Input("last_stock_selected", "value"),
        prevent_initial_call=True,
    )
    def stock_candles_plot_function(stocks_n_clicks: list, n_intervals: int, selected_symbol: str):
        print("GUN!")
        print(f"This is the selected symbol: {selected_symbol}")
        print(f"This is the trigger: {callback_context.triggered_id}")

        if bool(re.match(STOCK_BUTTON_REGEX, f"{callback_context.triggered_id}")):
            stock_symbol = re.findall(STOCK_BUTTON_REGEX, f"{callback_context.triggered_id}")[0]
            if stock_symbol != selected_symbol:
                print(f"Saved value: {stock_symbol}")
                return no_update, stock_symbol
        saved_stocks = [
            callback_context.inputs_list[0][n_click]["id"]["index"]
            for n_click in range(len(callback_context.inputs_list[0]))
        ]

        print(f"Saved stocks are: {saved_stocks}")
        if selected_symbol in saved_stocks:
            print("GUN THE FIG!")
            return stock_candles_figure(root_path, lock, selected_symbol), no_update

        print("This is the empty plot")
        return no_update, None


# if bool(re.match(STOCK_BUTTON_REGEX, f"{callback_context.triggered_id}")):
# stock_symbol = re.findall(STOCK_BUTTON_REGEX, f"{callback_context.triggered_id}")[0]
# if stock_candles_figure(root_path, lock, selected_symbol) is not None:
