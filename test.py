# from random import randint
#
# first = '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨'
# last = '关关雎鸠在河之洲蒹葭苍苍白露为霜溯游从之薇亦作止俟我于城隅静女其姝'
# # for i in first:
# #     print(i)
# user = []
# for name in range(50):
#     i = first[randint(0,15)] + last[randint(0,32)] + last[randint(0,32)]
#     user.append('name' = i,'password' = randint(0000000,9999999))
# import datetime
# import random
# import string
# import requests,json
#
# def send_mes(mes_data):
#     req_seq = 'PROD_' + datetime.datetime.now().strftime('%H%M%S%f') + "_" + ''.join(random.sample(string.digits, 2))
#     req = {
#         "HEAD": {"mid": "223", "uid": "57", "tran_type": "model_smpd_save", "checksum": "11223355", "req_seq": req_seq},
#         "BODY": mes_data
#     }
#     postdata = json.dumps(req)
#     print(postdata)
#     # url = 'http://127.0.0.1:5000/'
#     url = 'http://192.168.2.175/interface/tranapp/prodsmcb'
#     req = requests.post(url, postdata)
#     return req
# resdict = {"order": "MO2008A026", "model_id": "1234567890", "sn": "FF2060013C20", "chipid": "111111111111111222222111111111111111113333333333"}
# req = send_mes(resdict)
# code_res = json.loads(req.text)
# print(code_res)
# # # code_res = eval(req.text)
# # # res_flag = code_res.get('projectinfo')['model']
# print(code_res.get('BODY')['gwid_write_flag'])



# if res_flag == '1':
#     print('写入国网ID')
# elif res_flag == '2':
#     print('写入模块ID')
# elif res_flag == '3':
#     print('都写入')
#     chip_mmid = code_res.get('projectinfo')['chip_mmid']
#     a = '23 23 00 00 00 00 00 00 00 00 00 00 00 00 03 00 00 00 48 00 00 00 1E 00 00 00 48 00 18 00 18 00 %s 40 40 ' % chip_mmid
#     res = self.write_port(a,0.5)
#     if res != '':
#         res = {'win':str(self.win_id + 1),'data':res[-52:-4],'line_id':'4'}
#         self._signal.emit(res)
#
#     id = code_res.get('projectinfo')['id']
#     a = '23 23 00 00 00 00 00 00 00 00 00 00 00 00 03 00 00 00 3d 00 00 00 11 00 00 00 3d 00 0b 00 0b 00 %s 40 40' % id
#     res = self.write_port(a,0.5)
#     if res != '':
#         res = {'win':str(self.win_id + 1),'data':res[-26:-4],'line_id':'5'}
#         self._signal.emit(res)
# else:
#     print('都不写')
# import binascii
# from time import sleep
# import serial
#
# read_met = '68 32 00 00 00 00 00 68 11 04 34 33 33 32 E3 16'
# port = 'COM16'
# selParity = 'E'
# ser_2 = serial.Serial(port,9600,timeout=5,parity=selParity)
# print(ser_2.parity)
# print(ser_2.isOpen())
# # ser_2.flushInput()
# obj_write_info = binascii.a2b_hex(read_met.replace(" ", ""))
# ser_2.write(obj_write_info)
#
# while True:
#     sleep(1)
#     if ser_2.in_waiting:
#         res = ser_2.read(ser_2.in_waiting).hex().upper()
#         print(res)

