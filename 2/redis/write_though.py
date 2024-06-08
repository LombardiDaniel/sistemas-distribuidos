"""
git clone https://github.com/lerocha/chinook-database
"""

import pickle
import time
from typing import Any

import psycopg2
import redis

CONN = psycopg2.connect(
    dbname="chinook",
    user="user",
    password="pass",
    host="localhost",
    port="5432",
)
CURSOR = CONN.cursor()

REDIS_CLIENT = redis.Redis()


def exec_sql(query: str) -> list[tuple[Any, ...]]:
    CURSOR.execute(query)

    CONN.commit()

    try:
        return CURSOR.fetchall()
    except Exception as err:
        print(err)
        return


def get_from_redis():
    raw_data = REDIS_CLIENT.get("sql:chinook:large-join")
    # return pickle.loads(raw_data)
    return raw_data


def save_to_redis(rows):
    REDIS_CLIENT.set(
        "sql:chinook:large-join",
        pickle.dumps(rows),
    )


def update(album_id, title):
    query = f"""
        UPDATE album 
        SET title = '{title}'
        WHERE album_id = {album_id};
    """

    REDIS_CLIENT.set(f"sql:album-title:{album_id}", title, ex=3600)

    # disparar a atualizacao assíncrona

    return 0


def main():
    update(5, "Big Ones")


if __name__ == "__main__":
    main()
