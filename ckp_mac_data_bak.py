# 接收数据
def start_data():
    recv_data = input("\t请输入载波读取的数据：\n\t")
    recv_data = recv_data.strip()
    print(recv_data)
    if len(recv_data) >= 239:
        print("{:#<245}\n".format('\t解析数据 '))
        # print(receive_data)
        print(recv_data.split())
        recv_data = recv_data.split()[10:78]
        print(recv_data)

        return recv_data
    else:
        print("\t输入数据不完整，请重新输入！\n")
        return 0


# 截取报文数据区， 减 33 处理
def no_33(recv_data):
    data_temp = []
    for i in recv_data:
        # 转换为 16进制 依据645-13协议 减去33
        i = eval('0x' + i) - 0x33
        # 处理 减33后，i 为负值的情况
        if '-' in str(i):
            i = i + 0xFF + 1

        # 将 16进制i 转换为 字符串
        i = str("%02X" % i)
        # print(i, end=", ")

        # 添加 i 到列表 data_temp
        data_temp.append(i)
        # print(len(data_temp), data_temp)
    return data_temp


# FW_read     ### 解析软件版本 ###
def fw_read(recv_data):
    # 截取软件版本数据
    fw_version_temp = recv_data[5:9]
    fw_version_temp.reverse()  # 列表反序
    # print(fw_version_temp)

    fw_num = ""
    for i in fw_version_temp:
        # i = '0x' + i
        fw_num += "%02X" % (eval('0x' + i))  # 输出两位十六进制，字母大写，空缺补零
        # print(fw_num)

    fw_num = int(fw_num, 16)  # 转化为 10进制
    # print(fw_num)

    # 解析软件版本
    fw_major = str(fw_num >> 27) + "."
    fw_minor = str((fw_num & 0x7F00000) >> 20) + "."
    fw_micor = str((fw_num & 0xF0000) >> 16) + "."
    fw_build = str(fw_num & 0xFFFF)
    firmware_version = fw_major + fw_minor + fw_micor + fw_build
    print('\t 软件版本：', firmware_version)


# hd_read     ### 解析硬件版本 ###
def hd_read(recv_data):
    hd_version_temp = recv_data[57:61]
    hd_version_temp.reverse()  # 列表反序
    # print(hd_version_temp)
    hd_version = ''
    for i in range(len(hd_version_temp)):
        hd_version += str(int(hd_version_temp[i], 16)) + '.'

    hd_version = hd_version.rstrip('.')
    print('\t 硬件版本：', hd_version)


# CRC校验   Flash_CRC   00:PASS  /  01:Fail
def crc_checkdata(recv_data):
    crc_temp = recv_data[56]
    if int(crc_temp, 16):
        crc_check = 'Fail'
    else:
        crc_check = 'Pass'
    print("\t CRC 验证：", crc_check)


# 校验厂商代码
def vendor_code_check(recv_data):
    vendor_code_temp = recv_data[19:21]
    vendor_code_temp.reverse()  # 列表反转
    vendor_code_data = ''
    for i in vendor_code_temp:
        i = eval('0x' + i)
        vendor_code_data += chr(i)
    print("\t 厂商代码：", vendor_code_data)


# 解析PCB_SN
def pcb_sn_read(recv_data):
    pcb_sn_temp = recv_data[61:67]
    pcb_sn = ''
    for i in pcb_sn_temp:
        pcb_sn += "%02X" % (eval('0x' + i))
    print("\t SN 码  ： ", pcb_sn)


# 解析壳体条码
def shell_read(recv_data):
    shell_code_temp = recv_data[21:32]
    shell_code_temp.reverse()  # 列表反转
    shell_code = ''
    for i in shell_code_temp:
        shell_code += i
    print("\t 壳体条码：", shell_code)


# 解析芯片ID
def key_id_read(recv_data):
    key_id_temp = recv_data[32:56]
    key_id_temp.reverse()  # 列表反转
    key_id = ''
    for i in key_id_temp:
        key_id += i
    print("\t 芯片 ID： ", key_id)


# 解析函数
def data_analysis_temp():
    pcb_sn_read(no_33_data)
    shell_read(no_33_data)
    key_id_read(no_33_data)
    fw_read(no_33_data)
    hd_read(no_33_data)
    vendor_code_check(no_33_data)
    crc_checkdata(no_33_data)
    print("\n")


# 主函数
while True:
    receive_data = start_data()
    if receive_data != 0:
        no_33_data = no_33(receive_data)
        data_analysis_temp()
