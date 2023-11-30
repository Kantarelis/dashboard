import os
from multiprocessing.synchronize import Lock as LockType

import dash

from dashboard.run import Dashboard


def test_Dashboard__init__():
    dashboard = Dashboard()

    assert dashboard.app_title == "Dashboard"
    assert type(dashboard.app) is dash.Dash
    assert dashboard.root_path == os.getcwd()
    assert type(dashboard.lock) is LockType
