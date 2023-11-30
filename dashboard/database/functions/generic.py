import logging
import os
import sqlite3
from sqlite3 import Error
from typing import Optional

from dotenv import load_dotenv


def configure_environment() -> None:
    load_dotenv()


def get_api_key(api_key: Optional[str] = None) -> str:
    if api_key is None:
        api_key = os.getenv("API_KEY")
    if api_key is None:
        error_message: str = "API_KEY is not setup in the running environment neither provided by the user. Please "
        error_message += "check README.md to see how to setup API_KEY in you environment."
        raise Exception(error_message)
    return api_key


def create_connection(db_file: str) -> None:
    """create a database connection to a SQLite database"""
    logging.debug("Trying to connect to database")
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logging.debug(f"Connection succeed with: {sqlite3.version}")
    except Error as error:
        logging.error(f"Error while trying to connect with database: {error}")
    finally:
        if conn:
            conn.close()
            logging.debug("Connection succeed and closing.")


def run_query(query: str, database_file: str) -> list:
    """Run query and fetch results"""
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    results = cursor.fetchall()
    return results
