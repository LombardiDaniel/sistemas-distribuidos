import json
from uuid import uuid4

import paho.mqtt.client as mqtt

TOPIC = "/payments/credit-cards/brasil/fraudulent"


def main():
    mqtt_client = mqtt.Client(str(uuid4()))
    mqtt_client.username_pw_set("ufscar", "iti")
    mqtt_client.connect("localhost", 1883)

    msg = json.dumps(
        {
            "id_sender": "9991238778018",
            "valor": 88.99,
            "fraud": True,
            "id_reciever": "88192773122204",
            "ts": "2006-01-02T15:04:05Z07:00",
            "id": str(uuid4()),
        }
    )
    mqtt_client.publish(TOPIC, msg)


if __name__ == "__main__":
    main()
