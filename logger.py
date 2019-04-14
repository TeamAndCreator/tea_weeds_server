import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

import coloredlogs

# 获取logger实例，如果参数为空则返回root logger
logger = logging.getLogger()

# 指定logger输出格式
formatter = logging.Formatter(
    fmt='%(asctime)s: %(levelname)-1.1s %(pathname)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d,%H:%M:%S')

# 文件日志

log_dir = "./logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
# fileLog=logging.FileHandler("."+os.sep+"CustomLog_"+dataStr+'.log')
file_handler = TimedRotatingFileHandler(filename="{}/log".format(log_dir),
                                        when="midnight", interval=1,
                                        backupCount=4)
# file_handler = logging.FileHandler("log.log")
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值

# 为logger添加的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 指定日志的最低输出级别，默认为WARN级别
# logger.setLevel(logging.DEBUG)

# 控制台日志着色
coloredlogs.install(level='DEBUG', logger=logger,
                    fmt='%(asctime)s: %(levelname)-1.1s %(pathname)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d,%H:%M:%S.%f', stream=sys.stdout)

if __name__ == "__main__":
    logger.warning("I'm a warning!")
    logger.info("Hello, Python!")
    logger.debug("I'm a debug message!")