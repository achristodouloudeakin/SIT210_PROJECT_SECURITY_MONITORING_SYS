import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

from picamera import PiCamera
from datetime import datetime

import time
import sys

ourClient = mqtt.Client("makerio_mqtt")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


camera_sys = PiCamera()
file_capture = "{0:%Y}-{0:%m}-{0:%d}-{0:H}-{0:&M}-{0:S}".format(datetime.now()) + ".h264"


def camera_procedure():
    print("Camera Starting")

    #camera_sys.start_preview()
    #camera_sys.start_recording('intruder.h264')
    camera_sys.start_recording(file_capture)
    
    time.sleep(4)
    
    camera_sys.stop_recording()
    #camera_sys.stop_preview()

    print("Photos Taken")
    time.sleep(2)



def message_function(client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    message.replace("argonLog", '')

    range_in_centimetres = int(message)
    print(range_in_centimetres)

    if (range_in_centimetres < 100):
        print("Someone has openned the door")

        print("Stopping MQTT Connection Loop")
        client.loop_stop()

        camera_procedure()

        print("Procedure Exited, Restarting MQTT Connection Loop")
        time.sleep(4)
        main()

    else:
        print("Doorway clear")


def main():
    try:
        ourClient = mqtt.Client("makerio_mqtt")
        ourClient.connect("test.mosquitto.org", 1883)
        ourClient.subscribe("argonLog")
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