# 抄表结果上传mes校验
# def cc_send_mes(self, mes_data):
#     req_seq = 'PROD_' + datetime.datetime.now().strftime('%H%M%S%f') + "_" + ''.join(
#         random.sample(string.digits, 2))
#     req = {
#         "HEAD": {"mid": "223", "uid": "57", "tran_type": "model_smpd_save", "checksum": "11223355",
#                  "req_seq": req_seq},
#         "BODY": mes_data
#     }
#     postdata = json.dumps(req)
#     print(postdata)
#     url = 'http://192.168.2.175/interface/tranapp/prodsmcb'
#     req = requests.post(url, postdata)
#     return req
# import binascii
# import time
# import serial
# port = 'COM11'
# ser = serial.Serial(port,19200,timeout=0.5)
# test = '00'
# order = 'Get RGB.All'  + '\r'
# # LEDA0,LEDB0,LEDA1,LEDB1,LEDA2,LEDB2 = False
# dict1 = {'LED0':False,'LED1':False,'LED2':False,'LED3':False,'LED4':False,'LED5':False}
# list1 = []
# print(order)
# order = str.encode(order)
# print(order)
# ser.write(order)
# time.sleep(1)
# if ser.in_waiting:
#     res = ser.read(ser.in_waiting).decode().replace("\n","").strip('%').replace(',', '').strip(';')
#     res = res.split(";")
#     print(res)
#     for i in range(3):
#         green_code = int(res[i][3:6])
#         red_code = int(res[i][0:3])
#         if red_code > 150 and green_code < 100:
#             name = 'LED' + str(i)
#             dict1[name] = True
#             list1.append()
#         elif red_code < 100 and green_code > 150:
#             name = 'LED' + str(i)
#             dict1[name] = True
#         else:
#             name = 'LED' + str(i)
#             dict1[name] = False
#
#     print(dict1)
import binascii
import re
import time
import traceback
from socket import *
from time import ctime, sleep

# HOST = ''
# PORT = 21567
# BUFSIZ = 1024
# ADDR = (HOST,PORT)
#
# tcpSerSock = socket(AF_INET,SOCK_STREAM)
# tcpSerSock.bind(ADDR)
# tcpSerSock.listen(5)
#
# while True:
#     print('waiting for connection...')
#     tcpCliSock, addr = tcpSerSock.accept()
#     print('...connnecting from:', addr)
#
#     while True:
#         data = tcpCliSock.recv(BUFSIZ)
#         if not data:
#             break
#         #tcpCliSock.send('[%s] %s' %(bytes(ctime(),'utf-8'),data))
#         tcpCliSock.send(('[%s] %s' % (ctime(), data)).encode())
#     tcpCliSock.close()
# tcpSerSock.close()
import serial

