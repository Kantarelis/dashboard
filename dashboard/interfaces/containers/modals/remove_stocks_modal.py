import dash_bootstrap_components as dbc
from dash import html  # , dcc

remove_stocks_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Remove Stocks from 'your stocks'.")),
        dbc.ModalBody(
            html.Div(id="stocks_box"),
        ),
    ],
    id="remove_stocks_modal",
    size="xl",
    centered=True,
    is_open=False,
)
