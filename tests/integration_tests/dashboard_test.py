from dash.testing.application_runners import import_app
from dashboard.run import Dashboard


def test_dashboard(dash_duo):
    dashboard = Dashboard()

    app = import_app(dashboard.app)
    dash_duo.start_server(app)
    dash_duo.wait_for_text_to_equal("h1", "Hello Dash", timeout=4)
