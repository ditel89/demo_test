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

def is_number_string(s):
    try:
        float(s)  # 숫자로 변환 시도
        return True
    except ValueError:
        return False

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
        parts = line.split(' ')
        result = [x for x in parts if x and x.strip()]
            #['RH=', '22.9', '%RH', 'T=', '26.4', "'C"]

        humi = float(result[1])
        temp = float(result[4])

    ser0.close()
    return humi, temp, cnt

def pwd20():
    global vis_1, vis_10
    line = ser1.readline().decode('ascii').strip()
        # PW  100   7147  7086  

    if line:
        parts = line.split(' ')
            # ['\x01PW', '', '1\x0200', '', '', '7484', '', '8232\x03']
        result = [x for x in parts if x and x.strip()]
            # ['\x01PW', '1\x0200', '7562', '8120\x03']
        remove_chars = ["\x01", "\x02", "\x03"]
        result2 = [x.translate({ord(c): None for c in remove_chars}) for x in result]
            #['PW', '100', '7562', '8120']
        vis_1 =float(result2[2])        # 1 minute average visibility
        vis_10 = float(result2[3])  # 10 minute average visibility

    ser1.close()
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
