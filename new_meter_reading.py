import json

from mian import *
from toconfig import *
import os
import serial
import time
import datetime
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QComboBox, QRadioButton, QMessageBox, QCheckBox, \
    QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal, QWaitCondition, QCoreApplication
import configparser
from get_order import Get_order
from start_code import Start_code
# from bar_code import Bar_code
from read_write import Read_write
import log
from led_code import Led_code
from bar_code import Bar_code
from no_code import Read_nocode
import public_var
global conut_num
conut_num = []



class Main_ui(QMainWindow,Ui_New_meter_reading):#实例化主界面
    def __init__(self):
        super(Main_ui, self).__init__()
        self.setupUi(self)
        self.child_window = Child_ui()
        self.ui_init()
        self.pushButton.clicked.connect(self.work_start)
        self.pushButton_2.clicked.connect(self.work_stop)
        self.pushButton_3.clicked.connect(self.sysbutton)

    def ui_init(self):#初始化界面
        self.clear_text()
        if os.path.exists(public_var.init_path+'/config.ini'):
            self.check_option_log('配置文件正常')
        else:
            self.check_option_log('配置文件异常，请检查')
        self.work_stop()
        self.read_config()
        #启动获取订单详情
        self.get_order = Get_order(public_var.server_ip)
        self.get_order._signal.connect(self.order_res)
        self.get_order.run()
        # 启动接收PLC命令
        self.start_fl = Start_code(public_var.new_plccom)
        self.start_fl._signal.connect(self.start_flag, type=QtCore.Qt.DirectConnection)
        self.start_fl.start()
        # print(self.comboBox.currentText())
        # print(public_var.order_id)
    def read_config(self):
        read_ini = configparser.ConfigParser()
        read_ini.read('config.ini')
        public_var.new_pline = read_ini.get('test station', 'prod_line')
        public_var.new_cname = read_ini.get('test station', 'computer_name')
        public_var.new_plist = read_ini.get('test station', 'station_list')
        public_var.new_plccom = read_ini.get('server', 'plc_com')
        public_var.qcode_com = read_ini.get('server', 'qcode_com')
        public_var.server_ip = read_ini.get('server', 'server_ip')
        public_var.test_model = read_ini.get('test option', 'test_model')
        public_var.order_id = self.comboBox.currentText()
        # print(public_var.order_id)
    #PLC信号
    def start_flag(self,data):
        print('接收PLC信息：',data)
        if public_var.code_model: # 条码数量正确
            if data == 'A':
                try:
                    self.port_list = public_var.new_plist.split(",")
                    print(self.port_list)
                    public_var.dict1 = {'LED0': False, 'LED1': False, 'LED2': False, 'LED3': False, 'LED4': False, 'LED5': False,
                             'LED6': False, 'LED7': False, 'LED8': False, 'LED9': False, 'LED10': False, 'LED11': False,
                             'LED12': False, 'LED13': False, 'LED14': False, 'LED15': False}
                    # self.led_check = Led_code()
                    # self.led_check.start()

                    for i in self.port_list:
                        num = 'lineEdit_' + str(i)
                        name2 = 'lineEdit_' + i + '_10'
                        self.findChild(QWidget, name2).setStyleSheet('background-color:#fff')
                        for s in range(2, 11):
                            name = num + '_' + str(s)
                            self.findChild(QWidget, name).clear()
                    if public_var.test_method:
                        print('执行有条码模式')
                        for i in self.port_list:
                            start_i = int(i)-1
                            name = 'lineEdit_' + i + '_1'
                            model_id = self.findChild(QWidget,name).text()
                            self.start_rw = Read_write(win_id=start_i,model_id=model_id)
                            self.start_rw._signal.connect(self.mytest, type=QtCore.Qt.DirectConnection)
                            self.start_rw.start()
                            time.sleep(0.2)
                        public_var.code_model = False #初始化测试码
                    else:
                        print('执行无条码模式')
                        for i in self.port_list:
                            start_i = int(i)-1
                            self.Read_nocode = Read_nocode(win_id=start_i)
                            self.Read_nocode._signal.connect(self.mytest, type=QtCore.Qt.DirectConnection)
                            self.Read_nocode.start()
                except Exception as e:
                    print(e)
            else:
                print('PLC压合信号错误:',data)
                self.start_fl.ser.write('D'.encode('gbk'))
                self.check_error_log('PLC压合信号错误')
        else:
            self.start_fl.ser.write('D'.encode('gbk'))
            self.check_error_log('条码/扫码异常，请检测')
            self.work_stop()

    #测试结果
    def mytest(self,data):
        print(data)
        res_date_code = data.get('win')
        res_date = data.get('data')
        res_date_num = data.get('line_id')
        res_ngcode = data.get('ngcode')
        try:
            name = 'lineEdit_' + res_date_code + '_' + res_date_num
            # print(name)
            test = 'self.%s.setText(res_date)' % name
            eval(test)
            if res_date_num == '10' and res_ngcode == 'fail':
                name = 'lineEdit_' + res_date_code + '_10'
                datas = 'background-color:red;font-family:微软雅黑;color:#fff;font-weight:bold;font-size:14px'
                test = 'self.%s.setStyleSheet(datas)' %name
                eval(test)
                public_var.conut_num.append('0')
            elif res_date_num == '10' and res_ngcode =='pass':
                name = 'lineEdit_' + res_date_code + '_10'
                datas = 'background-color:green;font-family:微软雅黑;color:#fff;font-weight:bold;font-size:14px'
                test = 'self.%s.setStyleSheet(datas)' % name
                eval(test)
                public_var.conut_num.append('1')

            if len(public_var.conut_num) == len(self.port_list):
                self.start_fl.ser.write('C'.encode('gbk')) #发送抬起气缸命令
                conuts = ''.join(public_var.conut_num)
                res = {i: conuts.count(i) for i in conuts}
                l125 = '成功：'+ str(res.get('1'))
                l126 = '失败：' + str(res.get('0'))
                self.label_125.setText(l125)
                self.label_126.setText(l126)
                public_var.conut_num = []
        except Exception as e:
            print(e)

    #订单线程返回
    def order_res(self,res):
        res = json.loads(res)
        if res.get('respcode') and res.get('respcode') =='000000':
            try:
                # print(res)
                self.items = res.get('projectinfo')
                # a = [item[key] for item in items for key in item]
                order_list = ['--请选择指令单号--']
                for i in range(len(self.items)):
                    order_list.append(self.items[i]['order_id'])
                self.comboBox.addItems(order_list)
                self.comboBox.currentIndexChanged.connect(lambda:self.flag_change(self.comboBox.currentIndex()))
            except Exception as e:
                log.logging.error('<%s>' % str(e))
        else:
            self.check_error_log('订单信息获取失败，请联系管理人员')

    #订单更新函数
    def flag_change(self,tag):
        if tag != 0:
            order_option = [self.items[tag-1]['order_msg'],self.items[tag-1]['begin_id'],self.items[tag-1]['end_id']]
            # print(order_option)
            for i in range(len(order_option)):
                name = 'lineEdit_' + str(i+1)
                values = order_option[i]
                self.findChild(QWidget,name).setText(values)
            # self.pushButton.setEnabled(True)
            self.check_option_log('更新订单号成功')
        else:
            for i in range(3):
                name = 'lineEdit_' + str(i+1)
                self.findChild(QWidget,name).setText('暂无数据')



    def work_start(self):#启动按钮
        self.clear_text()
        if self.lineEdit_2.text() == '暂无数据':
            self.check_error_log('请先选择制令单号')
        else:
            self.comboBox.setEnabled(False)
            self.read_config()
            try:
                # test_model = read_ini.get('test option', 'test_model')
                if public_var.test_model == '0':
                    #启动正常模式
                    public_var.test_method = True
                    self.check_tip_log('当前模式：正常模式')
                    public_var.get_code = 1
                    self.get_barcode = Bar_code()#启动扫码枪通讯线程
                    self.get_barcode._signal.connect(self.res_barcode)
                    self.get_barcode.start()
                else:
                    self.check_tip_log('当前模式：无条码模式')
                    public_var.test_method = False #启动无条码模式
                    public_var.code_model = True
                    for i in range(1,9):
                        num = 'lineEdit_'+str(i)
                        for sv in range(1,7):
                            name = num + '_' + str(sv)
                            self.findChild(QWidget,name).setEnabled(False)
            except Exception as e:
                print(e)

            self.pushButton.setEnabled(False)
            self.pushButton.setStyleSheet('background-color:#ccc')
            self.pushButton_2.setEnabled(True)
            self.pushButton_2.setStyleSheet('background-color:#FF2121;font-family:微软雅黑;color:#fff;font-weight:bold')
            self.pushButton_3.setEnabled(False)
            self.check_option_log('start')
            self.win_list = public_var.new_plist
            #print(win_list)
            cho_station = ['1','2','3','4','5','6','7','8']

            if len(self.win_list) == len(cho_station):
                self.check_tip_log('工作端口全部打开')
                start_ser_list = 'BBBBBBBB'
            else:
                try:
                    inter = [i for i, v in enumerate(cho_station) if v not in self.win_list]
                    #self.checked_num = []
                    plc_num = ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
                    for i in inter:
                        num = cho_station[int(i)]
                        #self.checked_num.append(num)
                        plc_num[int(num)-1] = 'A'
                        self.check_tip_log('%s号工作端口已被关闭' %num)
                        for sta in range(10):
                            name = 'lineEdit_'+ num + '_' + str(sta+1)
                            self.findChild(QWidget, name).setText('[T01] %s # window is closed'%num)
                            # self.findChild(QWidget, name).setStyleSheet('color:#FF2121')
                            self.findChild(QWidget,name).setEnabled(False)
                    start_ser_list = ''.join(plc_num)
                    print(start_ser_list)
                except Exception as e:
                    log.logging.error('<%s>' % str(e))
            # 给plc传送开始命令和工作端口
            self.start_fl.ser.write(start_ser_list.encode('gbk'))

    ##扫码枪线程
    def res_barcode(self,code):
        code = code.split(',')
        code_length = len(code) - 1
        if code.count('NG') == 9:
            public_var.code_model = False  # 扫码异常
            self.start_fl.ser.write('D'.encode('gbk'))
            self.check_error_log('条码错误')
            self.work_stop()
            return
        try:
            for i in range(code_length):
                num = code[i]
                name_num = int(i) + 1
                name = 'lineEdit_'+ str(name_num) +'_1'
                self.findChild(QWidget, name).setText(num)
            public_var.code_model = True#扫码正常
        except Exception as e:
            print(e)
            print('条码数量错误')
            public_var.code_model = False#扫码异常
            self.start_fl.ser.write('D'.encode('gbk'))
            self.check_error_log('条码数量错误，请联系管理人员')
            self.work_stop()

    ###########
    # 工具类  #

    def work_stop(self):#停止按钮
        self.check_option_log('soft stop')
        # Start_code().exec()
        public_var.get_code = 0
        self.comboBox.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setStyleSheet('background-color:#ccc;font-family:微软雅黑;')
        self.pushButton.setEnabled(True)
        self.pushButton.setStyleSheet('background-color:#3D9140;color:#fff')
        self.pushButton_3.setEnabled(True)
    def sysbutton(self):#配置选项按钮
        self.child_window.show()
    def check_option_log(self,check_log):#正常
        now_time = datetime.datetime.now().strftime("%H:%M:%S")
        last_style = '<font color=\"#708090\">''[' + str(now_time) + ']：' + '[ run ] ''</font>' +check_log
        self.findChild(QWidget,'textBrowser').append(last_style)
    def check_tip_log(self,check_log):#提醒
        now_time = datetime.datetime.now().strftime("%H:%M:%S")
        last_style = '<font color=\"#FF7500\">''[' + str(now_time) + ']：' + '[ tip ] ''</font>' +check_log
        self.findChild(QWidget,'textBrowser').append(last_style)
    def check_error_log(self,check_log):#异常
        now_time = datetime.datetime.now().strftime("%H:%M:%S")
        last_style = '<font color=\"#ff2121\">''[' + str(now_time) + ']：' + '[ error ] ''</font>' +check_log
        self.findChild(QWidget,'textBrowser').append(last_style)
        log.logging.error('<%s>' % str(check_log))
    def clear_text(self):
        for i in range(1, 9):
            num = 'lineEdit_' + str(i)
            for sv in range(1, 11):
                name = num + '_' + str(sv)
                self.findChild(QWidget, name).setEnabled(True)
                self.findChild(QWidget, name).clear()

