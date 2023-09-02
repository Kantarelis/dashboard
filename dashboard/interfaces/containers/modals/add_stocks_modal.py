import dash_bootstrap_components as dbc
import dash_loading_spinners as dls
from dash import html

add_stocks_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Add Stocks to 'your stocks'.")),
        dbc.ModalBody(
            dls.RingChase(
                html.Div(id="all_stocks"),
                color="#435278",
            )
        ),
    ],
    id="add_stocks_modal",
    size="xl",
    centered=True,
    is_open=False,
)
