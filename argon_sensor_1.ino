// Libraries
#include <MQTT.h>
#include <Grove-Ultrasonic-Ranger.h>


// Ultrasonic object constructor
Ultrasonic ultrasonic(D4);

// Callback (Unused as the Rpi won't be sending info back to Argon_AC_TEST)
MQTT client("test.mosquitto.org", 1883, callback);

void callback(char *topic, byte *payload, unsigned int length)
{
}

void setup()
{
    client.connect("argon_dev");

    // Begin serial communications
    Serial.begin(9600);
}

void loop()
{
    // Assign variable for the distance measurement
    long RangeInCentimeters;

    // Calculate the current distance value
    RangeInCentimeters = ultrasonic.MeasureInCentimeters();

    // // Set a small delay, so the sensor has some time to recalculate the distance
    // delay(1000);

    if (client.isConnected())
    {
        client.publish("argon_Log_AC_TEST", String(RangeInCentimeters));
        delay(1000);
    }

    client.loop();
}
