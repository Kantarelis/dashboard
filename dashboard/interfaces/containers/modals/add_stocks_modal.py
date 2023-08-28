import dash_bootstrap_components as dbc
from dash import html

add_stocks_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Add Stocks to 'your stocks'.")),
        dbc.ModalBody(
            html.Div(id="all_stocks"),
        ),
    ],
    id="add_stocks_modal",
    size="xl",
    centered=True,
    is_open=False,
)
