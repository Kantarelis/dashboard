from dash import dcc

stock_figure = dcc.Graph(
    id="stock_candle_plot",
    animate=False,
    style={
        "width": "65vw",
        "height": "60vh",
        "max-width": "65vw",
        "max-height": "60vh",
    },
    config={
        "displaylogo": False,
        "doubleClickDelay": 1000,
        "scrollZoom": True,
        "editable": True,
        "modeBarButtons": [
            [
                "toImage",
                "autoScale2d",
                "toggleSpikelines",
                "hoverClosestCartesian",
                "hoverCompareCartesian",
                "drawopenpath",
                "drawline",
            ]
        ],
    },
)
