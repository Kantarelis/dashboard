import dash_bootstrap_components as dbc
from dash import html
from dashboard.interfaces.navbar import Navbar

# Load Navbar
nav = Navbar()

# Define Body of the page
body = dbc.Container(
    [],
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


# Create Homepage
def dashboard_main():
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
