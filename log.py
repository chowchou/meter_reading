# import logging,os,sys,time
#
# def make_dir(make_dir_path):
#     path = make_dir_path.strip()
#     if not os.path.exists(path):
#         os.makedirs(path)
#     date = time.strftime("%Y-%m-%d")
#     newpath = path+ '/' + date+'.log'
#     return newpath
#
# # 当前文件路径
# if getattr(sys, 'frozen', False):
#     pathname = sys._MEIPASS
# else:
#     pathname = os.path.split(os.path.realpath(__file__))[0] #获取上级目录的绝对路径
#     print(pathname)
#
# log_dir = pathname + '/log'
#
#
#
# # 初始化日志配置
# logging.basicConfig(
#     # 日志级别,logging.DEBUG,logging.ERROR
#     level = logging.INFO,
#
#     # 日志格式
#     # 时间、代码所在文件名、代码行号、日志级别名字、日志信息
#     # format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#     format= '[%(asctime)s] [%(levelname)s] %(message)s',
#
#     # 打印日志的时间
#     datefmt = '%Y-%m-%d %H:%M:%S',
#
#     # 日志文件存放的目录（目录必须存在）及日志文件名
#     filename = make_dir(log_dir),
#
#     # 打开日志文件的方式
#     filemode = 'a+'
# )


import logging as lg
import os
from logging import handlers



class MyLog:
    logger=None
    def __init__(self,name,filename='log.log'):
        self.logger = lg.getLogger(name)
        self.logger.setLevel(lg.INFO)
        format = '[%(asctime)s] [%(levelname)s] %(message)s'
        datefmt = '%Y-%m-%d %H:%M:%S'
        log_path = os.path.join(os.getcwd(), "log")
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        log_filepath = os.path.join(log_path, filename)
        th = handlers.TimedRotatingFileHandler(filename=log_filepath,when='midnight',encoding='utf-8')
        th.setFormatter(lg.Formatter(format,datefmt))
        self.logger.addHandler(th)
        console = lg.StreamHandler()
        console.setLevel(lg.INFO)
        console.setFormatter(lg.Formatter(format,datefmt))
        self.logger.addHandler(console)


def getLogger(name):
    mylog=MyLog(name)
    return mylog.logger

logging=getLogger(__name__)