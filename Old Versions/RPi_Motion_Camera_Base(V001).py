import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

from picamera import PiCamera
from datetime import datetime

import time
import sys
import requests

ourClient = mqtt.Client("makerio_mqtt")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


camera_sys = PiCamera()
file_capture = "{0:%Y}-{0:%m}-{0:%d}".format(datetime.now()) + ".h264"
file_capture = time.strftime("%Y%m%d-%H%M%S")


def camera_procedure():
    print("Camera Starting")

    camera_sys.start_recording(file_capture)
    time.sleep(5)
    camera_sys.stop_recording()

    print("Video Recorded")
    time.sleep(2)



def message_function(client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    message.replace("argon_Log_AC_TEST", '')

    range_in_centimetres = int(message)

    if (range_in_centimetres < 100):
        print("Someone has openned the door")

        print("Stopping MQTT Connection Loop")
        client.loop_stop()

        camera_procedure()

        print("Notifying User")
        requests.post("https://maker.ifttt.com/trigger/ARGON_AC_TEST_DETECTED_MOVEMENT/with/key/eU_JJJKmZOp_tczeQ56DCVRWKFmnvYPiAZ1fMz0oI6U")

        

        print("Procedure Exited, Restarting MQTT Connection Loop")
        time.sleep(4)
        main()

    else:
        print("Doorway clear")


def main():
    try:
        ourClient = mqtt.Client("makerio_mqtt")
        ourClient.connect("test.mosquitto.org", 1883)
        ourClient.subscribe("argon_Log_AC_TEST")
        ourClient.on_message = message_function
        ourClient.loop_start()

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
