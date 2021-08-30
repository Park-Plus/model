import json
import requests
import config
import paho.mqtt.client as mqtt

zones = config.ZONES


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for zone in zones:
        client.subscribe("parks/" + zone + "/rec")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    dataJSON = json.loads(msg.payload)
    if dataJSON["type"] == "statusesRequest":
        for zone in zones:
            client.publish(
                "parks/" + zone + "/send",
                '{"type": "statusesRequest", "data": {"'
                + zone
                + '1": 0, "'
                + zone
                + '2": 0, "'
                + zone
                + '3": 0, "'
                + zone
                + '4": 0, "'
                + zone
                + '5": 0}}',
            )
    if dataJSON["type"] == "statusUpdate":
        data = dataJSON["data"]
        for park in data:
            url = config.BACKEND_ADDRESS + "/park/setStatus"
            requestObject = {"park_id": park["park"], "status": park["newStatus"]}
            requests.post(url, data=requestObject)
    if dataJSON["type"] == "endStay":
        plate = dataJSON["plate"]
        url = config.BACKEND_ADDRESS + "/park/stay/end"
        requestObject = {"plate": plate}
        r = requests.post(url, data=requestObject)
        print(r.text)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
