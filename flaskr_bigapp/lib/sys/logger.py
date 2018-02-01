#-*- coding: utf8 -*-
import logging,logging.handlers
import sys
import os
from flaskr_bigapp.lib.sys.configuration import Config_read
from flaskr_bigapp.lib.sys.make import GET,CREATE

'''
定义一个初始化函数，主要用来定义一个日志等级的函数
'''
class Logger(object):
    def __init__(self,external_path,logger_name='root'):
        self.logger_name = logger_name
        self.path = external_path
        self.__initalizeData()
        self.__timeroating_kind()
        self.__file_kind()
        self.__stream_kind()



    def __initalizeData(self):
        self.basepath = GET().get_log_dir()
        self.create_dir = CREATE()
        self.config_items = Config_read()
        self.local_path = self.create_dir.create_dir(basepath=self.basepath,extra_path=self.config_items.get_value(sections='LOGGER_DIR', key='GLOBAL_LOG_FILE'))
        self.external_path = self.create_dir.create_dir(basepath=self.basepath,extra_path=self.path)
        self.logger = logging.getLogger(self.logger_name)

    def level(self,level_name):
        if level_name == 'DEBUG':
            self.level_return = logging.DEBUG
        elif level_name == 'INFO':
            self.level_return = logging.INFO
        elif level_name == 'WARNING':
            self.level_return = logging.WARNING
        elif level_name == 'ERROR':
            self.level_return = logging.ERROR
        elif level_name == 'CRITICAL':
            self.level_return = logging.CRITICAL
        else:
            self.level_return = logging.INFO
        return self.level_return

    def __self_logger(self,message):
        self.logger = logging.getLogger()
        st_handler = logging.StreamHandler()
        st_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] %(filename)s[line:%(lineno)d] - %(message)s'))
        rf_handler = logging.handlers.TimedRotatingFileHandler(self.local_path, when='midnight', interval=1,
                                                               backupCount=7, )
        rf_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] %(filename)s[line:%(lineno)d] - %(message)s'))
        self.logger.addHandler(rf_handler)
        self.logger.addHandler(st_handler)
        self.logger.critical(message)
        sys.exit(1)

    def __timeroating_kind(self):
        try:
            self.logger.setLevel(self.level(level_name=self.config_items.get_value(sections='LOGGER', key='GLOBAL_LOG_LEVEL')))
            rf_handler = logging.handlers.TimedRotatingFileHandler(self.local_path, when='midnight', interval=1, backupCount=7,)
            rf_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] %(filename)s[line:%(lineno)d] - %(message)s'))
            self.logger.addHandler(rf_handler)
        except Exception as e:
            self.__self_logger(message=e)


    def __file_kind(self):
        try:
            f_handler = logging.FileHandler(self.external_path)
            f_handler.setLevel(self.level(level_name=self.config_items.get_value(sections='LOGGER', key='FILE_LOG_LEVEL')))
            f_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] %(filename)s[line:%(lineno)d] - %(message)s'))
            self.logger.addHandler(f_handler)
        except Exception as e:
            self.__self_logger(message=e)

    def __stream_kind(self):
        try:
            st_handler = logging.StreamHandler()
            st_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] %(filename)s[line:%(lineno)d] - %(message)s'))
            st_handler.setLevel(self.level(level_name=self.config_items.get_value(sections='LOGGER', key='STREAM_LOG_LEVEL')))
            self.logger.addHandler(st_handler)
        except Exception as e:
            self.__self_logger(message='System crash: %s!' %e)

    def debug(self,message):
        self.logger.debug(message)

    def info(self,message):
        self.logger.info(message)

    def warning(self,message):
        self.logger.warning(message)

    def error(self,message):
        self.logger.error(message)

    def critical(self,message):
        self.logger.critical(message)

if __name__ == '__main__':
    example = Logger(logger_name='example',external_path='/var/log/messages.log')
    example.debug('example debug info')

