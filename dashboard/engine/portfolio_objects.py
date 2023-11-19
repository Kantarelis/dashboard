import os
import datetime
import numpy as np
from typing import Optional, List
from dashboard.engine.black_scholes import BlackScholes
from dashboard.settings import DATABASE_PATH
from dashboard.engine.settings import STD_SMALL_RANGE
from dashboard.database.functions.generic import run_query

CREATION_STOCKS_DATA_FEED_QUERY = """
                 CREATE TABLE IF NOT EXISTS stocks_data_feed
                 ([timestamp] INTEGER PRIMARY KEY, [pid] INTEGER, [symbol] TEXT, [close] FLOAT,
                 [high] FLOAT, [low] FLOAT, [open] FLOAT, [status] TEXT, [volume] INTEGER)
                 """


class Stock:
    def __init__(
        self, symbol: str, risk_free_interest_rate: float, volatility: Optional[float], root_path: str, lock
    ) -> None:
        self.symbol = symbol
        self.rf_r = risk_free_interest_rate
        self.volatility = volatility
        if self.volatility is None:
            self.volatility = self._calculate_volatility()
        self.root_path = root_path
        self.lock = lock

    def _std_calculator(self, prices: np.ndarray) -> np.ndarray:
        """This std calculation corresponds to a moving window std calculation with window equal to 4 bins."""
        prices_matrix = np.array(
            [
                prices,
                np.append(prices[1:], [np.NaN]),
                np.append(prices[2:], [np.NaN, np.NaN]),
                np.append(prices[3:], [np.NaN, np.NaN, np.NaN]),
            ]
        )
        std = np.std(prices_matrix, axis=0)
        std = np.append(std[:-STD_SMALL_RANGE], [0.0, 0.0, 0.0, 0.0])
        return std

    def _calculate_volatility(self):
        # Gather results of selected stock.
        get_candle_stock_data = f"""
                    SELECT timestamp, open, high, low, close
                    FROM stocks_data_feed
                    WHERE symbol='{self.symbol}'
                    """
        db_location = os.path.abspath(os.path.join(self.root_path, DATABASE_PATH))
        with self.lock:
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

            return self._std_calculator(np.array(close))


class Portfolio:
    def __init__(self, stocks: List[Stock], price_gain: float) -> None:
        self.stocks = stocks
        self.price_gain = price_gain

    def check_stocks_for_sell(self, analysis_days: int, stock_price: float):
        stocks_to_sell: List[Stock] = []
        for stock in self.stocks:
            strike_price = (1.0 + self.price_gain) * stock_price
            bs = BlackScholes(analysis_days, stock.symbol, stock.rf_r, stock.volatility)
            if bs.solution(stock_price, strike_price) < 0:
                if stock not in stocks_to_sell:
                    stocks_to_sell.append(stock)
        return stocks_to_sell
