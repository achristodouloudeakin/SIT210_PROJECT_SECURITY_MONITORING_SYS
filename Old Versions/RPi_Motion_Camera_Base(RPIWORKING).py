import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

from picamera import PiCamera
from datetime import datetime

import time
import sys


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


camera_sys = PiCamera()
file_capture = "{0:%Y}-{0:%m}-{0:%d}".format(datetime.now())


def camera_procedure():

    print("Beginning Procedure p2")
    
    print("Preview Start")
    ##camera_sys.start_preview()

    time.sleep(2)
    
    # PiCamera.capture('home/pi/photo1.png')
    
    time.sleep(2)
    
    ##camera_sys.stop_preview()  
    #print("Taking photo 1")
    #camera_sys.start_preview()
    #camera_sys.stop_preview()
    
    
    #time.sleep(2)
    #print("Taking photo 2")
    #camera_sys.capture('home/pi/photo2.png')

    print("Photos Taken, Exiting Proceedure")

    # x_cap = 0
    # while x_cap < 2:
    #     time.sleep(0.5)
    #     camera_sys.capture(file_capture)
    #     print("photo: " + str(x_cap))
    #     x_cap += 1

    # camera_sys.capture(file_capture)
    # camera_sys.close()

    # camera_sys.stop_preview()
    #print("resetting")
    #time.sleep(5)



def message_function(client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    message.replace("argonLog", '')

    range_in_centimetres = int(message)

    if (range_in_centimetres < 100):
        
        print("loop stopped")
        client.loop_stop()
        
        print("Someone has openned the door")

        print("Beginning Procedure p1")
        time.sleep(2)
        camera_procedure()

        print("Procedure Exited, resetting")

        time.sleep(5)
        
        print("loop starting")
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
