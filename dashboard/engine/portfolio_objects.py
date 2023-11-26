import os
import logging
import datetime
import numpy as np
from typing import Optional, List

# from dashboard.engine.black_scholes import BlackScholes
from dashboard.settings import DATABASE_PATH, FULL_YEAR_DAYS, GREAT_MINUS_NUMBER
from dashboard.engine.settings import STD_SMALL_RANGE, DEFAULT_PRICE_GAIN, DEFAULT_ANALYSIS_DAYS
from dashboard.database.functions.generic import run_query

CREATION_STOCKS_DATA_FEED_QUERY = """
                 CREATE TABLE IF NOT EXISTS stocks_data_feed
                 ([timestamp] INTEGER PRIMARY KEY, [pid] INTEGER, [symbol] TEXT, [close] FLOAT,
                 [high] FLOAT, [low] FLOAT, [open] FLOAT, [status] TEXT, [volume] INTEGER)
                 """


class Stock:
    def __init__(
        self,
        root_path: str,
        lock,
        symbol: str,
        risk_free_interest_rate: Optional[float] = None,
        volatility: Optional[float] = None,
    ) -> None:
        self.root_path = root_path
        self.lock = lock
        self.symbol = symbol
        self.prices = self._get_stock_prices()
        self.stock_last_price = self.prices[-1]
        self.volatility = volatility
        if self.volatility is None:
            self.volatility = self._calculate_volatility()
        if risk_free_interest_rate is None:
            self.rf_r = self._calculate_free_interest_rate()
        else:
            self.rf_r = risk_free_interest_rate

    def _get_stock_prices(self):
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

            # If there are any stock_price
            timestamps, open, high, low, close = [[], [], [], [], []]
            for result in results:
                timestamps.append(result[0])
                open.append(result[1])
                high.append(result[2])
                low.append(result[3])
                close.append(result[4])

            timestamps = [datetime.datetime.fromtimestamp(timestamp) for timestamp in timestamps]
        return np.array(close)

    def _calculate_free_interest_rate(self):
        if len(self.prices) < STD_SMALL_RANGE:
            return 0.0
        return self.prices.mean()

    def _std_calculator(self, prices: np.ndarray) -> np.ndarray:
        """This std calculation corresponds to a moving window std calculation with window equal to 4 bins."""
        if list(prices) == []:
            error_message = "Prices is an empty numpy array. Hence std calculator cannot calculate standard deviation."
            logging.error(error_message)
            raise Exception(error_message)
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
        return std.mean()

    def _calculate_volatility(self):
        if len(self.prices) < STD_SMALL_RANGE:
            return self.prices.mean()
        return self._std_calculator(self.prices)


class BlackScholes:
    def __init__(self, stock: Stock, target_days: int) -> None:
        self.stock = stock
        self.target_days = target_days

    def _integral_formula(self, x_axis: np.ndarray) -> np.ndarray:
        return np.exp(-x_axis * x_axis * 0.5)

    def _nd_formula(self, d: float) -> float:
        x_axis = np.arange(GREAT_MINUS_NUMBER, d)
        y_axis = self._integral_formula(x_axis)
        return np.trapz(y_axis)

    def put_solution(self, stock_price: float, strike_price: float) -> float:
        """The put price solution of the Black - Scholes differential equation"""
        if self.stock.volatility is None:
            error_message = f"Please provide a value for stock volatility for stock: {self.stock.symbol}"
            logging.error(error_message)
            raise Exception(error_message)

        d_one = (
            np.log(stock_price / strike_price)
            + (self.stock.rf_r + 0.5 * (self.stock.volatility**2)) * (self.target_days / FULL_YEAR_DAYS)
        ) / (self.stock.volatility * (self.target_days / FULL_YEAR_DAYS) ** 0.5)

        d_two = (
            np.log(stock_price / strike_price)
            + (self.stock.rf_r - 0.5 * (self.stock.volatility**2)) * (self.target_days / FULL_YEAR_DAYS)
        ) / (self.stock.volatility * (self.target_days / FULL_YEAR_DAYS) ** 0.5)

        return strike_price * np.exp(-self.stock.rf_r * (self.target_days / FULL_YEAR_DAYS)) * self._nd_formula(
            -d_two
        ) - stock_price * self._nd_formula(-d_one)

    def call_solution(self, stock_price: float, strike_price: float) -> float:
        """The call price solution of the Black - Scholes differential equation"""
        if self.stock.volatility is None:
            error_message = f"Please provide a value for stock volatility for stock: {self.stock.symbol}"
            logging.error(error_message)
            raise Exception(error_message)

        d_one: float = (
            np.log(stock_price / strike_price)
            + (self.stock.rf_r + 0.5 * (self.stock.volatility**2)) * (self.target_days / FULL_YEAR_DAYS)
        ) / (self.stock.volatility * (self.target_days / FULL_YEAR_DAYS) ** 0.5)

        d_two: float = (
            np.log(stock_price / strike_price)
            + (self.stock.rf_r - 0.5 * (self.stock.volatility**2)) * (self.target_days / FULL_YEAR_DAYS)
        ) / (self.stock.volatility * (self.target_days / FULL_YEAR_DAYS) ** 0.5)

        return stock_price * self._nd_formula(d_one) - strike_price * np.exp(
            -self.stock.rf_r * (self.target_days / FULL_YEAR_DAYS)
        ) * self._nd_formula(d_two)


class Portfolio:
    def __init__(self, stocks: List[Stock], price_gain: float = DEFAULT_PRICE_GAIN) -> None:
        self.stocks = stocks
        self.price_gain = price_gain

    def check_stocks_for_sell(self, analysis_days: int = DEFAULT_ANALYSIS_DAYS):
        stocks_to_sell: List[Stock] = []
        for stock in self.stocks:
            strike_price = (1.0 + self.price_gain) * stock.stock_last_price
            bs = BlackScholes(stock, analysis_days)
            if (bs.call_solution(stock.stock_last_price, strike_price) < 0) or stock.rf_r == 0:
                if stock not in stocks_to_sell:
                    stocks_to_sell.append(stock)
        return stocks_to_sell
