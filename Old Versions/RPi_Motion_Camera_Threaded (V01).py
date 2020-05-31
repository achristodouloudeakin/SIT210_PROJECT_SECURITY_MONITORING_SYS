import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

from picamera import PiCamera
from datetime import datetime

import time
import sys
import requests
import _thread

primary_client = mqtt.Client("makerio_mqtt")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


camera_sys = PiCamera()


def argon_notification_procedure():
    timer_x = 0
    while timer_x < 30:
        secondary_client = mqtt.Client("makerio_mqtt")
        secondary_client.connect("test.mosquitto.org", 1883)
        secondary_client.subscribe("argon_Log_AC_3")
        secondary_client.publish("RPi_AC", "Active")
        print("Sending data to ARGON; Active; time:" + str(timer_x))
        time.sleep(1)
        timer_x += 1

    secondary_client = mqtt.Client("makerio_mqtt")
    secondary_client.connect("test.mosquitto.org", 1883)
    secondary_client.subscribe("argon_Log_AC_3")
    secondary_client.publish("RPi_AC", "Non_Active")
    print("Sending data to ARGON; Non_ACTIVE")

    _thread.exit()


def camera_procedure():
    print("Thread Starting for Camera")
    print("Camera Starting")

    #Rotate Camera Imaging
    camera_sys.rotation(180)

    file_capture = "Entranceway Recording at " + \
        time.strftime("%Y-%m-%d---%H-%M-%S") + ".h264"

    camera_sys.start_recording(file_capture)
    time.sleep(7)
    camera_sys.stop_recording()

    print("Video Recorded")
    time.sleep(2)

    print("Thread Exiting for Camera")
    _thread.exit()


def message_function(client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    message.replace("argon_Log_AC_TEST", '')

    range_in_centimetres = int(message)

    if (range_in_centimetres < 100):
        print("Someone has openned the door")

        print("Stopping MQTT Connection Loop")
        client.loop_stop()

        # camera_procedure()

        _thread.start_new_thread(camera_procedure, ())
        _thread.start_new_thread(argon_notification_procedure, ())

        print("Notifying User")
        requests.post("https://maker.ifttt.com/trigger/ARGON_AC_TEST_DETECTED_MOVEMENT/with/key/eU_JJJKmZOp_tczeQ56DCVRWKFmnvYPiAZ1fMz0oI6U")

        print("Procedure Exited, Restarting MQTT Connection Loop")
        time.sleep(4)
        main()

    else:
        print("Doorway clear")


def main():
    try:
        # Primary Client Between Argon_AC_TEST and RPi
        primary_client = mqtt.Client("makerio_mqtt")
        primary_client.connect("test.mosquitto.org", 1883)
        primary_client.subscribe("argon_Log_AC_TEST")
        primary_client.on_message = message_function
        primary_client.loop_start()

        while(1):
            time.sleep(1)

    except:
        KeyboardInterrupt()


main()


# Photo Stuff #
# x_cap = 0
# while x_cap < 2:
#     time.sleep(0.5)
#     camera_sys.capture(file_capture)
#     print("photo: " + str(x_cap))
#     x_cap += 1

# camera_sys.capture(file_capture)
# camera_sys.close()

# camera_sys.stop_preview()
