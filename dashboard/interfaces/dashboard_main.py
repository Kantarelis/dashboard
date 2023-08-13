import dash_bootstrap_components as dbc
from dash import html
from dashboard.interfaces.navbar import navbar
from dashboard.interfaces.containers.stock_figure import stock_figure


# Define Body of the page
body = dbc.Container(
    [
        dbc.Row(
            [],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [],
                ),
                dbc.Col(
                    [
                        html.Div(stock_figure),
                    ],
                    style={
                        "display": "flex",
                        "flex-flow": "column",
                    },
                ),
            ],
        ),
        dbc.Row(
            [],
        ),
    ],
    style={
        "display": "flex",
        "textAlign": "center",
        "justify-content": "center",
        "align-items": "center",
        "max-width": "100%",
        "width": "100%",
        "height": "94%",
        "flex-flow": "column",
    },
)


# Create dashboard_main Div
dashboard_main = html.Div(
    [navbar, body],
    id="home",
    style={
        "backgroundColor": "black",
        "width": "100vw",
        "height": "100vh",
        "max-width": "100vw",
        "max-height": "100vh",
        "display": "flex",
        "flex-flow": "column",
    },
)
