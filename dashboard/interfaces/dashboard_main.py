import dash_bootstrap_components as dbc
from dash import dcc, html

from dashboard.interfaces.containers.modals.stocks_portfolio import stocks_portfolio
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
                                        dbc.Button("Portfolio", id="stocks_portfolio_button", n_clicks=0),
                                        html.Div(stocks_portfolio),
                                        dcc.Store(id="saved_stocks_add_list"),
                                        dcc.Store(id="saved_stocks_remove_list")
                                        # html.Div(id="add_stocks_to_database_dummy"),
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
                                html.H4("Stocks Portfolio"),
                                html.Div(id="stocks_box"),
                                dcc.Interval(id="refresh_stocks_box", interval=1 * 1000, n_intervals=0),
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
