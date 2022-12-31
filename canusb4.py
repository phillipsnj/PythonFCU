import serial
import time
import threading
import serial.tools.list_ports as listports


class CanUsb4(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.callback = callback
        self.com_port = ''
        for port in list(listports.comports()):
            port_name = str(port[2])[12:21]
            if port_name.upper() == '04D8:F80C':
                print(f"I'm using {str(port[0])}")
                self.com_port = str(port[0])
        self.ser = serial.Serial(self.com_port)

    def run(self):
        count = 0
        buffer = ''
        char = ''
        while True:
            if self.ser.inWaiting() > 0:
                data = self.ser.read().decode()
                # print(f"Data in {str(data)}")
                buffer = buffer + data
                if data == ';':
                    # print(f"Buffer == {buffer}")
                    self.callback(buffer)
                    buffer = ''
                # print(f"In Waiting : {str(ser.in_waiting)}")
            time.sleep(0.001)

    def send(self, msg):
        for i in msg:
            self.ser.write(str.encode(str(i)))
