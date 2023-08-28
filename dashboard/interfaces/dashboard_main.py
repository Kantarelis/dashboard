import dash_bootstrap_components as dbc
from dash import dcc, html

from dashboard.interfaces.containers.modals.add_stocks_modal import add_stocks_modal
from dashboard.interfaces.containers.modals.remove_stocks_modal import remove_stocks_modal
from dashboard.interfaces.containers.stock_figure import stock_figure
from dashboard.interfaces.navbar import navbar

# Body of the main page
body = dbc.Container(
    [
        dbc.Row(
            [],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.H4("Your Stocks:"),
                                dbc.ListGroup(
                                    [
                                        dbc.Button("-", title="remove stocks", id="remove_stocks", n_clicks=0),
                                        dbc.Button("+", title="add stocks", id="add_stocks", n_clicks=0),
                                        html.Div(add_stocks_modal),
                                        html.Div(remove_stocks_modal),
                                    ],
                                    horizontal=True,
                                    style={
                                        "display": "flex",
                                        "flex-flow": "row",
                                        "align-items": "center",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flex-flow": "column",
                                "align-items": "left",
                            },
                        ),
                        dbc.Row(
                            [
                                html.Div(id="stocks_box"),
                                dcc.Interval(id="refresh_stocks_box", interval=1 * 1000, n_intervals=0),
                                # html.H4("TODO: Stocks Box"),
                            ],
                            style={
                                "display": "flex",
                                "flex-flow": "column",
                                "align-items": "left",
                            },
                        ),
                    ],
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
