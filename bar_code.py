import serial
from time import sleep
from PyQt5.QtCore import QThread,pyqtSignal,Qt
import log
import public_var
class Bar_code(QThread):
    _signal = pyqtSignal(str)
    def __init__(self):
        super(Bar_code, self).__init__()
        self.code_nums = []
        self.rev_data = ''
    def run(self):
        try:
            port = public_var.qcode_com
            self.ser = serial.Serial(port,9600,timeout=0.01)
            while True:
                self.get_code = public_var.get_code
                if self.get_code:
                    if self.ser.in_waiting:
                        str = self.ser.readall().decode('gbk')
                        print(str)
                        self.code_nums.append(str)
                        # print(self.code_nums)
                    if len(self.code_nums) != 9:
                        pass
                    else:
                        self.rev_data = ','.join(self.code_nums)
                        self._signal.emit(self.rev_data)
                        # print('发送信号')
                        self.code_nums = []
                else:
                    break
        except Exception as e:
            self.rev_data = 'F00'
            print(e)
            # log.logging.error('<%s>'%e)
            self._signal.emit(self.rev_data)
            return