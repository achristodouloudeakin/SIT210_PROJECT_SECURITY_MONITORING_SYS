// This #include statement was automatically added by the Particle IDE.
#include <MQTT.h>
#include <Grove-Ultrasonic-Ranger.h>

// Ultrasonic object constructor
Ultrasonic ultrasonic(D4);


MQTT client("test.mosquitto.org", 1883, callback);

void callback(char *topic, byte *payload, unsigned int length)
{
    String response;
    for (int i = 0; i < length; i++)
    {
        response += (char)payload[i];
    }

    // Assign variable for the distance measurement
    long RangeInCentimeters;

    // Calculate the current distance value
    RangeInCentimeters = ultrasonic.MeasureInCentimeters();

    if (response.equals("Active") and RangeInCentimeters < 100)
    {
        // Particle.publish("Working, Received 'Active' AND Distance Bellow 100 ");
        Particle.publish("MONITORING_STATUS", "INTRUSION");
    }

    else if (response.equals("Non_Active") and RangeInCentimeters < 100)
    {
        // Particle.publish("Working, Received 'Non_Active' ");
        Particle.publish("SOFT_MONITORING_STATUS", "SOFT_INTRUSION");
    }
}

void setup()
{
    client.connect("RPi_AC");

    // Begin serial communications
    Serial.begin(9600);
}

void loop()
{
    if (client.isConnected())
    {
        client.subscribe("RPi_AC");

        // Assign variable for the distance measurement
        long RangeInCentimeters;

        // Calculate the current distance value
        RangeInCentimeters = ultrasonic.MeasureInCentimeters();

        if (RangeInCentimeters < 100)
        {
            Particle.publish("SOFT_MONITORING_STATUS", "SOFT_INTRUSION");
        }

        delay(1000);
    }

    client.loop();
}
