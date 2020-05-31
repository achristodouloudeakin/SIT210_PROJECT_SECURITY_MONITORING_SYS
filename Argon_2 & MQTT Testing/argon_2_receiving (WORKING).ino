// This #include statement was automatically added by the Particle IDE.
#include <MQTT.h>
#include <Grove-Ultrasonic-Ranger.h>

// Callback (Unused as the Rpi won't be sending info the the Argon)
MQTT client("test.mosquitto.org", 1883, callback);


void callback(char* topic, byte* payload, unsigned int length) 
{
    String response;
    for (int i = 0; i < length; i++) 
    {
        response += (char)payload[i];
    }
    
    if (response.equals("Active"))
    {
        Particle.publish("Working, Received 'Active' ");
    }

    else if (response.equals("Non_Active"))
    {
        Particle.publish("Working, Received 'Non_Active' ");
    }
    
}

void setup()
{
    // client.connect("argon_dev_3");
    // client.subscribe("RPi_AC");
    
    client.connect("RPi_AC");
    // client.subscribe("RPi_AC");

    // Begin serial communications
    Serial.begin(9600);
}

void loop()
{
    if (client.isConnected())
    {
        // This demonstrates that the argon is connected to the Rpi, and is able to publish '1' successfully
        client.publish("argon_Log_AC_3", "Connected to Argon_AC_3");
        
        client.subscribe("RPi_AC");

        delay(1000);
    }

    client.loop();
}
