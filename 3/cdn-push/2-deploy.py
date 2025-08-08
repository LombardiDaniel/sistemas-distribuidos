import io
import json
import sys
from pprint import pprint
from uuid import uuid4

import paho.mqtt.client as mqtt
import requests
from minio import Minio

TOPIC = "tgt:continents"
NEXT_TOPIC = ""
# NEXT_TOPIC = "from:{CONTINENT}"
CONTINENT = ""

minio_client = Minio(
    "localhost:9000",
    access_key="itiufscar",
    secret_key="itiufscar",
    secure=False,
)


def upload_code(bytes_obj: io.BytesIO) -> str:
    """uploads and returns signed-url"""
    print("uploading...")

    if not minio_client.bucket_exists(f"{CONTINENT}-code-uploads"):
        minio_client.make_bucket(f"{CONTINENT}-code-uploads")

    n_bytes = bytes_obj.getbuffer().nbytes
    bytes_obj.seek(0)
    minio_client.put_object(
        f"{CONTINENT}-code-uploads", f"code-{str(uuid4())}.bin", bytes_obj, n_bytes
    )
    bytes_obj.seek(0)
    minio_client.put_object(
        f"{CONTINENT}-code-uploads", "latest-code.bin", bytes_obj, n_bytes
    )
    print("...done!")

    return minio_client.get_presigned_url(
        "GET", f"{CONTINENT}-code-uploads", "latest-code.bin"
    )


def download(url):
    """
    Downloads a file from the given URL
    """
    response = requests.get(url, stream=True, timeout=30)

    lines = []
    if response.status_code == 200:
        for line in response.iter_lines():
            lines.append(line)

        return io.BytesIO(b"".join(lines))
    else:
        print("Failed to download file")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TOPIC)


def message_callback(client, userdata, msg):
    print("Mensagem recebida")
    conteudo_msg = msg.payload.decode()
    print(f"Topico: {msg.topic}")
    m = json.loads(conteudo_msg)
    pprint(m)
    exec_obj = download(m["new-code-url"])
    local_url = upload_code(exec_obj)
    client.publish(NEXT_TOPIC, json.dumps({"new-code-url": local_url}))


def main():

    global CONTINENT
    global NEXT_TOPIC
    if len(sys.argv) > 1:
        CONTINENT = sys.argv[1].lower()
        NEXT_TOPIC = f"from:{CONTINENT}"
    else:
        print("specify continent: python 2-deploy.py CONTINENT_NAME")
        return

    mqtt_client = mqtt.Client(str(uuid4()))
    mqtt_client.on_message = message_callback
    mqtt_client.on_connect = on_connect
    mqtt_client.connect("localhost", 1883)

    mqtt_client.loop_forever()


if __name__ == "__main__":
    main()
