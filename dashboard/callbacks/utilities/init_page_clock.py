from typing import Optional, Type, Union

from dash import Dash, Input, Output, no_update

from dashboard.settings import MAIN_PAGE_PATH, N_INTEGRALS_IN_INIT_PAGE


def init_page_clock(app: Dash):
    @app.callback(
        Output("url", "pathname"),
        [Input("init_page_clock", "n_intervals")],
    )
    def init_page_clock_def(n_interval: Optional[int]) -> Union[str, Type]:
        """Callback function that automatically change after 1 dt time integral from init_page to main page of
        the application.
        """
        if n_interval is not None:
            if n_interval >= N_INTEGRALS_IN_INIT_PAGE:
                return MAIN_PAGE_PATH
        return no_update
