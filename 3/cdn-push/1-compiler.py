import io
import json
from time import sleep
from uuid import uuid4

import paho.mqtt.client as mqtt
import pika
from minio import Minio

minio_client = Minio(
    "localhost:9000",
    access_key="itiufscar",
    secret_key="itiufscar",
    secure=False,
)

mqtt_client = mqtt.Client(str(uuid4()))
mqtt_client.username_pw_set("itiufscar", "itiufscar")
mqtt_client.connect("localhost", 1883)

parameters = pika.ConnectionParameters(
    "localhost",
    5672,
    "/",
    pika.PlainCredentials("itiufscar", "itiufscar"),
)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

queue_name = "compile.queue"
channel.queue_declare(queue=queue_name)


def upload_code(bytes_obj: io.BytesIO) -> str:
    """uploads and returns signed-url"""
    print("uploading...")

    if not minio_client.bucket_exists("global-code-uploads"):
        minio_client.make_bucket("global-code-uploads")

    n_bytes = bytes_obj.getbuffer().nbytes
    bytes_obj.seek(0)
    minio_client.put_object(
        "global-code-uploads", f"code-{str(uuid4())}.bin", bytes_obj, n_bytes
    )
    bytes_obj.seek(0)
    minio_client.put_object(
        "global-code-uploads", "latest-code.bin", bytes_obj, n_bytes
    )
    print("...done!")

    return minio_client.get_presigned_url(
        "GET", "global-code-uploads", "latest-code.bin"
    )


def notify(signed_url: str):
    """notify"""
    mqtt_client.publish(
        "tgt:continents",
        json.dumps(
            {
                "new-code-url": signed_url,
            }
        ),
    )


def compile_code(repo: str, branch: str) -> io.BytesIO:
    """
    compiles code. i.e.:
    # git pull
    # make compile
    # push exec
    """
    print("comipiling...")

    sleep(5)

    bytes_io = io.BytesIO()
    bytes_io.write(f"compiled code from: {repo}:{branch}".encode())
    print("...done!")
    return bytes_io


def callback(ch, method, properties, body):
    """
    msg callback -> expecting:
        {
            "msgId": str(uuid4()),
            "repo": "my-example-repository",
            "branch": "prod",
        }
    """
    print(f" [x] Received {body}")
    msg = json.loads(body)

    # compile
    code_io = compile_code(msg["repo"], msg["branch"])

    # upload
    signed_url = upload_code(code_io)

    # notify
    notify(signed_url)

    # ack msg
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    """main"""

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=False
    )
    channel.start_consuming()


if __name__ == "__main__":
    main()
