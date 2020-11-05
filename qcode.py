import serial

try:
    ser = serial.Serial('COM3',9600,timeout=0.01)
    data = ''
    n = ser.inWaiting()
    while True:
        if ser.in_waiting:
            str = ser.readall().decode("gbk")
            data = data + str
            print(data)
            data = ''
except Exception as e:
    print(e)
    print(e.__traceback__.tb_lineno)