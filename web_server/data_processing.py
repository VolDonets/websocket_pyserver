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
    if "Relax" in message:
        return "NONE"
    try:
        json_orig_data = json.loads(message)
    except json.JSONDecodeError:
        return "NONE"

    t0 = json_orig_data['Ch_0']
    t1 = json_orig_data['Ch_1']
    t2 = json_orig_data['Ch_2']
    t3 = json_orig_data['Ch_3']

    a0 = json_orig_data['Max_0']
    a1 = json_orig_data['Max_1']
    a2 = json_orig_data['Max_2']
    a3 = json_orig_data['Max_3']

    json_data = dict()

    json_data['t0'] = t0
    json_data['t1'] = t1
    json_data['t2'] = t2
    json_data['t3'] = t3

    json_data['A0'] = a0
    json_data['A1'] = a1
    json_data['A2'] = a2
    json_data['A3'] = a3

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
        # self.mySerialPort = MySerial('/dev/ttyUSB0', 115200)
        self.mySerialPort = MySerial('COM3', 115200)

    def get_message(self):
        msg = self.mySerialPort.read_msg()
        return process_data(msg)
        # return msg


if __name__ == "__main__":
    mySerial = MySerial('/dev/ttyUSB1', 115200)
    json_data = dict()
    json_data['t0'] = 1
    json_data['t1'] = 2
    json_data['t2'] = 3
    json_data['t3'] = 4

    json_data['A0'] = 3
    json_data['A1'] = 4
    json_data['A2'] = 3
    json_data['A3'] = 3

    json_data['A'] = 3.333
    json_data['phi'] = 0
    json_data['tetta'] = 3.14
    while True:
        msg_to_sent = json.dumps(json_data)
        mySerial.write_msg(msg_to_sent)
        print("msg:", msg_to_sent, "is sent")
        json_data['phi'] += 0.1
        time.sleep(1)
