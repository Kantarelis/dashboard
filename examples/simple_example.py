import os
import sys

sys.path.insert(0, os.getcwd())
from dashboard import Dashboard

if __name__ == "__main__":
    Dashboard().run()
