# from flask import Flask, request
# import json
#
# app = Flask(__name__)
#
#
# # 只接受POST方法访问
# @app.route("/", methods=["POST"])
# def check():
#     # 默认返回内容
#     return_dict = {'return_code': '200','respcode':'000000', 'return_info': '处理成功', 'projectinfo': {'chip_mmid': '111111111111111222222111111111111111113333333333', 'id': '0000000000000000001111','model':'3'}}
#     # 判断传入的json数据是否为空
#     if request.get_data() is None:
#         return_dict['return_code'] = '5004'
#         return_dict['return_info'] = '请求参数为空'
#         return json.dumps(return_dict, ensure_ascii=False)
#     # 获取传入的参数
#     get_Data = request.get_data()
#     # 传入的参数为bytes类型，需要转化成json
#     get_Data = json.loads(get_Data)
#     print(get_Data)
#     name = get_Data.get('trantype')
#     age = get_Data.get('MENU_ID')
#     return_dict['projectinfo'] = {'chip_mmid': '111111111111111222222111111111111111113333333333', 'id': '0000000000000000001111','model':'3'}
#     return json.dumps(return_dict, ensure_ascii=False)
#
#
# if __name__ == "__main__":
#     app.run(debug=True)

from socket import *

HOST = '127.0.0.1' # or 'localhost'
PORT = 21567
BUFSIZ =1024
ADDR = (HOST,PORT)

tcpCliSock = socket(AF_INET,SOCK_STREAM)
tcpCliSock.connect(ADDR)
while True:
     data1 = input('>')
     #data = str(data)
     if not data1:
         break
     tcpCliSock.send(data1.encode())
     data1 = tcpCliSock.recv(BUFSIZ)
     if not data1:
         break
     print(data1.decode('utf-8'))
tcpCliSock.close()