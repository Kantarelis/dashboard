import numpy as np
import pytest

from dashboard.engine.functions.mathematics import std_calculator


def test_std_calculator():
    prices = np.array([1.0, 2.0, 3.0, 4.0, 3.0, 2.0, 1.0])
    result = std_calculator(prices)
    assert result == pytest.approx(0.3617496501604271)
