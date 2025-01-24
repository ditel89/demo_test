import paho.mqtt.client as mqtt
import time
import random  
import json
import serial

BROKER = "localhost" 
PORT = 1883
TOPIC = "test"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)
cnt = 0

def open_serial(device, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False):
    ss = serial.Serial()
    ss.port = device
    ss.baudrate = baudrate
    ss.bytesize = bytesize
    ss.parity = parity
    ss.stopbits = stopbits
    ss.timeout = timeout
    ss.xonxoff = xonxoff
    ss.rtscts = rtscts
    ss.dsrdtr = dsrdtr
    ss.open()
    return ss

def hmp155(cnt):

    global temp, humi
    
    if cnt == 0:
        cmd = "r\r\n"
        ser0.write(cmd.encode())
        line = ser0.readline().decode('ascii').strip()
        print("initial setting fot hmp155")
        cnt = 1
        time.sleep(5)

    line = ser0.readline().decode('ascii').strip()
    first = line.startswith("RH")

    if first == True:
        #"RH= 22.9 %RH T= 24.3 ‘C"
        # 데이터 파싱
        # if line.startswith("pw"):
        parts = line.split(' ')
        humi = float(parts[1])
        temp = float(parts[4][:4])

    ser0.close()
    return humi, temp, cnt

def pwd20():
    global vis_1, vis_10
    line = ser1.readline().decode('ascii').strip()
        
    if line:
        # PW  100   7147  7086
        # 데이터 파싱
        # if line.startswith("pw"):
        parts = line.split('  ')
        vis_1 =float(parts[2])        # 1 minute average visibility
        vis_10 = float(parts[3][:4])  # 10 minute average visibility

    ser0.close()
    return vis_1, vis_10

try:
    while True:
        temp, humi, vis_1, vis_10 = 0, 0, 0, 0
        ser0 = open_serial("/dev/ttyUSB0")
        humi, temp, cnt = hmp155(cnt)

        time.sleep(0.5)
        ser1 = open_serial("/dev/ttyUSB1")
        vis_1, vis_10 = pwd20()

        time.sleep(0.5)

        wind_speed = round(random.uniform(0, 15), 1) 
        wind_direction = round(random.uniform(0, 360), 1)
        # temp = round(random.uniform(-10, 30), 1) 
        # humi = round(random.uniform(0, 100), 1)
        # pwd = round(random.uniform(300, 1000), 0) 

        payload = {
            "wind_speed": wind_speed,
            "wind_direction": wind_direction,
            "temp": temp,
            "humi": humi,
            "pwd_1": vis_1,
            "pwd_10": vis_10
        }

        client.publish(TOPIC, json.dumps(payload))
        print(payload)

        time.sleep(5)  

except KeyboardInterrupt:
    print("MQTT STOP")
finally:
    client.disconnect()
