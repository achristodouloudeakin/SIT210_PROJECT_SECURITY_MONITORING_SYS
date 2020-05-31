import paho.mqtt.client as mqtt

from datetime import datetime

import time
import sys
import requests
# import _thread

primary_client = mqtt.Client("makerio_mqtt")


def message_function(client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    message.replace("argon_Log_AC_TEST", '')

    range_in_centimetres = int(message)

    if (range_in_centimetres < 100):
        print("Someone has openned the door")
    else:
        print("Doorway clear")


def main():
    try:
        # Primary Client Between Argon_AC_TEST and RPi
        primary_client = mqtt.Client("makerio_mqtt")
        primary_client.connect("test.mosquitto.org", 1883)
        primary_client.subscribe("argon_Log_AC_TEST")
        primary_client.on_message = message_function
        primary_client.loop_forever()


    except:
        KeyboardInterrupt()


main()
