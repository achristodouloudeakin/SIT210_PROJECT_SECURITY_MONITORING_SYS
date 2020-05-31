# Essentially, I want to send the word "Active" to my Argon

import paho.mqtt.client as mqtt
import time

# import time
# import sys
# import requests
# import _thread



# def message_function(client, userdata, message):
#     topic = str(message.topic)
#     message = str(message.payload.decode("utf-8"))
#     message.replace("argon_Log_AC_3", '')

#     print(message)

#     print("Publishing back to argon")
#     secondary_client.publish("Active")
#     print(secondary_client.publish("Active"))


# def main():
#     try:
#         secondary_client = mqtt.Client("makerio_mqtt")
#         secondary_client.connect("test.mosquitto.org", 1883)
#         secondary_client.subscribe("argon_Log_AC_3")
#         secondary_client.on_message = message_function
#         secondary_client.publish("Active")
#         secondary_client.loop_start()

#         while(1):
#             time.sleep(1)

#     except:
#         KeyboardInterrupt()

# main()

########################## OR THIS BELOW CODE? ##########################

# secondary_client = mqtt.Client("makerio_mqtt")
# secondary_client.connect("test.mosquitto.org", 1883)
# secondary_client.subscribe("argon_Log_AC_3")

# timer_x = 0
# while timer_x < 30:
#     secondary_client.publish("RPi_AC", "Active")
#     print("Sending data to ARGON; Active; time:" + str(timer_x))
#     time.sleep(1)
#     timer_x += 1

# print("Sending data to ARGON; NON_ACTIVE")
# secondary_client.publish("RPi_AC", "Non_Active")



timer_x = 0
while timer_x < 30:
    secondary_client = mqtt.Client("makerio_mqtt")
    secondary_client.connect("test.mosquitto.org", 1883)
    secondary_client.subscribe("argon_Log_AC_3")
    secondary_client.publish("RPi_AC", "Active")
    print("Sending data to ARGON; Active; time:" + str(timer_x))
    time.sleep(1)
    timer_x += 1

print("Sending data to ARGON; NON_ACTIVE")
secondary_client.publish("RPi_AC", "Non_Active")