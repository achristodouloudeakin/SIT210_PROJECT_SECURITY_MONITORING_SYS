// This #include statement was automatically added by the Particle IDE.
#include <MQTT.h>
#include <Grove-Ultrasonic-Ranger.h>

void callback(char* topic, byte* payload, unsigned int length);

/**
 * if want to use IP address,
 * byte server[] = { XXX,XXX,XXX,XXX };
 * MQTT client(server, 1883, callback);
 * want to use domain name,
 * exp) iot.eclipse.org is Eclipse Open MQTT Broker: https://iot.eclipse.org/getting-started
 * MQTT client("iot.eclipse.org", 1883, callback);
 **/
MQTT client("test.mosquitto.org", 1883, callback);

// recieve message
void callback(char* topic, byte* payload, unsigned int length) 
{
    char p[length + 1];
    memcpy(p, payload, length);
    p[length] = NULL;

    Serial.print( "Got a message : " );
    Particle.publish(p, PUBLIC);
}


void setup() 
{
    // connect to the server
    client.connect("makerio_mqtt");

    // publish/subscribe
    if (client.isConnected()) 
    {
        Serial.print("\nConnected");
        // client.publish("outTopic/message","hello world");
        client.subscribe("Rpi_AC");
        client.onmessage() = callback;
    }
}

void loop() 
{
    if (client.isConnected())
        client.loop();
}