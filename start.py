import serial
from time import sleep
from PyQt5.QtCore import QThread,pyqtSignal,Qt
import log
import serial.tools.list_ports
class Start(QThread):
    _signal = pyqtSignal(str)
    def __init__(self):
        super(Start, self).__init__()
        # self.ss_list = 'a' + ss_list
    def run(self):
        try:
            self.ser = serial.Serial('COM3',9600,timeout=0.5)
            # self.ser.write(self.ss_list.encode('gbk'))
            if self.ser.isOpen():
                print("open success")
                while True:
                    if self.ser.in_waiting:
                        a = self.ser.read(self.ser.in_waiting).decode("GBK")
                        self.code_nums = a.strip()
                        self._signal.emit(self.code_nums)
                        sleep(1)
                        continue
        except Exception as e:
            self.rev_data = 'F01'
            log.logging.error('<%s>'%str(e))
            self._signal.emit(self.rev_data)