import json
from uuid import uuid4

import paho.mqtt.client as mqtt

TOPIC = "/payments/credit-cards/brasil/fraudulent"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TOPIC)


def message_callback(client, userdata, msg):
    print("Mensagem recebida")
    conteudo_msg = msg.payload.decode()
    print(f"Topico: {msg.topic}")
    m = json.loads(conteudo_msg)
    print(f"Conteudo: {m}")
    print(f"ID: {m['id']}")
    return


def main():
    mqtt_client = mqtt.Client(str(uuid4()))
    mqtt_client.on_message = message_callback
    mqtt_client.on_connect = on_connect
    mqtt_client.username_pw_set("ufscar", "iti")
    mqtt_client.connect("localhost", 1883)

    mqtt_client.loop_forever()


if __name__ == "__main__":
    main()
