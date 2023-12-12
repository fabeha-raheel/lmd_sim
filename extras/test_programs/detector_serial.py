import serial

port = "/dev/ttyUSB0"

controller = serial.Serial(port=port, baudrate=9600)

while True:
    data = controller.readline()
    data = data.decode('utf-8').strip()
    # if data != "0":
    #     print("High")
    # else:
    #     pass
    print(data)