#################
#   无条码模式
#################
import binascii
import json
import random
import re
import traceback
from time import sleep
import datetime
import string
import func_timeout
import requests
import serial
from PyQt5.QtCore import QThread, pyqtSignal
from func_timeout import func_set_timeout
from  dealing import data_analysis_temp,no_33
import public_var


class Read_nocode(QThread):
    _signal = pyqtSignal(dict)
    def __init__(self, win_id):
        super(Read_nocode, self).__init__()
        self.pair = [61, 62, 63, 64, 65, 66, 67, 68]
        self.meter = [71, 72, 73, 74, 75, 76, 77, 78]
        self.win_id = win_id
        self.order_id = public_var.order_id
        self.computer = public_var.new_cname
        self.prod_line = public_var.new_pline
        self.transmission = '68 BB BB BB BB BB BB 68 1C 04 00 FF FF FF FF 4E 16'  # 开启数据透传
        self.close_trans = '68 BB BB BB BB BB BB 68 1C 04 00 F0 F0 F0 F0 12 16'  # 关闭数据透传
        self.up_power = '68 BB BB BB BB BB BB 68 1A 04 00 14 26 27 2B DC 16'
        self.down_power = '68 BB BB BB BB BB BB 68 1B 04 00 2B 28 27 14 DF 16'
    def __del__(self):
        self.wait()

    def is_fail(self,data,line_id):
        rev_data = {'win': str(self.win_id + 1), 'data': data, 'line_id': line_id, 'ngcode': 'fail'}
        self._signal.emit(rev_data)
    def is_pass(self,data,line_id):
        res = {'win': str(self.win_id + 1), 'data': data, 'line_id': line_id, 'ngcode': 'pass'}
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
            self.is_fail('串口打开错误：%s' %e, '10')
            res = False
            return res
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

    @func_set_timeout(15)
    def run_meter(self):
        sleep(3)
        read_met = '68 32 00 00 00 00 00 68 11 04 34 33 33 32 E3 16'
        port = 'COM' + str(self.meter[self.win_id])
        self.ser_2 = serial.Serial(port, 9600, timeout=1, parity='E')
        obj_write_info = binascii.a2b_hex(read_met.replace(" ", ""))
        self.ser_2.write(obj_write_info)
        print('发送成功', obj_write_info)
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
        ###抄表开始
        res = self.write_port(self.up_power, 1)  # 上电
        if res:
            self.is_pass('进入抄表模式', '8')
        else:
            self.is_fail('抄表模式进入失败', '10')
            return
        try:
            run_meter = self.run_meter()
        except func_timeout.exceptions.FunctionTimedOut:
            run_meter = False
            self.ser_2.close()
            self.write_port(self.close_trans, 1)
            self.write_port(self.down_power, 1)
            print('状态清理完成')
        if not run_meter:
            self.is_fail('抄表服务器校验错误', '10')
            return
        else:
            self.is_pass('抄表完成,抄表正常', '9')
        ##LED
        run_led = self.run_led()
        if not run_led:
            self.is_fail('LED异常', '7')
            self.is_fail('LED异常', '10')
            return
        else:
            self.is_pass('LED正常', '7')
        self.is_pass('全部流程完成，pass', '10')


    def run(self):
        self.port = 'COM' + str(self.pair[self.win_id])
        try:
            self.run_all()
        except func_timeout.exceptions.FunctionTimedOut:
            print('已超时')
            print(self.ser_flag)
            if self.ser_flag:
                self.ser.close()
            self.write_port(self.close_trans, 1)
            self.write_port(self.down_power, 1)
            print('状态清理完成，退出线程')
        return