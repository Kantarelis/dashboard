import os
from multiprocessing import Lock

import numpy as np
import pytest

from dashboard.engine.portfolio_objects import BlackScholes, Portfolio, Stock


def test_Stock__init__(mocker):
    root_path = os.path.abspath(os.path.dirname(__file__))
    lock = Lock()
    symbol = "DUMMYSTOCK"
    risk_free_interest_rate = None
    volatility = None

    def _get_stock_prices():
        return np.array([1.0, 2.0, 3.0, 4.0, 3.0, 2.0, 1.0])

    mocker.patch("dashboard.engine.portfolio_objects.Stock._get_stock_prices", side_effect=_get_stock_prices)

    stock = Stock(root_path, lock, symbol, risk_free_interest_rate=risk_free_interest_rate, volatility=volatility)

    assert stock.root_path == root_path
    assert stock.lock == lock
    assert stock.symbol == symbol
    assert np.all(stock.prices == np.array([1.0, 2.0, 3.0, 4.0, 3.0, 2.0, 1.0]))
    assert stock.last_price == 1.0
    assert stock.rf_r == pytest.approx(2.2857142857142856)
    assert stock.volatility == pytest.approx(0.3617496501604271)


def test__calculate_free_interest_rate(mocker):
    root_path = os.path.abspath(os.path.dirname(__file__))
    lock = Lock()
    symbol = "DUMMYSTOCK"
    risk_free_interest_rate = None
    volatility = None

    def _get_stock_prices():
        return np.array([1.0, 2.0, 3.0, 4.0, 3.0, 2.0, 1.0])

    mocker.patch("dashboard.engine.portfolio_objects.Stock._get_stock_prices", side_effect=_get_stock_prices)
    stock = Stock(root_path, lock, symbol, risk_free_interest_rate=risk_free_interest_rate, volatility=volatility)
    fr_r = stock._calculate_free_interest_rate()

    assert fr_r == pytest.approx(2.2857142857142856)


def test_BlackScholes__init__(mocker):
    root_path = os.path.abspath(os.path.dirname(__file__))
    lock = Lock()
    symbol = "DUMMYSTOCK"
    risk_free_interest_rate = None
    volatility = None

    def _get_stock_prices():
        return np.array([1.0, 2.0, 3.0, 4.0, 3.0, 2.0, 1.0])

    mocker.patch("dashboard.engine.portfolio_objects.Stock._get_stock_prices", side_effect=_get_stock_prices)

    stock = Stock(root_path, lock, symbol, risk_free_interest_rate=risk_free_interest_rate, volatility=volatility)
    target_days = 1
    bs = BlackScholes(stock, target_days)

    assert bs.stock == stock
    assert bs.target_days == target_days


def test_put_solution(mocker):
    root_path = os.path.abspath(os.path.dirname(__file__))
    lock = Lock()
    symbol = "DUMMYSTOCK"
    risk_free_interest_rate = None
    volatility = None

    def _get_stock_prices():
        return np.array([1.0, 2.0, 3.0, 4.0, 3.0, 2.0, 1.0])

    mocker.patch("dashboard.engine.portfolio_objects.Stock._get_stock_prices", side_effect=_get_stock_prices)

    stock = Stock(root_path, lock, symbol, risk_free_interest_rate=risk_free_interest_rate, volatility=volatility)
    target_days = 1

    bs = BlackScholes(stock, target_days)

    stock_price = 1.0
    strike_price = 15.0

    gain = bs.put_solution(stock_price, strike_price)

    assert gain == pytest.approx(34.85807545932756)


def test_call_solution(mocker):
    root_path = os.path.abspath(os.path.dirname(__file__))
    lock = Lock()
    symbol = "DUMMYSTOCK"
    risk_free_interest_rate = None
    volatility = None

    def _get_stock_prices():
        return np.array([1.0, 2.0, 3.0, 4.0, 3.0, 2.0, 1.0])

    mocker.patch("dashboard.engine.portfolio_objects.Stock._get_stock_prices", side_effect=_get_stock_prices)

    stock = Stock(root_path, lock, symbol, risk_free_interest_rate=risk_free_interest_rate, volatility=volatility)
    target_days = 1

    bs = BlackScholes(stock, target_days)

    stock_price = 1.0
    strike_price = 15.0

    gain = bs.call_solution(stock_price, strike_price)

    assert gain == pytest.approx(0.0)


def test_Portfolio__init__(mocker):
    root_path = os.path.abspath(os.path.dirname(__file__))
    lock = Lock()
    symbol1 = "DUMMYSTOCK1"
    symbol2 = "DUMMYSTOCK2"
    symbol3 = "DUMMYSTOCK3"
    risk_free_interest_rate = None
    volatility = None

    def _get_stock_prices():
        return np.array([1.0, 2.0, 3.0, 4.0, 3.0, 2.0, 1.0])

    mocker.patch("dashboard.engine.portfolio_objects.Stock._get_stock_prices", side_effect=_get_stock_prices)

    stock1 = Stock(root_path, lock, symbol1, risk_free_interest_rate=risk_free_interest_rate, volatility=volatility)
    stock2 = Stock(root_path, lock, symbol2, risk_free_interest_rate=risk_free_interest_rate, volatility=volatility)
    stock3 = Stock(root_path, lock, symbol3, risk_free_interest_rate=risk_free_interest_rate, volatility=volatility)

    stocks = [stock1, stock2, stock3]

    price_gain = 0.05
    portfolio = Portfolio(stocks, price_gain)

    assert portfolio.stocks == stocks
    assert portfolio.price_gain == price_gain


def test_check_stocks_for_sell(mocker):
    root_path = os.path.abspath(os.path.dirname(__file__))
    lock = Lock()
    symbol1 = "DUMMYSTOCK1"
    symbol2 = "DUMMYSTOCK2"
    symbol3 = "DUMMYSTOCK3"
    risk_free_interest_rate = None
    volatility = None

    def _get_stock_prices():
        return np.array([1.0, 2.0, 3.0, 4.0, 3.0, 2.0, 1.0])

    mocker.patch("dashboard.engine.portfolio_objects.Stock._get_stock_prices", side_effect=_get_stock_prices)

    stock1 = Stock(root_path, lock, symbol1, risk_free_interest_rate=risk_free_interest_rate, volatility=volatility)
    stock2 = Stock(root_path, lock, symbol2, risk_free_interest_rate=risk_free_interest_rate, volatility=volatility)
    stock3 = Stock(root_path, lock, symbol3, risk_free_interest_rate=risk_free_interest_rate, volatility=volatility)

    stocks = [stock1, stock2, stock3]

    price_gain = 0.05
    portfolio = Portfolio(stocks, price_gain)

    analysis_days = 1

    stocks_to_sell_dummy = ["DUMMYSTOCK1", "DUMMYSTOCK2", "DUMMYSTOCK3"]

    assert [stock.symbol for stock in portfolio.check_stocks_for_sell(analysis_days)] == stocks_to_sell_dummy
