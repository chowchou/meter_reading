######
# 有条码模式
######

import re
import traceback
from time import sleep

import func_timeout
import serial
from PyQt5.QtCore import QThread,pyqtSignal,Qt
import binascii
import datetime
import random
import string
import requests,json
from func_timeout import func_set_timeout

import public_var
import time
from  dealing import data_analysis_temp,no_33
# from test_log import getLogger
class Read_write(QThread):
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(dict)
    def __init__(self,win_id,model_id):
        super(Read_write, self).__init__()
        self.pair = [61,62,63,64,65,66,67,68]
        self.meter = [71,72,73,74,75,76,77,78]
        self.win_id = win_id
        self.order_id = public_var.order_id
        self.computer = public_var.new_cname
        self.prod_line = public_var.new_pline
        # self.order_id = order_id
        self.model_id = model_id
        # self.prod_line = prod_line
        # self.computer = computer_name
        #print(self.model_id)
        self.transmission = '68 BB BB BB BB BB BB 68 1C 04 00 FF FF FF FF 4E 16'  # 开启数据透传
        self.close_charging = '23 23 00 00 00 00 00 00 00 00 00 00 00 00 03 00 00 00 2d 00 00 00 06 00 00 00 2d 00 00 00 00 00 40 40'  # 关闭电容充电
        self.get_sn = '23 23 00 00 00 00 00 00 00 00 00 00 00 00 03 00 00 00 2b 00 00 00 06 00 00 00 2b 00 00 00 00 00 40 40'  # 获取6位SN
        self.get_id = '23 23 00 00 00 00 00 00 00 00 00 00 00 00 03 00 00 00 3e 00 00 00 06 00 00 00 3e 00 00 00 00 00 40 40'  # 获取11位模块ID
        self.chip_mmid = '23 23 00 00 00 00 00 00 00 00 00 00 00 00 03 00 00 00 38 00 00 00 06 00 00 00 38 00 00 00 00 00 40 40'  # 获取24位国网ID
        self.close_trans = '68 BB BB BB BB BB BB 68 1C 04 00 F0 F0 F0 F0 12 16'  # 关闭数据透传
        self.up_power = '68 BB BB BB BB BB BB 68 1A 04 00 14 26 27 2B DC 16'
        self.down_power = '68 BB BB BB BB BB BB 68 1B 04 00 2B 28 27 14 DF 16'
        times = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
        self.ser_2 = None
        self.ser = None
    def __del__(self):
        self.wait()
    def write_port(self,order,timeout):
        try:
            self.ser = serial.Serial(self.port, 115200, timeout=0.5)
            self.ser_flag = True
            obj_write_info = binascii.a2b_hex(order.replace(" ", ""))
            self.ser.write(obj_write_info)
            sleep(timeout)
            while True:
                if self.ser.in_waiting:
                    res = self.ser.readall().hex().upper()
                    print(res)
                    break
            self.ser.close()
            self.ser_flag = False
            print('串口1已关闭')
            return res
        except Exception as e:
            traceback.print_exc()
            # self.ser_flag = False
            self.is_fail('串口打开错误：%s' %e, '10')
            res = False
            return res
            #self.log.error('串口打开错误：'+str(e))
    #关闭充电
    def close_char(self):
        res = self.write_port(self.close_charging, 0.5)
        return res
    #上传mes获取数据
    def send_mes(self,mes_data):
        req_seq = 'PROD_' + datetime.datetime.now().strftime('%H%M%S%f') + "_" + ''.join(random.sample(string.digits, 2))
        req = {
                "HEAD":{"mid": "223", "uid": "57", "tran_type": "model_smpd_save", "checksum": "11223355", "req_seq": req_seq},
                "BODY": mes_data
               }
        postdata = json.dumps(req)
        print(postdata)
        url = 'http://%s/interface/tranapp/prodsmcb' %public_var.server_ip
        req = requests.post(url, postdata)
        # return req
        code_res = json.loads(req.text)
        self.gwid_flag = code_res.get('BODY')['gwid_write_flag']
        self.modid_flag = code_res.get('BODY')['modelid_write_flag']
        if self.gwid_flag:
            self.new_chip_mmid = code_res.get('BODY')['chipid']
        if self.modid_flag:
            self.new_mod_id = code_res.get('BODY')['model_id']
        if code_res.get('HEAD')['respcode'] == '000000':
            flag = True
            # list = [gwid_flag,modid_flag,chip_mmid,mod_id]
            # flag = list
        else:
            flag = False
        return flag
    # 抄表结果上传mes校验
    def cc_send_mes(self, mes_data):
        req_seq = 'PROD_' + datetime.datetime.now().strftime('%H%M%S%f') + "_" + ''.join(
            random.sample(string.digits, 2))
        req = {
            "HEAD": {"mid": "223", "uid": "57", "tran_type": "model_meterread_save", "checksum": "11223355",
                     "req_seq": req_seq},
            "BODY": mes_data
        }
        postdata = json.dumps(req)
        print(postdata)
        url = 'http://%s/interface/tranapp/prodsmcb' %public_var.server_ip
        req = requests.post(url, postdata)
        return req
    #读国网ID
    def read_gwid(self):
        res = self.write_port(self.chip_mmid, 1)
        chipid = res[-52:-4]
        if chipid != '':
            self.resdict['chipid'] = chipid
            flag = True
        else:
            self.resdict['chipid'] = '000'
            flag = False
        return flag
    # 读模块ID
    def read_modelid(self):
        res = self.write_port(self.get_id, 1)
        model_id = res[-26:-4]
        #self.log.info('读模块ID：' + str(model_id))
        return model_id
    #进入产测模式
    def test_inset(self):
        res = self.write_port(self.transmission, 3)
        if res == '68BBBBBBBBBBBB689C0000CE16':
            res = {'win': str(self.win_id + 1), 'data': '进入产测成功', 'line_id': '2', 'ngcode': '0'}
            flag = True
        else:
            res = {'win': str(self.win_id + 1), 'data': '进入产测失败', 'line_id': '2', 'ngcode': '0'}  # 进入产测失败
            flag = False
        self._signal.emit(res)
        return flag
    #获取SN
    def read_sn(self):
        res = self.write_port(self.get_sn, 0.5)
        print(res, 'j1')
        sn = res[-16:-4]
        if sn != ' ':
            res = {'win': str(self.win_id + 1), 'data': sn, 'line_id': '3', 'ngcode': '0'}  # 获取SN成功
            self.resdict['sn'] = sn
            flag = True
            #self.log.info('获取SN：' + str(sn))
        else:
            res = {'win': str(self.win_id + 1), 'data': '获取SN失败', 'line_id': '3', 'ngcode': '0'}  # 获取SN失败
            self.resdict['sn'] = '000000000000'
            flag = False
            #self.log.info('获取SN失败：' + str(sn))
        self._signal.emit(res)
        return flag
    #写国网ID
    def write_gwid(self,num):
        write = '23 23 00 00 00 00 00 00 00 00 00 00 00 00 03 00 00 00 48 00 00 00 1E 00 00 00 48 00 18 00 18 00 %s 40 40 ' % num
        res = self.write_port(write, 0.5)
        res = {'win': str(self.win_id + 1), 'data': res[-52:-4], 'line_id': '4', 'ngcode': '0'}
        print(res)
        self._signal.emit(res)
        # 验证写入是否成功
        check_gwid = self.read_gwid()
        if check_gwid == num:
            check_gwid_flag = True
            print('写入成功')
            #self.log.info('写入国网ID成功：' + str(res[-52:-4]))
        else:
            check_gwid_flag = False
        return check_gwid_flag
    #写模块ID
    def write_modle(self,num):
        a = '23 23 00 00 00 00 00 00 00 00 00 00 00 00 03 00 00 00 3d 00 00 00 11 00 00 00 3d 00 0b 00 0b 00 %s 40 40' % num
        res = self.write_port(a, 0.5)
        res = {'win': str(self.win_id + 1), 'data': res[-26:-4], 'line_id': '5', 'ngcode': '0'}
        print(res)
        self._signal.emit(res)
        # 验证写入是否成功
        check_modelid = self.read_modelid()
        if check_modelid == num:
            check_modelid = True
            print('写入成功')
            #self.log.info('写入模块ID成功：' + str(res[-26:-4]))
        else:
            check_modelid = False
        return check_modelid
    def is_fail(self,data,line_id):
        rev_data = {'win': str(self.win_id + 1), 'data': data, 'line_id': line_id, 'ngcode': 'fail'}
        #self.log.error(str(data) + 'LINE:' + str(line_id))
        self._signal.emit(rev_data)
    def is_pass(self,data,line_id):
        res = {'win': str(self.win_id + 1), 'data': data, 'line_id': line_id, 'ngcode': 'pass'}
        #self.log.info(str(data))
        self._signal.emit(res)
    def run_led(self):
        ledname1 = 'LED' + str(self.win_id * 2)
        ledname2 = 'LED' + str(self.win_id * 2 + 1)
        ledA = public_var.dict1[ledname1]
        ledB = public_var.dict1[ledname2]
        if ledA and ledB:
            self.is_pass('LED正常', '7')
            flag = True
        else:
            flag = False
        return flag

    @func_set_timeout(15)
    def run_meter(self):
        sleep(3)
        read_met = '68 32 00 00 00 00 00 68 11 04 34 33 33 32 E3 16'
        port = 'COM' + str(self.meter[self.win_id])
        self.ser_2 = serial.Serial(port, 9600, timeout=1, parity='E')
        obj_write_info = binascii.a2b_hex(read_met.replace(" ", ""))
        self.ser_2.write(obj_write_info)
        print('发送成功',obj_write_info)
        while True:
            if self.ser_2.in_waiting:
                res = self.ser_2.readall().hex().upper()
                res = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", res)
                print(res)
                break
        self.ser_2.close()
        print('串口2已关闭')
        # if len(res) >= 239:
        recv_data = res.split()[10:78]
        res = no_33(recv_data)
        res = data_analysis_temp(res)
        # print(res)
        res['prod_line'] = self.prod_line
        res['win_id'] = self.computer
        res['order_id'] = self.order_id
        res['model_id']=self.model_id
        result = self.cc_send_mes(res)
        # print('发送给MES')
        result = json.loads(result.text)
        print(result)
        if result.get('HEAD')['respcode'] == '000000':
            flag = True
        else:
            flag = False
        return flag
    @func_set_timeout(30)
    def run_all(self):
        test_inset = self.test_inset()
        if test_inset:
            self.close_char()
        else:
            self.is_fail('产测模式失败', '10')
            return
        read_sn = self.read_sn()
        if not read_sn:
            self.is_fail('SN读取失败', '10')
            return
        read_gwid = self.read_gwid()
        if not read_gwid:
            self.is_fail('国网ID读取失败', '10')
            return
        send_mes = self.send_mes(self.resdict)
        if not send_mes:
            self.is_fail('扫码配对服务器验证失败', '10')
            return

        if not self.gwid_flag:
            self.is_pass('国网ID不写入', '4')
            # self.is_pass('国网&模块ID写入成功','6')
        else:
            write_gwid = self.write_gwid(self.new_chip_mmid)
            if not write_gwid:
                self.is_fail('国网ID写入失败', '10')
                return
            else:
                self.is_pass(self.new_chip_mmid, '4')
        if not self.modid_flag:
            self.is_pass('模块ID不写入', '5')
            self.is_pass('国网&模块ID成功','6')
        else:
            write_modid = self.write_modle(self.new_mod_id)
            if not write_modid:
                self.is_fail('模块ID写入失败', '10')
                return
            else:
                self.is_pass(self.new_mod_id, '5')
        res = self.write_port(self.close_trans, 1.4)
        if res:
            self.is_pass('扫码配对完成', '6')
            # self.meter_flag = True
        else:
            return

        ###抄表开始
        res = self.write_port(self.up_power, 1)  # 上电
        if res:
            self.is_pass('进入抄表模式', '8')
        else:
            self.is_fail('抄表模式进入失败', '10')
            return
        # time.sleep(2)
        try:
            run_meter = self.run_meter()
        except func_timeout.exceptions.FunctionTimedOut:
            run_meter = False
            self.ser_2.close()
            self.is_fail('超时', '10')
            self.write_port(self.close_trans, 1)
            self.write_port(self.down_power, 1)
            print('状态清理完成')
        if not run_meter:
            self.is_fail('抄表服务器校验错误', '10')
            return
        else:
            self.is_pass('抄表完成,抄表正常', '9')
        ##LED
        # run_led = self.run_led()
        # if not run_led:
        #     self.is_fail('LED异常', '7')
        #     self.is_fail('LED异常', '10')
        #     return
        # else:
        #     self.is_pass('LED正常', '7')

        self.is_pass('全部流程完成，pass','10')
    def run(self):
        self.times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(self.times)
        # self.meter_flag = False
        self.resdict = {'order_id': self.order_id, 'model_id': str(self.model_id),'win_id':self.computer,'prod_line':self.prod_line}
        self.port = 'COM' + str(self.pair[self.win_id])
        try:
            self.run_all()
        except func_timeout.exceptions.FunctionTimedOut:
                # print()
            print('已超时')
            self.is_fail('超时', '10')
            print(self.ser_flag)
            if self.ser_flag:
                self.ser.close()
            self.write_port(self.close_trans, 1)
            self.write_port(self.down_power, 1)
            print('状态清理完成，退出线程')
        return
