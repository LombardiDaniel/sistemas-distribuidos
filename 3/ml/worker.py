import io
import pickle

import minio
import pandas as pd
import pika
import psycopg2
from sklearn.linear_model import LinearRegression

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="recommendation_tasks")

client = minio.Minio(
    "localhost:9000", access_key="itiufscar", secret_key="itiufscar", secure=False
)

if not client.bucket_exists("models"):
    client.make_bucket("models")

conn = psycopg2.connect(
    dbname="db",
    user="itiufscar",
    password="itiufscar",
    host="localhost",
    port="5432",
)


def callback(ch, method, properties, body):
    print("msg rcvd")
    df = pd.read_sql("SELECT * FROM interactions", conn)

    x = df[["user_id", "item_id"]]
    y = df["rating"]

    model = LinearRegression()
    model.fit(x, y)

    # Save model to Minio
    serialized_model = pickle.dumps(model)
    model_data = io.BytesIO(serialized_model)
    client.put_object(
        "models", "interactions-reg-model.pkl", model_data, len(serialized_model)
    )
    print("Model saved to Minio")
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    channel.basic_consume(queue="recommendation_tasks", on_message_callback=callback)
    print("Waiting for messages...")
    channel.start_consuming()
