#!python3
# Covered under Presidio EULA
# import libraries
import paho.mqtt.client as mqtt
import time
import random

#define logging functions
def on_log(client, userdata, level, buffer):
        print("Loginfo: " + buffer)

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("Connected")
    else:
        print("Connection Failed with code` ", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected")

#create flag in class
mqtt.Client.connected_flag=False

# set broker address of hub
broker = "10.22.204.12"

# create object for broker connection
client = mqtt.Client("pythonSender", True)

# set blind callback deffinitions
client.on_connect = on_connect
client.on_disconnect = on_disconnect
# client.on_log = on_log

client.loop_start()
# establish connection to broker
client.connect(broker)
print ("Connecting to broker: ", broker)
while not client.connected_flag: #wait in loop
    print("In wait loop")
    time.sleep(1)
print("in Main Loop")


# create and publish some fake data
for i in range(250):
    for x in range(5):
        y = str(int(random.gauss(5000,100)))
        z = str(x + 1)
        sensor_string = "sensor" + z
        channel_string = "test/bw/" + sensor_string
        message_string = sensor_string + ":" + y
        print("bandwidth msg: " + message_string)
        client.publish(channel_string, message_string)
    time.sleep(5)
    for x in range(5):
        y = str(int(random.gauss(130,3)))
        z = str(x + 1)
        sensor_string = "sensor" + z
        channel_string = "test/heat/" + sensor_string
        message_string = sensor_string + ":" + y
        print("temperature msg: " + message_string)
        client.publish(channel_string, message_string)
    time.sleep(5)
    for x in range(5):
        y = str(int(random.gauss(120,3.5)))
        z = str(x + 1)
        sensor_string = "sensor" + z
        channel_string = "test/power/" + sensor_string
        message_string = sensor_string + ":" + y
        print("voltage msg: " + message_string)
        client.publish(channel_string, message_string)
    time.sleep(5)
# end loop

client.loop_stop()
client.disconnect()