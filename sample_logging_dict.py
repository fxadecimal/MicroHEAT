"""

In this example, we will use the `SqliteDict` to store the sensor logs in a SQLite database.
It creates a KeyValue store on top of SQLite.
It hides much of the annoyance of working with databases, and it is a good choice for small projects.

SqliteDict automatically creates a table that looks like this:

```
CREATE TABLE IF NOT EXISTS "sensor_logs" (key TEXT PRIMARY KEY, value BLOB);
```

- Where "BLOB" is a binary field
- The "Key" must be unique, so here will use timestamp (epoch time)


"""

import os
import logging
import time
import requests
from sqlitedict import SqliteDict
import json
import csv

logging.basicConfig(level=logging.INFO)

API_URL = "http://localhost:8080"
DB_PATH = "dict.sqlite3"
SLEEP = 10
PATH_CSV = "sensor_logs.csv"


# We're overriding the encode and decode functions in SqliteDict to use json.dumps and json.loads instead of using the default "pickle" (binary) serialization.
sensor_logs_db = SqliteDict(
    DB_PATH, tablename="sensor_logs", encode=json.dumps, decode=json.loads
)


def dump_db_to_csv(db=sensor_logs_db, path=PATH_CSV):
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "sensor_1"])
        for key, dict_ in db.items():
            writer.writerow([key, *dict_.values()])  ## *values is list unpacking


if __name__ == "__main__":
    logging.info(f"Dumping database:{PATH_CSV}")
    dump_db_to_csv(db=sensor_logs_db, path=PATH_CSV)

    while True:
        logging.info("Fetching data from API: %s", API_URL)
        response = requests.get(f"{API_URL}/sensor")
        response.raise_for_status()
        response = response.json()
        value = response["value"]

        logging.info("Inserting data into database: %s", value)
        key = time.time()
        # write to the db
        sensor_logs_db[key] = {"sensor_1": value}
        # must commit the db
        sensor_logs_db.commit()

        logging.info("Sleeping..")
        time.sleep(SLEEP)
