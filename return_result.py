from PyQt5.QtCore import QThread,pyqtSignal,Qt
import requests,json
import log,configparser
class Get_result(QThread):
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)
    def __init__(self,res):
        super(Get_result, self).__init__()
        self.rev_data =''
    def __del__(self):
        self.wait()
    def run(self):
        try:

        except Exception as e:
            self.rev_data = '{"respcode":"-1","respmsg": "请求服务器失败！"}'
            log.logging.error('<%s>'%str(e))
        else:
            self.rev_data=req.text
        self._signal.emit(self.rev_data)