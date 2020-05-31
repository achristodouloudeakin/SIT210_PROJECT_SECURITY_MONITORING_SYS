# Libraries Imported
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

from picamera import PiCamera
from datetime import datetime

import time
import sys
import requests
import _thread


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


camera_sys = PiCamera()


# Procedure to Notify Argon_AC_3 of movement detection at the Entryway
def argon_notification_procedure():
    print("Thread Starting for Argon_AC_3 Notification")
    timer_x = 0
    while timer_x < 10:
        # Secondary Client to communicate from RPi to Argon_AC_3
        secondary_client = mqtt.Client("Reception_2_mqtt")
        secondary_client.connect("test.mosquitto.org", 1883)
        secondary_client.subscribe("argon_Log_AC_3")
        secondary_client.publish("RPi_AC", "Active")
        print("Sending data to ARGON; Active; time:" + str(timer_x))
        time.sleep(1)
        timer_x += 1

    secondary_client = mqtt.Client("Reception_2_mqtt")
    secondary_client.connect("test.mosquitto.org", 1883)
    secondary_client.subscribe("argon_Log_AC_3")
    secondary_client.publish("RPi_AC", "Non_Active")
    print("Sending data to ARGON; Non_ACTIVE")

    secondary_client.unsubscribe("argon_Log_AC_3")

    print("Thread Exiting for Argon_AC_3 Notification")
    _thread.exit()


# Procedure to record Entryway after movement is detected
def camera_procedure():
    print("Thread Starting for Camera")
    print("Camera Starting")

    # Rotate Camera Imaging 180 Degrees
    camera_sys.rotation = 180

    # Pre-formate of Video File
    file_capture = "Entranceway Recording at " + time.strftime("%Y-%m-%d---%H-%M-%S") + ".h264"

    # Recording Entryway as a 7 Second Video
    camera_sys.start_recording(file_capture)
    time.sleep(7)
    camera_sys.stop_recording()

    print("Video Recorded")
    time.sleep(2)

    print("Notifying User of Front Door Movement and Camera Recording")
    requests.post("https://maker.ifttt.com/trigger/ARGON_AC_TEST_DETECTED_MOVEMENT/with/key/eU_JJJKmZOp_tczeQ56DCVRWKFmnvYPiAZ1fMz0oI6U")

    print("Thread Exiting for Camera")
    _thread.exit()


# Function which launches when a message is received from Argon_AC_Test (The Motion Sensor)
def message_function(client, userdata, message):
    # Decoding the Payload in the message
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    message.replace("argon_Log_AC_TEST", '')

    # Converting message into integer
    range_in_centimetres = int(message)

    # IF Statement that stops client loop and launches multiple threads if movement is detected
    if (range_in_centimetres < 100):
        print("Movement Detected at the Front Door")

        print("Stopping MQTT Connection Loop")
        client.loop_stop()

        # Thread 1: Camera Procedure
        _thread.start_new_thread(camera_procedure, ())

        # Thread 2: Argon Notification Procedure
        _thread.start_new_thread(argon_notification_procedure, ())


        print("Procedure Exited, Restarting MQTT Connection Loop")
        main()

    else:
        print("Doorway clear")


def main():
    try:
        # Primary Client Between Argon_AC_TEST and RPi
        primary_client = mqtt.Client("Reception_1_mqtt")
        primary_client.connect("test.mosquitto.org", 1883)
        primary_client.subscribe("argon_Log_AC_TEST")
        primary_client.on_message = message_function
        primary_client.loop_start()

        # while(1):
        # time.sleep(1)

    except:
        KeyboardInterrupt()


main()
