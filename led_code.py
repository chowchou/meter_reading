#######
# LED线程
#######

import serial
from time import sleep
from PyQt5.QtCore import QThread,pyqtSignal,Qt
import log
import serial.tools.list_ports
# from local_test import dict1
import public_var
class Led_code(QThread):
    _signal = pyqtSignal(str)
    def __init__(self):
        super(Led_code, self).__init__()
        #self.ss_list = 'a' + ss_list
    def run(self):
        try:
            port = 'COM11'
            ser = serial.Serial(port, 19200, timeout=0.5)
            order = 'Get RGB.All' + '\r'
            # dict1 = {'LED0': False, 'LED1': False, 'LED2': False, 'LED3': False, 'LED4': False, 'LED5': False}
            order = str.encode(order)
            sleep(10)
            print('LED开始检测')
            ser.write(order)
            sleep(1)
            if ser.in_waiting:
                res = ser.read(ser.in_waiting).decode().replace("\n", "").strip('%').replace(',', '').strip(';')
                res = res.split(";")
                print(res)
                # global dict1
                # print(dict1)
                for i in range(3):
                    green_code = int(res[i][3:6])
                    red_code = int(res[i][0:3])
                    if red_code > 150 and green_code < 100:
                        name = 'LED' + str(i)
                        public_var.dict1[name] = True
                    elif red_code < 100 and green_code > 150:
                        name = 'LED' + str(i)
                        public_var.dict1[name] = True
                    else:
                        name = 'LED' + str(i)
                        public_var.dict1[name] = False
                print(public_var.dict1)
                ser.close()
                return
        except Exception as e:
            # self.rev_data = 'F01'
            print(e)
            log.logging.error('<%s>'%str(e))
            # self._signal.emit(self.rev_data)