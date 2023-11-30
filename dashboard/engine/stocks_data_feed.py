import datetime
from multiprocessing import Process
from multiprocessing.synchronize import Lock as LockType

from dashboard.database.functions.generic import get_api_key, run_query
from dashboard.engine.finnhubwrapper import FinnhubWrapper
from dashboard.settings import DATA_FEED_WINDOW, DATABASE_PATH, TIME_INTERVAL

CREATION_QUERY = """
                 CREATE TABLE IF NOT EXISTS saved_stocks
                 ([pid] INTEGER PRIMARY KEY AUTOINCREMENT, [symbol] TEXT UNIQUE NOT NULL, [name] TEXT, [country] TEXT,
                 [currency] TEXT, [estimateCurrency]  TEXT, [exchange] TEXT, [finnhubIndustry] TEXT, [ipo] TEXT,
                 [logo] TEXT, [marketCapitalization] TEXT, [phone] TEXT, [shareOutstanding] TEXT, [ticker] TEXT,
                 [weburl] TEXT)
                 """

CREATION_STOCKS_DATA_FEED_QUERY = """
                 CREATE TABLE IF NOT EXISTS stocks_data_feed
                 ([timestamp] INTEGER PRIMARY KEY, [pid] INTEGER, [symbol] TEXT, [close] FLOAT,
                 [high] FLOAT, [low] FLOAT, [open] FLOAT, [status] TEXT, [volume] INTEGER)
                 """

SELECT_SAVED_STOCKS = """
                    SELECT symbol, pid FROM saved_stocks
                    """


class StocksDataFeed(Process):
    fin: FinnhubWrapper
    loop: bool

    def __init__(self, lock: LockType, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = lock
        self.loop = True

    def run(self):
        self.fin = FinnhubWrapper(get_api_key())

        while self.loop:
            start_date = datetime.datetime.now() - datetime.timedelta(days=DATA_FEED_WINDOW)
            end_date = datetime.datetime.now()

            with self.lock:
                run_query(CREATION_QUERY, DATABASE_PATH)
                results = run_query(SELECT_SAVED_STOCKS, DATABASE_PATH)

            stocks = [result[0] for result in results]
            pids = [result[1] for result in results]

            for stock, pid in zip(stocks, pids):
                stock_candle = self.fin.stock_candles(stock, TIME_INTERVAL, start_date, end_date)
                if stock_candle["s"] == "ok":
                    for record in range(len(stock_candle["c"])):
                        stock_data = (
                            f"('{stock_candle['t'][record]}', '{pid}', '{stock}', '{stock_candle['c'][record]}', "
                        )
                        stock_data += f"'{stock_candle['h'][record]}', '{stock_candle['l'][record]}', "
                        stock_data += f"'{stock_candle['o'][record]}', '{stock_candle['s']}', "
                        stock_data += f"'{stock_candle['v'][record]}')"
                        insert_stock_data_feed = f"""
                                    INSERT INTO stocks_data_feed (timestamp, pid, symbol, close, high, low, open,
                                    status, volume)
                                    VALUES {stock_data}
                                    ON CONFLICT (timestamp) DO NOTHING;
                                    """

                        with self.lock:
                            run_query(CREATION_STOCKS_DATA_FEED_QUERY, DATABASE_PATH)
                            run_query(insert_stock_data_feed, DATABASE_PATH)

                    start_date_to_string = int(start_date.timestamp())
                    delete_out_dated_data_feed = f"""
                                DELETE FROM stocks_data_feed
                                WHERE timestamp < {start_date_to_string};
                                """
                    with self.lock:
                        run_query(CREATION_STOCKS_DATA_FEED_QUERY, DATABASE_PATH)
                        run_query(delete_out_dated_data_feed, DATABASE_PATH)
