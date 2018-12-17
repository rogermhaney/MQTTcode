#!python3
# Covered under Presidio EULA
# import libraries
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import datetime

# define InfluxDB message
def persists_pwr(sensor_name, volts):
    current_time = datetime.datetime.utcnow().isoformat()
    json_body = [
        {
            "measurement": "voltage",
            "tags": {
                "sensor": sensor_name
            },
            "time": current_time,
            "fields": {
                "value": int(volts)
            }
        }
    ]
    print(json_body)
    influx_client.write_points(json_body)

def persists_heat(sensor_name, temp):
    current_time = datetime.datetime.utcnow().isoformat()
    json_body = [
        {
            "measurement": "temperature",
            "tags": {
                "sensor": sensor_name
            },
            "time": current_time,
            "fields": {
                "value": int(temp)
            }
        }
    ]
    print(json_body)
    influx_client.write_points(json_body)

def persists_bw(sensor_name, bw):
    current_time = datetime.datetime.utcnow().isoformat()
    json_body = [
        {
            "measurement": "bandwidth",
            "tags": {
                "sensor": sensor_name
            },
            "time": current_time,
            "fields": {
                "value": int(bw)
            }
        }
    ]
    print(json_body)
    influx_client.write_points(json_body)


#define logging functions
def on_log(client, userdata, level, buffer):
    print("Loginfo: " + buffer)

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected")
    else:
        print("Connection Failed with code ", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected")

def on_message(client, userdata, msg):
    get_topic = msg.topic
    print(get_topic)
    if "heat" in get_topic:
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        sensor_name = m_decode[:7]
        temp = m_decode[-3:]
        persists_heat(sensor_name, temp)
        print("Sensor: " + sensor_name + " with temperature " + temp)
    if "power" in get_topic:
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        sensor_name = m_decode[:7]
        volts = m_decode[-3:]
        persists_pwr(sensor_name, volts)
        print("Sensor: " + sensor_name + " with voltage " + volts)
    if "bw" in get_topic:
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        sensor_name = m_decode[:7]
        bw = m_decode[-4:]
        persists_bw(sensor_name, bw)
        print("Sensor: " + sensor_name + " with bandwidth " + bw)

# set broker address of hub
broker = "10.22.204.12"

# set InfluxDB client
influx_client = InfluxDBClient('10.22.204.10', 8086, database='iot')

# create object for broker connection
client = mqtt.Client("pythonSubscriber", False)

# set blind callback deffinitions
client.on_connect = on_connect
client.on_disconnect = on_disconnect
# client.on_log = on_log
client.on_message = on_message

# establish connection to broker
client.connect(broker)
print ("Connecting to broker ", broker)
client.subscribe("test/#")
client.loop_forever()