# ser = serial.Serial('COM5',2400,timeout=0.01,stopbits=2,parity='E')
# print(ser.parity)
# # data = ''
# # data.encode('UTF-8')
#
# while True:
#     time.sleep(1)
#     # # ser.flushInput()
#     order = 'BBBBBBBB'
#     # obj_write_info = binascii.a2b_hex(order.replace(" ", ""))
#     ser.write(order.encode("gbk"))
#     print('已发送',order)
#     # sleep(timeout)
#     data = ''
#     try:
#         if ser.in_waiting:
#             str = ser.readall().decode("gbk")
#             data = data + str
#             print('已接收',data)
#             data = ''
#     except Exception as e:
#         print(e)
#         print(e.__traceback__.tb_lineno)





        # try:
        #     if self.ser_flag:
        #         test_inset = self.test_inset()
        #         # print(test_inset)
        #         if test_inset:
        #             #关闭充电
        #             self.close_char()
        #             #读SN
        #             self.read_sn()
        #             sleep(0.1)
        #             # 读国网ID
        #             read_gwid = self.read_gwid()
        #             if read_gwid != '':
        #                 self.resdict['chipid'] = read_gwid
        #             else:
        #                 self.resdict['chipid'] = '000'
        #             sleep(0.1)
        #             ##上送mes校验
        #             req = self.send_mes(self.resdict)
        #             code_res = json.loads(req.text)
        #             gwid_flag = code_res.get('BODY')['gwid_write_flag']
        #             modid_flag = code_res.get('BODY')['modelid_write_flag']
        #             #验证MES校验返回结果
        #             if code_res.get('HEAD')['respcode'] == '000000':
        #                 chip_mmid = code_res.get('BODY')['chipid']
        #                 mod_id = code_res.get('BODY')['model_id']
        #                 if gwid_flag and modid_flag:
        #                     #写入国网ID
        #                     write_gwid = self.write_gwid(chip_mmid)
        #                     #写入模块ID
        #                     write_modid = self.write_modle(mod_id)
        #                     #验证写入是否成功
        #                     if write_gwid and write_modid:
        #                         print('写入成功')
        #                         self.is_pass('国网&模块ID写入成功','6')
        #                     elif write_gwid == False and write_modid :
        #                         self.is_fail('国网ID写入失败', '6')
        #                         self.is_fail('国网ID写入失败', '10')
        #                     elif write_modid ==False and write_gwid:
        #                         self.is_fail('模块ID写入失败', '6')
        #                         self.is_fail('模块ID写入失败', '10')
        #                     else:
        #                         self.is_fail('国网&模块ID写入失败', '6')
        #                         self.is_fail('国网&模块ID写入失败', '10')
        #
        #                 elif gwid_flag and modid_flag == False:
        #                     # 写入国网ID
        #                     write_gwid = self.write_gwid(chip_mmid)
        #                     #print(write_gwid)
        #                     if not write_gwid:
        #                         self.is_fail('国网ID写入失败', '6')
        #                         self.is_fail('国网ID写入失败', '10')
        #
        #                 elif modid_flag and gwid_flag == False:
        #                     # 写入模块ID
        #                     write_modid = self.write_modle(mod_id)
        #                     if not write_modid:
        #                         self.is_fail('模块ID写入失败', '6')
        #                         self.is_fail('模块ID写入失败', '10')
        #                 else:
        #                     self.is_pass('国网ID不写入', '4')
        #                     self.is_pass('模块ID不写入', '5')
        #
        #             else:
        #                 print('MES校验失败')
        #                 self.is_fail('MES校验失败', '10')
        #             ##退出产测模式
        #             res = self.write_port(self.close_trans, 1)
        #             self.is_pass('扫码配对完成', '6')
        #             self.meter_flag = True
        #             #self.log.info('退出产测模式')
        #             print(res, '退出产测模式,进入抄表流程')
        #
        #         else:
        #             print('进入产测模式失败')
        #             # self.log.error('进入产测模式失败')
        #             self.is_fail('进入产测失败','10')
        #     else:
        #         pass
        #
        # except Exception as e:
        #     traceback.print_exc()
        #     print(e,'diyi')
        #     res = self.write_port(self.close_trans, 1)
        #     print(res, 'end')
        #     self.is_fail('扫码配对运行出错','10')
        # #68 BB BB BB BB BB BB 68 1A 04 00 14 26 27 2B DC 16
        # #68 BB B7 B7 DB DB 68 9A 80 80 73 F1
        # #68 BB BB BB BB BB BB 68 1B 04 00 2B 28 27 14 DF 16
        # #68 BB B7 B7 DB DB 68 9B 80 40 73 F1
        # #68 32 00 00 00 00 00 68 11 04 34 33 33 32 E3 16
        # try:
        #     if self.meter_flag:
        #         res = self.write_port(self.up_power,1)
        #         # self.times = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        #         # print(res, '上电',self.times)
        #         # self.log.info('进入抄表模式 start')
        #         self.is_pass('进入抄表模式', '8')
        #         if res != '':
        #             sleep(3)
        #             print('抄表开始')
        #             read_met = '68 32 00 00 00 00 00 68 11 04 34 33 33 32 E3 16'
        #             port = 'COM' + str(self.meter[self.win_id])
        #             selParity = 'E'
        #             ser_2 = serial.Serial(port, 9600, timeout=5, parity=selParity)
        #             obj_write_info = binascii.a2b_hex(read_met.replace(" ", ""))
        #             ser_2.write(obj_write_info)
        #             while True:
        #                 sleep(1)
        #                 if ser_2.in_waiting:
        #                     res = ser_2.read(ser_2.in_waiting).hex().upper()
        #                     resp = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", res)
        #                     if len(resp) >= 239:
        #                         # print('dealing date')
        #                         recv_data = resp.split()[10:78]
        #                         res = no_33(recv_data)
        #                         res = data_analysis_temp(res)
        #                         print(res)
        #                         print(type(res))
        #                         res['prod_line'] = self.prod_line
        #                         res['win_id'] = self.computer
        #                         ##缺少指令单号
        #                         result = self.cc_send_mes(res)
        #                         # result = result.text
        #                         result = json.loads(result.text)
        #                         print(result)
        #                         print(type(result))
        #                         if result.get('HEAD')['respcode'] == '000000':
        #                             print('成功')
        #                             #self.log.info('抄表数据对比成功 PASS')
        #                         else:
        #                             print('失败')
        #                             #self.log.error('抄表数据对比失败 Fail')
        #                         self.is_pass('pass', '9')
        #                         self.is_pass('pass完成', '10')
        #
        #                         ledname1 = 'LED' + str(self.win_id*2)
        #                         ledname2 = 'LED' + str(self.win_id*2 + 1)
        #                         ledA = dict1[ledname1]
        #                         ledB = dict1[ledname2]
        #                         if ledA and ledB:
        #                             self.is_pass('LED正常', '7')
        #                         else:
        #                             self.is_fail('LED异常', '7')
        #                             self.is_fail('LED异常', '10')
        #
        #                     else:
        #                         self.is_fail('抄表读取数据错误', '10')
        #                         # self.log.error('抄表读取数据错误')
        #                     break
        #
        #             print('抄表结束')
        #             res = self.write_port(self.down_power, 1)
        #             self.times = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        #             print(res,'掉电',self.times)
        #             #self.log.info('掉电 end')
        #         else:
        #             # self.log.error('进入抄表模式失败')
        #             self.is_fail('进入抄表模式失败', '8')
        #             self.is_fail('进入抄表模式失败', '10')
        # except Exception as e:
        #     print(e)
        #     self.is_fail('抄表运行出错', '10')
        #     # self.log.error('抄表运行出错')


