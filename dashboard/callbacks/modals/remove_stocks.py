from dash import callback_context
from dash.dependencies import Input, Output, State


def remove_stocks_modal(app):
    @app.callback(
        Output("remove_stocks_modal", "is_open"),
        [
            Input("remove_stocks", "n_clicks"),
        ],
        State("remove_stocks_modal", "is_open"),
    )
    def remove_stocks_modal_function(n_clicks, open_modal):
        if callback_context.triggered_id == "remove_stocks":
            return not open_modal
        return open_modal
