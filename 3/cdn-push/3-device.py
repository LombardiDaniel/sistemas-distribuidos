import json
import sys
from pprint import pprint
from uuid import uuid4

import paho.mqtt.client as mqtt
import requests

# TOPIC = "from:{CONTINENT}"
TOPIC = ""
CONTINENT = ""


def download_and_print(url):
    """
    Downloads a file from the given URL and prints its contents to stdout.
    """
    response = requests.get(url, stream=True, timeout=30)

    if response.status_code == 200:
        for line in response.iter_lines():
            decoded_line = line.decode("utf-8")
            print(decoded_line)
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
    print("\n\n")
    download_and_print(m["new-code-url"])
    print("\n\n")


def main():

    global CONTINENT
    global TOPIC
    if len(sys.argv) > 1:
        CONTINENT = sys.argv[1].lower()
        TOPIC = f"from:{CONTINENT}"
    else:
        print("specify continent: python 3-device.py CONTINENT_NAME")
        return

    mqtt_client = mqtt.Client(str(uuid4()))
    mqtt_client.on_message = message_callback
    mqtt_client.on_connect = on_connect
    mqtt_client.connect("localhost", 1883)

    mqtt_client.loop_forever()


if __name__ == "__main__":
    main()
