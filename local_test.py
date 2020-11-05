# import binascii
# from time import sleep
# import serial
# ser = serial.Serial('COM15',115200,timeout=5000)
# ser.flushInput()#清空缓存区  必要
# # a = '68 BB BB BB BB BB BB 68 1C 04 00 FF FF FF FF 4E 16'
# # up_power = '68 BB BB BB BB BB BB 68 1A 04 00 14 26 27 2B DC 16'
# # while True:
# #     ser.write(obj_write_info)
# #     sleep(0.5)
# #     print(obj_write_info)
# #     if ser.in_waiting:
# #         c = ser.read(ser.in_waiting).decode("GBK")
# #         print(c)
# #         break
#
# transmission = '68 BB BB BB BB BB BB 68 1C 04 00 FF FF FF FF 4E 16' #开启数据透传
# close_charging = '23 23 00 00 00 00 00 00 00 00 00 00 00 00 03 00 00 00 2d 00 00 00 06 00 00 00 2d 00 00 00 00 00 40 40' #关闭电容充电
# get_sn = '23 23 00 00 00 00 00 00 00 00 00 00 00 00 03 00 00 00 2b 00 00 00 06 00 00 00 2b 00 00 00 00 00 40 40'#获取6位SN
# get_id = '23 23 00 00 00 00 00 00 00 00 00 00 00 00 03 00 00 00 3e 00 00 00 06 00 00 00 3e 00 00 00 00 00 40 40'#获取11位模块ID
# chip_mmid = '23 23 00 00 00 00 00 00 00 00 00 00 00 00 03 00 00 00 38 00 00 00 06 00 00 00 38 00 00 00 00 00 40 40' #获取24位国网ID
# close_trans = '68 BB BB BB BB BB BB 68 1C 04 00 F0 F0 F0 F0 12 16'#关闭数据透传
# up_power = '68 BB BB BB BB BB BB 68 1A 04 00 14 26 27 2B DC 16' #上电
# down_power = '68 BB BB BB BB BB BB 68 1B 04 00 2B 28 27 14 DF 16' #下电
# try:
#     obj_write_info = transmission.replace(" ", "")
#     obj_write_info = binascii.a2b_hex(obj_write_info)
#     print(obj_write_info)
#     # ser.write(obj_write_info)
#     # res = ser.read(ser.in_waiting).decode("GBK")
#     # print(res)
#     if ser.isOpen():
#         print('serial is open')
#         ser.write(obj_write_info)
#         while True:
#             c = ser.read(ser.in_waiting)
#             c = c.hex().upper()
#             if c != '':
#                 print(c)
#                 break
#         print('关闭电容充电')
#         ser.flushInput()
#         obj_write_info = binascii.a2b_hex(close_charging.replace(" ", ""))
#         ser.write(obj_write_info)
#         sleep(0.5)
#         c = ser.read(ser.in_waiting).hex().upper()
#         # c = c.hex().upper()
#         if c != '':
#             print(c)
#         sleep(0.1)
#         print('国网ID')
#         ser.flushInput()
#         obj_write_info = chip_mmid.replace(" ", "")
#         obj_write_info = binascii.a2b_hex(obj_write_info)
#         ser.write(obj_write_info)
#         sleep(0.5)
#         c = ser.read(1)
#         c = c + ser.readline(ser.in_waiting)
#         c = c.hex().upper()
#         if c != '':
#             print(c)
#             print(len(c))
#             a = c[-52:-4]
#             print(a)
#         print('写入国网ID')
#         id = '111111111111111222222111111111111111111111111111'
#         a = '23 23 00 00 00 00 00 00 00 00 00 00 00 00 03 00 00 00 48 00 00 00 1E 00 00 00 48 00 18 00 18 00 %s 40 40 ' % id
#         obj_write_info = a.replace(" ", "")
#         obj_write_info = binascii.a2b_hex(obj_write_info)
#         ser.write(obj_write_info)
#         sleep(0.3)
#         c = ser.read(ser.in_waiting).hex().upper()
#         if c != '':
#             print(c)
#
#         print('模块ID')
#         ser.flushInput()
#         obj_write_info = get_id.replace(" ", "")
#         obj_write_info = binascii.a2b_hex(obj_write_info)
#         ser.write(obj_write_info)
#         sleep(0.5)
#         c = ser.read(1)
#         c = c + ser.read(ser.in_waiting)
#         c = c.hex().upper()
#         if c != '':
#             print(c)
#             a = c[-26:-4]
#             print(a)
#         sleep(0.1)
#         print('SN')
#         ser.flushInput()
#         obj_write_info = get_sn.replace(" ", "")
#         obj_write_info = binascii.a2b_hex(obj_write_info)
#         ser.write(obj_write_info)
#         sleep(0.5)
#         c = ser.read(1)
#         c = c + ser.read(ser.in_waiting)
#         c = c.hex().upper()
#         if c != '':
#             print(c)
#             a = c[-16:-4]
#             print(a)
#         sleep(0.1)
#         #sleep(3)
#         print('结束')
#         ser.flushInput()
#         obj_write_info = close_trans.replace(" ", "")
#         obj_write_info = binascii.a2b_hex(obj_write_info)
#         ser.write(obj_write_info)
#         sleep(0.5)
#         c = ser.read(1)
#         c = c + ser.read(ser.in_waiting)
#         c = c.hex().upper()
#         print(c)
#         sleep(1)
#     else:
#         print('no')
#     # while True:
#     #     if ser.in_waiting:
#     #         c = ser.read(ser.in_waiting)
#     #         print(c)
#     #         break
# except Exception as e:
#     print(e)

dict1 = {'LED0': False, 'LED1': False, 'LED2': False, 'LED3': False, 'LED4': False, 'LED5': False,
                         'LED6': False, 'LED7': False, 'LED8': False, 'LED9': False, 'LED10': False, 'LED11': False,
                         'LED12': False, 'LED13': False, 'LED14': False, 'LED15': False}

a = ['1111','2222']
b = True
if a:
    print('成功')
else:
    print('jia')
