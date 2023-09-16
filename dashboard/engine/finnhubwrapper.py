import datetime
from typing import Union

import finnhub

from dashboard.settings import COMPANY_NEWS_DATE_FORMAT, SELECTED_COUNTRY


class FinnhubWrapper:
    def __init__(self, api_key: str):
        self.finnhub_client = finnhub.Client(api_key=api_key)

    def to_timestamp_integer(self, dt: datetime.datetime) -> int:
        return int(dt.timestamp())

    def to_datetime(self, timestamp: int) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(timestamp)

    def stock_candles(
        self, stock: str, time_interval: Union[int, str], start_date: datetime.datetime, end_date: datetime.datetime
    ) -> dict:
        start_date_int = self.to_timestamp_integer(start_date)
        end_date_int = self.to_timestamp_integer(end_date)
        return self.finnhub_client.stock_candles(stock, time_interval, start_date_int, end_date_int)

    def company_news(self, stock: str, start_date: datetime.datetime, end_date: datetime.datetime) -> dict:
        start_date_str = start_date.strftime(COMPANY_NEWS_DATE_FORMAT)
        end_date_str = end_date.strftime(COMPANY_NEWS_DATE_FORMAT)
        return self.finnhub_client.press_releases(stock, _from=start_date_str, to=end_date_str)

    def market_news(self, stock: str, min_id: int = 0) -> dict:
        return self.finnhub_client.general_news(stock, min_id=min_id)

    def company_profile(self, stock: str) -> dict:
        return self.finnhub_client.company_profile2(symbol=stock)

    def stocks_to_list(self) -> dict:
        return self.finnhub_client.stock_symbols(SELECTED_COUNTRY)
