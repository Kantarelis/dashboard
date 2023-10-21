import logging
import sqlite3
from sqlite3 import Error


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
