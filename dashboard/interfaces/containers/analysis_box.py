import dash_bootstrap_components as dbc
from dash import html

analysis_box = html.Div(
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
        "flex-flow": "column",
        "justify-content": "flex-end",
    },
)
