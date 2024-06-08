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

    return CURSOR.fetchall()


def get_from_redis():
    raw_data = REDIS_CLIENT.get("sql:chinook:large-join")
    # return pickle.loads(raw_data)
    return raw_data


def save_to_redis(rows):
    REDIS_CLIENT.set(
        "sql:chinook:large-join",
        pickle.dumps(rows),
    )


def get_from_sql():
    rows = exec_sql(
        """
        SELECT
            t.Name AS TrackName,
            a.Title AS AlbumTitle,
            ar.Name AS ArtistName,
            g.Name AS GenreName,
            il.Unit_Price AS Unit_Price,
            il.Quantity AS Quantity,
            c.First_Name || ' ' || c.Last_Name AS CustomerName,
            i.Invoice_Date AS Purchase_Date,
            e.First_Name || ' ' || e.Last_Name AS SalesAgent
        FROM
            Track t
            JOIN Album a ON t.Album_Id = a.Album_Id
            JOIN Artist ar ON a.Artist_Id = ar.Artist_Id
            JOIN Genre g ON t.Genre_Id = g.Genre_Id
            JOIN Invoice_Line il ON t.Track_Id = il.Track_Id
            JOIN Invoice i ON il.Invoice_Id = i.Invoice_Id
            JOIN Customer c ON i.Customer_Id = c.Customer_Id
            JOIN Employee e ON c.Support_Rep_Id = e.Employee_Id
        """
    )
    return rows


def main():
    start = time.perf_counter()
    rows = get_from_sql()
    end = time.perf_counter()
    delta = end - start
    print(f"SQL took: {delta:.2f}s")

    save_to_redis(rows)

    start = time.perf_counter()
    rows = get_from_redis()
    end = time.perf_counter()
    delta = end - start
    print(f"REDIS took: {delta:.2f}s")
    data = pickle.loads(rows)


if __name__ == "__main__":
    main()
