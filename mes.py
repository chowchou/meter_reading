from threading import Thread
import requests,json
import log,configparser
class Send_mes(Thread):
    #  通过类成员对象定义信号对象
    def __init__(self,data):
        super(Send_mes, self).__init__()
        self.rev_data = data
    def run(self):
        try:
            postdata = self.rev_data
            print(postdata)
            postdata = json.dumps(postdata)
            url = 'http://127.0.0.1:5000/'
            req = requests.post(url, postdata)
        except Exception as e:
            self.rev_data = '{"respcode":"-1","respmsg": "请求服务器失败！"}'
            log.logging.error('<%s>'%str(e))
        else:
            self.res_data=req.text
            print(self.res_data)
        return self.res_data