transmission = '68 BB BB BB BB BB BB 68 1C 04 00 FF FF FF FF 4E 16'  # 开启数据透传
close_trans = '68 BB BB BB BB BB BB 68 1C 04 00 F0 F0 F0 F0 12 16'  # 关闭数据透传
up_power = '68 BB BB BB BB BB BB 68 1A 04 00 14 26 27 2B DC 16'
down_power = '68 BB BB BB BB BB BB 68 1B 04 00 2B 28 27 14 DF 16'
def write_port(order):
    try:
        ser = serial.Serial('COM61', 115200, timeout=0.5)
        obj_write_info = binascii.a2b_hex(order.replace(" ", ""))
        ser.write(obj_write_info)
        while True:
            if ser.in_waiting:
                res = ser.readall().hex().upper()
                print(res)
                break
        ser.close()
        print('串口1已关闭')
        return res
    except Exception as e:
        traceback.print_exc()
        res = False
        return res

def run_meter():
    print('进入成功')
    read_met = '68 32 00 00 00 00 00 68 11 04 34 33 33 32 E3 16'
    port = 'COM71'
    ser_2 = serial.Serial(port, 9600, timeout=1, parity='E')
    obj_write_info = binascii.a2b_hex(read_met.replace(" ", ""))
    ser_2.write(obj_write_info)
    print('发送成功', obj_write_info)
    while True:
        if ser_2.in_waiting:
            res = ser_2.readall().hex().upper()
            res = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", res)
            print(res)
            break
    return res

# a = write_port(down_power)
# a = write_port(up_power)
# sleep(2)
# b = run_meter()
a = write_port(down_power)

