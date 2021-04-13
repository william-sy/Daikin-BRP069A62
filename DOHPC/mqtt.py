# This file for now is a standalone script, will be tied in later
#def startMQTT(daikinMqttBroker, daikinMqttName, daikinMqttPublishTimeOut):
#    pass


import paho.mqtt.client as mqtt
import time, os, sys

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe([("DHPW/state",0),("DHPW/temp",0)])
    client.connected_flag=True

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    print("message topic=",message.topic)
    print("message received " ,str(message.payload.decode("utf-8")))
    # depending on the message, take a action

exit_file = "/exit"
client = mqtt.Client("DHPW")
client.connected_flag=False
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", port=1883, keepalive=60)

# Start the loop, and wait for a connection
client.loop_start()
while client.connected_flag == False:
    print("We are not yet connected, please hold!")
    time.sleep(2)

# Here we enter a while loop that can be terminated with a new file or a key stroke.
try:
    while not os.path.exists(exit_file):
        print("Staring MQTT process")
        print("Publish latest data")
        time.sleep(2)
        client.publish("DHPW/state","OFF")
        client.publish("DHPW/temp",21)
        time.sleep(5)

except KeyboardInterrupt:
    print(" I was brutally interrupted, tis but a scratch!")

# We reached the end, we can stop the loop
client.loop_stop()
