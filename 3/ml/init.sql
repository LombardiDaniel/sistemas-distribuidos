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
