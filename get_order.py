######################
# 获取订单线程 #
#####################


from PyQt5.QtCore import QThread,pyqtSignal,Qt
import requests,json
import log,configparser
class Get_order(QThread):
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)
    def __init__(self,data):
        super(Get_order, self).__init__()
        self.rev_data =''
        self.mes_ip = data
    def __del__(self):
        self.wait()
    def run(self):
        try:
            postdata = {
                "trantype": "getprojectinfo",  # 扫码配对工装获取项目信息
                "MENU_ID": "10",
                "uid": "38",
                "checksum": "11223355",
            }
            postdata = json.dumps(postdata)
            #print(postdata)
            url = 'http://%s/api/admin/lqkjsmpd'%self.mes_ip
            req = requests.post(url, postdata)
        except Exception as e:
            self.rev_data = '{"respcode":"-1","respmsg": "请求服务器失败！"}'
            log.logging.error('<%s>'%str(e))
        else:
            self.rev_data=req.text
        self._signal.emit(self.rev_data)