import datetime
import os
from multiprocessing.synchronize import Lock as LockType
from typing import Literal

import plotly.graph_objects as go

from dashboard.database.functions.generic import run_query
from dashboard.figures.empty_plot import empty_plot
from dashboard.settings import DATABASE_PATH

CREATION_STOCKS_DATA_FEED_QUERY = """
                 CREATE TABLE IF NOT EXISTS stocks_data_feed
                 ([timestamp] INTEGER PRIMARY KEY, [pid] INTEGER, [symbol] TEXT, [close] FLOAT,
                 [high] FLOAT, [low] FLOAT, [open] FLOAT, [status] TEXT, [volume] INTEGER)
                 """


def stock_candles_figure(
    root_path: str, lock: LockType, stock_symbol: str, mode: Literal["all", "candlesticks", "close_line"]
) -> go.Figure:
    # Gather results of selected stock.
    get_candle_stock_data = f"""
                SELECT timestamp, open, high, low, close
                FROM stocks_data_feed
                WHERE symbol='{stock_symbol}'
                """
    db_location = os.path.abspath(os.path.join(root_path, DATABASE_PATH))
    with lock:
        run_query(CREATION_STOCKS_DATA_FEED_QUERY, db_location)
        results = run_query(get_candle_stock_data, db_location)

    # If there are any results create the plotly figure Candlestick plot.
    if results:
        timestamps, open, high, low, close = [[], [], [], [], []]
        for result in results:
            timestamps.append(result[0])
            open.append(result[1])
            high.append(result[2])
            low.append(result[3])
            close.append(result[4])

        timestamps = [datetime.datetime.fromtimestamp(timestamp) for timestamp in timestamps]
        fig = go.Figure()

        if mode in ["all", "candlesticks"]:
            fig.add_trace(
                go.Candlestick(
                    x=timestamps,
                    open=open,
                    high=high,
                    low=low,
                    close=close,
                    name="Candlestick plot",
                )
            )
        if mode in ["all", "close_line"]:
            fig.add_trace(
                go.Scatter(
                    x=timestamps,
                    y=close,
                    mode="lines",
                    name="Closing Price",
                    line=dict(color="orange", width=2.75),
                    connectgaps=True,
                )
            )

        fig.update_layout(
            title=dict(text=f"{stock_symbol} analysis.", x=0.45),
            xaxis_title="Datetime",
            yaxis_title="Price",
            font=dict(family="Roboto", size=18, color="white"),
            paper_bgcolor="rgba(0,0,0,0)",
        )

        # Space between y axis and plot
        fig.update_yaxes(ticksuffix="   ")
        return fig
    # Else return an empty data plotly figure Candlestick plot.
    return empty_plot()
