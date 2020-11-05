############################
#     PLC线程        #
############################

import serial
from time import sleep
from PyQt5.QtCore import QThread,pyqtSignal,Qt
import log
import serial.tools.list_ports
class Start_code(QThread):
    _signal = pyqtSignal(str)
    def __init__(self,data):
        super(Start_code, self).__init__()
        #self.ss_list = 'a' + ss_list
        self.port = data
    def run(self):
        try:
            self.ser = serial.Serial(self.port,2400,timeout=0.5,stopbits=2,parity='E')
            data = ''
            #self.ser.write(self.ss_list.encode('gbk'))
            if self.ser.isOpen():
                print("open success")
                while True:
                    if self.ser.in_waiting:
                        a = self.ser.readall().decode("gbk")
                        # self.code_nums = a.strip()
                        data = data + a
                        print('已接收', data)
                        self._signal.emit(data)
                        data = ''
        except Exception as e:
            self.rev_data = 'F01'
            log.logging.error('<%s>'%str(e))
            self._signal.emit(self.rev_data)