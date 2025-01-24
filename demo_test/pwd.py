# import pymodbus.client as ModbusClient
# import pymodbus as ModbusException
# import schedule
# import time
# # Modbus RTU 클라이언트 설정
# client = ModbusClient.ModbusSerialClient(
#     # method='rtu',           # RTU 방식
#     port='/dev/ttySC0',    # RS-485 포트
#     baudrate=9600,          # 통신 속도
#     bytesize=8,
#     parity='N',
#     stopbits=1,
#     timeout=1              # 타임아웃 (초)
# )

# # 연결 확인
# if not client.connect():
#     print("Unable to connect to the Modbus device.")
#     exit()

# def read_pwd():
#     # 레지스터 데이터 읽기 (시작 주소: 0x0000, 레지스터 개수: 3)
#     print("read ...")
#     response = client.read_holding_registers(address=0x0000, count=3, slave=1)

#     if isinstance(response, ModbusException):
#         print("Modbus communication error.")
#     else:
#         # 응답 데이터 파싱
#         visibility = response.registers[0]  # 레지스터 0: 시정 거리
#         rainfall = response.registers[1]   # 레지스터 1: 강수량
#         weather_code = response.registers[2]  # 레지스터 2: 기상 상태 코드

#         print(f"Visibility: {visibility} m")
#         print(f"Rainfall: {rainfall} mm/h")
#         print(f"Weather Condition Code: {weather_code}")
    
# schedule.every(3).seconds.do(read_pwd)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

# client.close()

import serial
import time

# 시리얼 포트 설정
ser = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=9600,
    bytesize=8,
    parity='N',
    stopbits=1,
    timeout=1  # 타임아웃 설정
)

# cmd = "SET PERIOD 3\r\n"
# ser.write(cmd.encode())
# print(cmd)
# time.sleep(0.5)

try:
    while True:
        # 데이터 읽기

        line = ser.readline().decode('ascii').strip()
        
        if line:
            #print(line)
            # PW  100   7147  7086
            # 데이터 파싱
            # if line.startswith("pw"):
            parts = line.split('  ')
            visibility_1 = float(parts[2])  # 1 minute average visibility
            visibility_10 = float(parts[3][:4])    # 10 minute average visibility
            print(f"1 minute average visibility: {visibility_1} m")
            print(f"10 minute average visibility: {visibility_10} m")

except KeyboardInterrupt:
    print("Stopped.")
finally:
    ser.close()
