import serial
import time
import serial.tools.list_ports as listports

com_port = ''

ports = list(listports.comports())
for port in ports:
    # print(f"port : {str(port)}")
    # print(f"Port :" + str(port[0]) + " Description: " + str(port[1]) + " VID:PID " + str(port[2])[12:21])
    port_name = str(port[2])[12:21]
    if port_name.upper() == '04D8:F80C':
        print(f"I'm using {str(port[0])}")
        com_port = str(port[0])

ser = serial.Serial(com_port, 9600)
count = 0
buffer = ''
char = ''

qnn = ':S7020N0D;'

for i in qnn:
    ser.write(str.encode(str(i)))

while True:
    if ser.inWaiting() > 0:
        data = ser.read().decode()
        # print(f"Data in {str(data)}")
        buffer = buffer + data
        if data == ';':
            print(f"Buffer == {buffer}")
            buffer = ''
        # print(f"In Waiting : {str(ser.in_waiting)}")
    time.sleep(0.001)
    # print(f"In Waiting : {str(ser.inWaiting())}")




