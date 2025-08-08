import psycopg2
from faker import Faker
from psycopg2 import sql
from tqdm import tqdm

db_params = {
    "dbname": "db",
    "user": "itiufscar",
    "password": "itiufscar",
    "host": "localhost",
    "port": 5432,
}

# Number of records to generate
NUM_USERS = 10000
NUM_ITEMS = 100000
NUM_INTERACTIONS = 1000000

fake = Faker()

conn = psycopg2.connect(**db_params)
cur = conn.cursor()


def create_tables():
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );
        CREATE TABLE IF NOT EXISTS items (
            item_id SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );
        CREATE TABLE IF NOT EXISTS interactions (
            interaction_id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(user_id),
            item_id INT REFERENCES items(item_id),
            rating INT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    )
    conn.commit()


def insert_fake_users(n):
    for _ in tqdm(range(n)):
        cur.execute(sql.SQL("INSERT INTO users (name) VALUES (%s)"), [fake.name()])
    conn.commit()


def insert_fake_items(n):
    for _ in tqdm(range(n)):
        cur.execute(sql.SQL("INSERT INTO items (name) VALUES (%s)"), [fake.word()])
    conn.commit()


def insert_fake_interactions(n):
    user_ids = [i + 1 for i in range(NUM_USERS)]
    item_ids = [i + 1 for i in range(NUM_ITEMS)]
    for _ in tqdm(range(n)):
        cur.execute(
            sql.SQL(
                "INSERT INTO interactions (user_id, item_id, rating) VALUES (%s, %s, %s)"
            ),
            [
                fake.random_element(user_ids),
                fake.random_element(item_ids),
                fake.random_int(min=1, max=5),
            ],
        )
    conn.commit()


# Main script
if __name__ == "__main__":
    create_tables()

    print(f"Inserting {NUM_USERS} fake users...")
    insert_fake_users(NUM_USERS)
    print(f"Inserting {NUM_ITEMS} fake items...")
    insert_fake_items(NUM_ITEMS)
    print(f"Inserting {NUM_INTERACTIONS} fake interactions...")
    insert_fake_interactions(NUM_INTERACTIONS)

    cur.close()
    conn.close()
    print("Data generation complete.")
