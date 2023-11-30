import datetime
import logging

import pytest

from dashboard.engine.finnhubwrapper import FinnhubWrapper


def test_FinnhubWrapper__init__():
    api_key = "Dummy_api_key"
    fw = FinnhubWrapper(api_key)

    assert fw.finnhub_client.API_URL == "https://api.finnhub.io/api/v1"


def test_to_timestamp_integer():
    api_key = "Dummy_api_key"
    fw = FinnhubWrapper(api_key)

    one_datetime = datetime.datetime(2012, 12, 12, 12, 12, 12)
    one_timestamp = fw.to_timestamp_integer(one_datetime)
    assert one_timestamp == 1355307132


def test_to_datetime():
    api_key = "Dummy_api_key"
    fw = FinnhubWrapper(api_key)

    one_timestamp = 1355307132
    one_datetime = fw.to_datetime(one_timestamp)
    assert one_datetime == datetime.datetime(2012, 12, 12, 12, 12, 12)


def test_stock_candles(caplog):
    caplog.set_level(logging.WARNING)
    stock_symbol = "DUMMY_STOCK"
    time_interval = 1
    start_date = datetime.datetime(2012, 12, 12, 12, 12, 12)
    end_date = datetime.datetime(2012, 12, 12, 12, 12, 12)

    api_key = "Dummy_api_key"
    fw = FinnhubWrapper(api_key)

    with pytest.raises(Exception):
        fw.stock_candles(stock_symbol, time_interval, start_date, end_date)

    assert "Invalid API key" in caplog.text


def test_company_news(caplog):
    stock_symbol = "DUMMY_STOCK"
    start_date = datetime.datetime(2012, 12, 12, 12, 12, 12)
    end_date = datetime.datetime(2012, 12, 12, 12, 12, 12)

    api_key = "Dummy_api_key"
    fw = FinnhubWrapper(api_key)

    with pytest.raises(Exception):
        fw.company_news(stock_symbol, start_date, end_date)
    assert "Invalid API key" in caplog.text


def test_market_news(caplog):
    stock_symbol = "DUMMY_STOCK"
    min_id = 0

    api_key = "Dummy_api_key"
    fw = FinnhubWrapper(api_key)

    with pytest.raises(Exception):
        fw.market_news(stock_symbol, min_id)
    assert "Invalid API key" in caplog.text


def test_company_profile(caplog):
    stock_symbol = "DUMMY_STOCK"

    api_key = "Dummy_api_key"
    fw = FinnhubWrapper(api_key)

    with pytest.raises(Exception):
        fw.company_profile(stock_symbol)
    assert "Invalid API key" in caplog.text


def test_stocks_to_list(caplog):
    api_key = "Dummy_api_key"
    fw = FinnhubWrapper(api_key)

    with pytest.raises(Exception):
        fw.stocks_to_list()
    assert "Invalid API key" in caplog.text
