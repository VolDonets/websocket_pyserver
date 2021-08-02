import math
import serial
import json
import time


class MySerial:
    def __init__(self, port, baudrate):
        self.serialPort = serial.Serial(port=port, baudrate=baudrate)
        if self.serialPort.isOpen():
            print("Serial port in " + str(port) + ", " + str(baudrate) + " is OPENED")
        else:
            print("Serial port in " + str(port) + ", " + str(baudrate) + " is NOT opened")

    def write_msg(self, msg):
        msg += "\n"
        self.serialPort.write(msg.encode("ASCII"))

    def read_msg(self):
        msg = self.serialPort.readline().decode("ASCII")
        return msg


def process_data(message):
    try:
        json_data = json.loads(message)
    except json.JSONDecodeError:
        return ""

    t0 = json_data['t0']
    t1 = json_data['t1']
    t2 = json_data['t2']
    t3 = json_data['t3']

    a0 = json_data['A0']
    a1 = json_data['A1']
    a2 = json_data['A2']
    a3 = json_data['A3']

    a = (a0 + a1 + a2 + a3) / 4
    # phi = math.atan2(-t3 + t1 + t2 - t0, -t3 - t1 + t2 + t0)
    y_coord = -t3 + t1 + t2 - t0
    x_coord = -t3 - t1 + t2 + t0
    if x_coord == 0 and y_coord == 0:
        phi = 0
    else:
        phi = math.atan2(y_coord, x_coord) + math.pi
    C = math.cos(phi)
    S = math.sin(phi)

    tay = (t0 + t1 + t2 + t3) / 4
    t0 -= tay
    t1 -= tay
    t2 -= tay
    t3 -= tay

    Vs = - a / 2
    Vs *= t3 * (C + S) + t1 * (C - S) + t2 * (-C - S) + t0 * (-C + S)
    Vs /= (t0 * t0 + t1 * t1 + t2 * t2 + t3 * t3)

    c = 330

    tetta = 0
    if Vs < c:
        tetta = math.acos(Vs / c)

    json_data['phi'] = phi
    json_data['A'] = a
    json_data['tetta'] = tetta

    return json.dumps(json_data)


class MessageProcessing:
    def __init__(self):
        self.mySerialPort = MySerial('/dev/ttyUSB0', 115200)

    def get_message(self):
        msg = self.mySerialPort.read_msg()
        return process_data(msg)


if __name__ == "__main__":
    print("Do some tests: ")
    msg = '{"t0":1.1, "t1":1.2, "t2":1.2, "t3":1.3, "A0":1, "A1":1, "A2":1, "A3":4}'
    print("in data:", msg)
    print("out data:", process_data(msg))

    mySerial = MySerial('/dev/ttyUSB1', 115200)
    while True:
        mySerial.write_msg(msg)
        print("msg:", msg, "is sent")
        time.sleep(1)
