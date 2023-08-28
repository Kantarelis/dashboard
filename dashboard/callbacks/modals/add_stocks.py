from dash import callback_context
from dash.dependencies import Input, Output, State


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
