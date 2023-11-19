import numpy as np

from dashboard.settings import FULL_YEAR_DAYS, GREAT_MINUS_NUMBER


class BlackScholes:
    def __init__(self, risk_free_interest_rate: float, volatility: float, target_days: int) -> None:
        self.rf_r = risk_free_interest_rate
        self.volatility = volatility
        self.target_days = target_days

    def _integral_formula(self, x_axis: np.ndarray) -> np.ndarray:
        return np.exp(-x_axis * x_axis * 0.5)

    def _nd_formula(self, d: float) -> float:
        x_axis = np.arange(GREAT_MINUS_NUMBER, d)
        y_axis = self._integral_formula(x_axis)
        return np.trapz(y_axis)

    def solution(self, stock_price: float, strike_price: float) -> float:
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
