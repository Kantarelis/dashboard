import dash_bootstrap_components as dbc
from dash import dcc, html

from dashboard.interfaces.navbar import navbar
from dashboard.settings import N_INTEGRALS_IN_INIT_PAGE, TIME_INTEGRAL_OF_IN_INIT_PAGE

# Define Body of the page
body = dbc.Container(
    [
        html.H5("This Is The Init Page", style={"textAlign": "center"}),
        dcc.Interval(id="init_page_clock", interval=TIME_INTEGRAL_OF_IN_INIT_PAGE * N_INTEGRALS_IN_INIT_PAGE),
    ],
    style={
        "display": "flex",
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
