import datetime
import logging
from typing import Union

import finnhub

from dashboard.settings import COMPANY_NEWS_DATE_FORMAT, SELECTED_COUNTRY


class FinnhubWrapper:
    finnhub_client: finnhub.Client

    def __init__(self, api_key: str):
        self.finnhub_client = finnhub.Client(api_key=api_key)

    def to_timestamp_integer(self, dt: datetime.datetime) -> int:
        return int(dt.timestamp())

    def to_datetime(self, timestamp: int) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(timestamp)

    def stock_candles(
        self,
        stock_symbol: str,
        time_interval: Union[int, str],
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> dict:
        start_date_int = self.to_timestamp_integer(start_date)
        end_date_int = self.to_timestamp_integer(end_date)

        try:
            results = self.finnhub_client.stock_candles(stock_symbol, time_interval, start_date_int, end_date_int)
        except Exception as exc:
            logging.error(exc)
            raise Exception(exc)
        return results

    def company_news(self, stock_symbol: str, start_date: datetime.datetime, end_date: datetime.datetime) -> dict:
        start_date_str = start_date.strftime(COMPANY_NEWS_DATE_FORMAT)
        end_date_str = end_date.strftime(COMPANY_NEWS_DATE_FORMAT)

        try:
            company_news = self.finnhub_client.press_releases(stock_symbol, _from=start_date_str, to=end_date_str)
        except Exception as exc:
            logging.error(exc)
            raise Exception(exc)
        return company_news

    def market_news(self, stock_symbol: str, min_id: int = 0) -> dict:
        try:
            news = self.finnhub_client.general_news(stock_symbol, min_id=min_id)
        except Exception as exc:
            logging.error(exc)
            raise Exception(exc)
        return news

    def company_profile(self, stock_symbol: str) -> dict:
        try:
            profile = self.finnhub_client.company_profile2(symbol=stock_symbol)
        except Exception as exc:
            logging.error(exc)
            raise Exception(exc)
        return profile

    def stocks_to_list(self) -> dict:
        try:
            stocks_list = self.finnhub_client.stock_symbols(SELECTED_COUNTRY)
        except Exception as exc:
            logging.error(exc)
            raise Exception(exc)
        return stocks_list
