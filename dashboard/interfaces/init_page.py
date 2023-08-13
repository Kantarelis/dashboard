import dash_bootstrap_components as dbc
from dash import html, dcc
from dashboard.interfaces.navbar import Navbar

# Load Navbar
nav = Navbar()

# Define Body of the page
body = dbc.Container(
    [
        html.H5("This Is The Init Page", style={"textAlign": "center"}),
        dcc.Interval(id="init_page_clock", interval=1 * 1000, n_intervals=0),
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
def init_page():
    layout = html.Div(
        [nav, body],
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

    return layout
