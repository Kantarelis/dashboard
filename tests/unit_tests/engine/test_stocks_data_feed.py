from multiprocessing import Lock

from dashboard.engine.stocks_data_feed import StocksDataFeed


def tests_StocksDataFeed__init__():
    lock = Lock()
    sdf = StocksDataFeed(lock)

    assert sdf.lock == lock
    assert sdf.loop is True
