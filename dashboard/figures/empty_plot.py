import plotly.graph_objects as go


def empty_plot() -> go.Figure:
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=[],
                open=[],
                high=[],
                low=[],
                close=[],
            )
        ]
    )
    return fig
