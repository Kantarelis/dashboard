import numpy as np
import logging
from dashboard.settings import FULL_YEAR_DAYS, GREAT_MINUS_NUMBER
from dashboard.engine.portfolio_objects import Stock


class BlackScholes(Stock):
    def __init__(self, target_days: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.target_days = target_days

    def _integral_formula(self, x_axis: np.ndarray) -> np.ndarray:
        return np.exp(-x_axis * x_axis * 0.5)

    def _nd_formula(self, d: float) -> float:
        x_axis = np.arange(GREAT_MINUS_NUMBER, d)
        y_axis = self._integral_formula(x_axis)
        return np.trapz(y_axis)

    def put_solution(self, stock_price: float, strike_price: float) -> float:
        if self.volatility is None:
            error_message = f"Please provide a value for stock volatility for stock: {self.symbol}"
            logging.error(error_message)
            raise Exception(error_message)

        d_one = (
            np.log(stock_price / strike_price)
            + (self.rf_r + 0.5 * (self.volatility**2)) * (self.target_days / FULL_YEAR_DAYS)
        ) / (self.volatility * (self.target_days / FULL_YEAR_DAYS) ** 0.5)

        d_two = (
            np.log(stock_price / strike_price)
            + (self.rf_r - 0.5 * (self.volatility**2)) * (self.target_days / FULL_YEAR_DAYS)
        ) / (self.volatility * (self.target_days / FULL_YEAR_DAYS) ** 0.5)

        return strike_price * np.exp(-self.rf_r * (self.target_days / FULL_YEAR_DAYS)) * self._nd_formula(
            -d_two
        ) - stock_price * self._nd_formula(-d_one)

    def call_solution(self, stock_price: float, strike_price: float) -> float:
        if self.volatility is None:
            error_message = f"Please provide a value for stock volatility for stock: {self.symbol}"
            logging.error(error_message)
            raise Exception(error_message)

        d_one = (
            np.log(stock_price / strike_price)
            + (self.rf_r + 0.5 * (self.volatility**2)) * (self.target_days / FULL_YEAR_DAYS)
        ) / (self.volatility * (self.target_days / FULL_YEAR_DAYS) ** 0.5)

        d_two = (
            np.log(stock_price / strike_price)
            + (self.rf_r - 0.5 * (self.volatility**2)) * (self.target_days / FULL_YEAR_DAYS)
        ) / (self.volatility * (self.target_days / FULL_YEAR_DAYS) ** 0.5)

        return stock_price * self._nd_formula(d_one) - strike_price * np.exp(
            -self.rf_r * (self.target_days / FULL_YEAR_DAYS)
        ) * self._nd_formula(d_two)
