import sqlite3
import logging
import time
import requests

DB_PATH = "db.sqlite3"
API_URL = "http://localhost:8080/sensor"
SLEEP = 10

logging.basicConfig(level=logging.INFO)


def init_db(path=DB_PATH):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS sensor_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL DEFAULT (strftime('%s', 'now')),
            value REAL
        )
    """
    )
    conn.commit()
    conn.close()


def insert_data(value, path=DB_PATH):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("INSERT INTO sensor_log (value) VALUES (?)", (value,))
    conn.commit()
    conn.close()


def dump_data(path=DB_PATH):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("SELECT * FROM sensor_log")
    rows = c.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    logging.info("Initializing database: %s", DB_PATH)
    init_db()
    while True:
        logging.info("Fetching data from API: %s", API_URL)
        response = requests.get(API_URL)
        response.raise_for_status()
        response = response.json()
        value = response["value"]

        logging.info("Inserting data into database: %s", value)
        insert_data(value)
        logging.info("Sleeping..")
        time.sleep(SLEEP)
