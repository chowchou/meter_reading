#####
#公共变量
#####
import os
dict1 = {'LED0': False, 'LED1': False, 'LED2': False, 'LED3': False, 'LED4': False, 'LED5': False,
                         'LED6': False, 'LED7': False, 'LED8': False, 'LED9': False, 'LED10': False, 'LED11': False,
                         'LED12': False, 'LED13': False, 'LED14': False, 'LED15': False}  # LED灯变量
get_code = 0   # 扫码枪开关
init_path = os.getcwd()
test_model = ''  # 测试模式
new_pline = ''  # 线别
new_cname = ''  # 机台名
new_plist = ''  # 测试列表
new_plccom = ''  # plc串口号
qcode_com = ''  # 扫码枪串口号
server_ip = ''  # mes地址
conut_num = []
order_id = ''  # 制令单号
code_model = False  # 条码数量是否正常
test_method = True  # 有条码、无条码方式