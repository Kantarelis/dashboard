import dash_bootstrap_components as dbc
import dash_loading_spinners as dls
from dash import html

stocks_portfolio = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Stocks Portfolio")),
        dbc.ModalBody(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    html.H4("Saved stocks:"),
                                ]
                            ),
                            dbc.Row(
                                [
                                    html.Div(
                                        [
                                            html.Div(id="saved_stocks"),
                                        ],
                                        style={"width": "50%"},
                                    ),
                                    dbc.Button(
                                        "Remove from portfolio",
                                        id="remove_stocks_from_portfolio",
                                        n_clicks=0,
                                        style={"width": "auto", "height": "max-content"},
                                    ),
                                ]
                            ),
                        ],
                        style={"display": "flex", "flex-flow": "column"},
                    ),
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    html.H4("All stocks:"),
                                ]
                            ),
                            dbc.Row(
                                [
                                    html.Div(
                                        [
                                            dls.RingChase(
                                                html.Div(id="all_stocks"),
                                                color="#435278",
                                            ),
                                        ],
                                        style={"width": "50%"},
                                    ),
                                    dbc.Button(
                                        "Add to portfolio",
                                        id="add_stocks_to_portfolio",
                                        n_clicks=0,
                                        style={"width": "auto", "height": "max-content"},
                                    ),
                                ]
                            ),
                        ],
                        style={"display": "flex", "flex-flow": "column"},
                    ),
                ],
                style={"display": "flex", "flex-flow": "row"},
            )
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Done",
                id="close_portfolio",
                n_clicks=0,
                style={"width": "auto", "height": "max-content"},
            ),
        ),
    ],
    id="stocks_portfolio_modal",
    size="xl",
    centered=True,
    is_open=False,
    backdrop=False,
)