class Child_ui(QWidget,Ui_Form):#实例化配置选项窗口
    def __init__(self):
        super(Child_ui,self).__init__()
        self.setupUi(self)
        self.checkBox_99.setEnabled(False)
        self.checkBox_98.setEnabled(False)
        self.child_init()
        self.pushButton_2.clicked.connect(self.win_close)
        self.pushButton.clicked.connect(self.option_save)
        self.checkBox.stateChanged.connect(self.checkLanguage)
        self.temporary_d()
    def temporary_d(self):
        # 2020-10-30 16:21:29 临时关闭部分校验选项，改为mes服务校验
        self.checkBox_1.setEnabled(False)
        self.checkBox_2.setEnabled(False)
        self.groupBox_2.setEnabled(False)

    def checkLanguage(self,state):
        if state == QtCore.Qt.Unchecked:
            #print('取消选择了{0}: {1}')
            self.checkBox_1.setDisabled(False)
            self.checkBox_2.setDisabled(False)
            self.checkBox.setChecked(False)
            self.checkBox_1.setChecked(True)
            self.checkBox_2.setChecked(True)
        elif state == QtCore.Qt.Checked:
            #print('选择了{0}: {1}')
            self.checkBox_1.setDisabled(True)
            self.checkBox_2.setDisabled(True)
            self.checkBox.setChecked(True)
            self.checkBox_1.setChecked(False)
            self.checkBox_2.setChecked(False)
    def child_init(self):#初始化界面
        read_ini = configparser.ConfigParser()
        read_ini.read('config.ini')
        model = read_ini.get('test option','test_model')
        if model == '0':
            self.checkBox_1.setDisabled(False)
            self.checkBox_2.setDisabled(False)
            self.checkBox.setChecked(False)
        else:
            self.checkBox_1.setDisabled(True)
            self.checkBox_2.setDisabled(True)
            self.checkBox.setChecked(True)
        option_key = ['vendor_code', 'hw_version', 'user_type', 'external_version', 'fw_version']
        for i in range(5):
            version = read_ini.get('test option', option_key[i])
            name = 'lineEdit_' + str(i+1)
            self.findChild(QWidget,name).setText(version)
        option = read_ini.get('test option','option_list').split(',')
        option_list = list(option)
        for i in option_list:
            name = 'checkBox_'+ i
            #print(name)
            self.findChild(QCheckBox,name).setChecked(1)
        option = read_ini.get('test station', 'station_list')
        # print(option,1)
        if len(option) == 0:
            pass
        else:
            option = read_ini.get('test station', 'station_list').split(',')
            option_list = list(option)
            for i in option_list:
                num = int(i)+6
                name = 'checkBox_'+ str(num)
                self.findChild(QCheckBox,name).setChecked(1)

    def win_close(self):
        self.close()
    def option_save(self):
        read_ini = configparser.ConfigParser()
        read_ini.read('config.ini')
        #检测模式
        if self.checkBox.isChecked():
            read_ini.set('test option','test_model','1')
        else:
            read_ini.set('test option', 'test_model','0')
        #检测选项
        option_list = []
        for i in range(7):
            name = 'checkBox_' + str(i+1)
            try:
                if self.findChild(QWidget,name).isChecked():
                    option_list.append(i+1)
                else:
                    pass
            except Exception as e:
                print(e)
        try:
            read_ini.set('test option','option_list',",".join(str(i) for i in option_list))
        except Exception as e:
            print(e)
        #参数修改
        option_key = ['vendor_code','hw_version','user_type','external_version','fw_version']
        for i in range(1,6):
            #print(i)
            name = 'lineEdit_' + str(i)
            try:
                line_text = self.findChild(QWidget,name).text()
                #print(line_text)
                read_ini.set('test option',option_key[i-1],line_text)
            except Exception as e:
                print(e)
        #检测位关闭、开启
        window_id = []
        for i in range(8):
            num = i + 7
            name = 'checkBox_'+str(num)
            if self.findChild(QWidget,name).isChecked():
                window_id.append(i+1)
            else:
                pass
        read_ini.set('test station','station_list',",".join(str(i) for i in window_id))
        read_ini.write(open("config.ini", "w"))
        self.close()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = Main_ui()
    a.show()
    sys.exit(app.exec_())