#!_*_coding:utf-8_*_
"""
handle all the logging works
"""

import logging
from conf import settings
import time
import re

def logger(log_type):

    # create logger
    my_logger = logging.getLogger(log_type)
    my_logger.setLevel(settings.LOG_LEVEL)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(settings.LOG_LEVEL)

    # create file handler and set level to warning
    log_file = "%s/log/%s" % (settings.BASE_DIR, settings.LOG_TYPES[log_type])
    fh = logging.FileHandler(log_file)
    fh.setLevel(settings.LOG_LEVEL)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to logger
    my_logger.addHandler(ch)
    my_logger.addHandler(fh)
    return my_logger


def get_log_info(account):
    """ 将日志的内容进行转换后返回相应账号的转款信息

    :param account: 账号参数
    :return:
    """
    temp_list = []
    log_file = "%s/log/%s" % (settings.BASE_DIR, settings.LOG_TYPES['transaction'])
    with open(log_file, 'r') as f:
        for i in f:
            log_mat = re.search('(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}).*account:(.*?)\s.*action:(.*?)\s.*amount:(.*?)\s.*interest:(.*)',i)
            datetime = time.strptime(log_mat.group(1),'%Y-%m-%d %H:%M:%S')
            account_id = log_mat.group(2)
            action = log_mat.group(3)
            amount = log_mat.group(4)
            interest = log_mat.group(5)
            if account_id == account:
                temp_list.append([datetime,action,amount,interest])
    return temp_list