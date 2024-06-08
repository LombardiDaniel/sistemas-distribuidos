import random
import string

import psycopg2

# PostgreSQL connection parameters
pg_conn_params = {
    "dbname": "chinook",
    "user": "user",
    "password": "pass",
    "host": "localhost",
    "port": 5432,
}


# Function to connect to PostgreSQL
def get_pg_connection():
    return psycopg2.connect(**pg_conn_params)


# Function to fetch data from a table
def fetch_data(conn, table):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table}")
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return columns, rows


# Function to insert data into a table
def insert_data(conn, table, columns, rows):
    with conn.cursor() as cursor:
        for row in rows:
            placeholders = ", ".join(["%s"] * len(row))
            columns_list = ", ".join(columns)
            sql = f"INSERT INTO {table} ({columns_list}) VALUES ({placeholders})"
            cursor.execute(sql, row)
    conn.commit()


# Function to generate a new unique ID
def generate_new_id(existing_ids):
    while True:
        new_id = max(existing_ids) + 1
        if new_id not in existing_ids:
            existing_ids.add(new_id)
            return new_id


# Function to duplicate data
def duplicate_data(conn, table, key_column, multiplier):
    columns, rows = fetch_data(conn, table)
    existing_ids = {row[columns.index(key_column)] for row in rows}

    new_rows = []
    for i in range(multiplier - 1):
        for row in rows:
            new_row = list(row)
            new_row[columns.index(key_column)] = generate_new_id(existing_ids)
            new_rows.append(new_row)

    insert_data(conn, table, columns, new_rows)


# Main function
def main():
    conn = get_pg_connection()
    tables_to_duplicate = [
        ("Artist", "artist_id"),
        ("Album", "album_id"),
        ("Track", "track_id"),
        ("Genre", "genre_id"),
        ("Customer", "customer_id"),
        ("Invoice", "invoice_id"),
        ("Invoice_Line", "invoice_line_id"),
        ("Employee", "employee_id"),
        ("Media_Type", "media_type_id"),
        ("playlist", "playlist_id"),
        ("track", "track_id"),
    ]
    multiplier = 2  # Number of times to duplicate the data

    try:
        for table, key_column in tables_to_duplicate:
            print(f"Duplicating data in {table}...")
            duplicate_data(conn, table, key_column, multiplier)
        print("Data duplication complete.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
