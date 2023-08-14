import dash_bootstrap_components as dbc
from dash import html

navbar = dbc.Container(
    [
        dbc.Col([]),
        dbc.Col(
            [
                html.H2(
                    "Demo Dashboard - D&D",
                    style={
                        "font-size": "xx-large",
                    },
                ),
            ],
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
            },
        ),
        dbc.Col(
            [
                html.Div(
                    [],
                    style={"display": "flex", "flex-flow": "row"},
                )
            ],
            style={
                "display": "flex",
                "flex-flow": "row",
                "justify-content": "flex-end",
                "align-content": "flex-end",
            },
        ),
    ],
    style={
        "width": "100%",
        "max-width": "100%",
        "height": "6%",
        "display": "flex",
        "flex-flow": "row",
        "justify-content": "center",
        "align-content": "center",
        "backgroundColor": "#adb5bd",
    },
)
