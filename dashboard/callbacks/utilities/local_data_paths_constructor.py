import os

from dashboard.settings import DATABASE_PATH


def local_data_paths_constructor(root_path):
    database_path = os.path.join(root_path, DATABASE_PATH)

    if not os.path.exists(database_path):
        os.makedirs(database_path)
