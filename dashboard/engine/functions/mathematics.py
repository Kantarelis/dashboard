import logging

import numpy as np

from dashboard.engine.settings import STD_SMALL_RANGE


def std_calculator(prices: np.ndarray) -> np.ndarray:
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
