import dash_bootstrap_components as dbc
from dash import dcc, html

modes_buttons = html.Div(
    [
        html.Div(
            [
                dcc.Store(id="last_mode_selected"),
                dbc.Button(
                    "All",
                    id="all_mode",
                    n_clicks=0,
                    style={
                        "display": "flex",
                        "flex-flow": "row",
                        "align-items": "center",
                        "width": "auto",
                    },
                ),
                dbc.Button(
                    "Candlesticks",
                    id="candlesticks_mode",
                    n_clicks=0,
                    style={
                        "display": "flex",
                        "flex-flow": "row",
                        "align-items": "center",
                        "width": "auto",
                    },
                ),
                dbc.Button(
                    "Close Line",
                    id="close_line_mode",
                    n_clicks=0,
                    style={
                        "display": "flex",
                        "flex-flow": "row",
                        "align-items": "center",
                        "width": "auto",
                    },
                ),
            ],
            style={
                "display": "flex",
                "flex-flow": "row",
                "justify-content": "flex-end",
            },
        ),
        html.Div(
            [
                dbc.Button(
                    "Analyse Stocks",
                    id="analyse_stocks",
                    n_clicks=0,
                    style={
                        "display": "flex",
                        "flex-flow": "row",
                        "align-items": "center",
                        "width": "auto",
                    },
                ),
                html.Div(id="analysis_result"),
            ],
            style={
                "display": "flex",
                "flex-flow": "row",
                "justify-content": "flex-end",
            },
        ),
    ],
    style={
        "display": "flex",
        "flex-flow": "column",
        "justify-content": "flex-end",
    },
)
