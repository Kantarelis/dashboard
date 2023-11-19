from dash import html, dcc
import dash_bootstrap_components as dbc

modes_buttons = html.Div(
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
)
