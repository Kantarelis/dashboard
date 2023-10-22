import dash_bootstrap_components as dbc
import dash_extensions as de
from dash import dcc, html

from dashboard.interfaces.navbar import navbar
from dashboard.settings import N_INTEGRALS_IN_INIT_PAGE, TIME_INTEGRAL_OF_IN_INIT_PAGE, URL_ANIMATION

# Define Body of the page
body = dbc.Container(
    [
        dbc.Row(
            [
                html.H1("Demo Dashboard", style={"textAlign": "center"}),
            ],
            style={"display": "flex", "flex-flow": "row"},
        ),
        html.Div(
            de.Lottie(
                options=dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio="xMidYMid slice")),
                width="50%",
                height="50%",
                url=URL_ANIMATION,
                isClickToPauseDisabled=True,
            )
        ),
        dbc.Row(
            [
                html.H2(
                    "by Spyros Kantarelis",
                    style={
                        "textAlign": "center",
                    },
                ),
            ]
        ),
        dcc.Interval(id="init_page_clock", interval=TIME_INTEGRAL_OF_IN_INIT_PAGE * N_INTEGRALS_IN_INIT_PAGE),
    ],
    style={
        "display": "flex",
        "flex-flow": "column",
        "textAlign": "center",
        "justify-content": "center",
        "align-items": "center",
        "max-width": "100%",
        "width": "100%",
        "height": "94%",
    },
)


# Create Homepage
init_page = html.Div(
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
