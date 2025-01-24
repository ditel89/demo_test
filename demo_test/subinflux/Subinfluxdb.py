
import json
import paho.mqtt.client as mqtt
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUXDB_TOKEN="5RyKd96YeJIKyBHO_pafqYVTuPY-q2ZP4-MwgD-o7Yq78lDJxBi1dUp26asX06cFZzguUHdIZIuKxxgpnugqoA=="

INFLUXDB_ORG = "keti"
INFLUXDB_URL = "http://10.252.218.220:8086"
INFLUXDB_BUCKET = "test_SensorData"

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "test"

influx_client = influxdb_client.InfluxDBClient(INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG)

write_api = influx_client.write_api(write_options=SYNCHRONOUS)
   
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(payload)

        point = Point("SensorData") \
            .tag("location", "lab") \
            .field("wind_speed", payload.get("wind_speed")) \
            .field("wind_direction", payload.get("wind_direction")) \
            .field("temp", payload.get("temp")) \
            .field("humi", payload.get("humi")) \
            .field("pwd_1", payload.get("pwd_1"))   \
            .field("pwd_10", payload.get("pwd_10")) 


        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG,record=point)
        time.sleep(1) 
        print("Data written to InfluxDB.")

    except Exception as e:
        print(f"Error : {e}") 

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.subscribe(MQTT_TOPIC)

print(f"Subscribed : {MQTT_TOPIC}")

try:
    mqtt_client.loop_forever()
except KeyboardInterrupt:
    print("Stopping MQTT client...")
    mqtt_client.disconnect()
    influx_client.close()
