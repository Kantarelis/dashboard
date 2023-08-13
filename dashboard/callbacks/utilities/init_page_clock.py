from dash.dependencies import Input, Output


def init_page_clock(app):
    @app.callback(
        Output("url", "pathname"),
        [Input("init_page_clock", "n_intervals")],
    )
    def init_page_clock_def(n_interval):
        if n_interval is not None or n_interval != 0:
            if n_interval >= 1:
                return "/dashboard_main"
