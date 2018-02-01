#-*- coding: utf-8 -*-
import os
import ConfigParser
import logging
import logging.handlers
import sys
from flaskr_bigapp.lib.cfg.default_cfg import Default
from flaskr_bigapp.lib.cfg.range_cfg import Range
from flaskr_bigapp.lib.sys.make import GET,CREATE

class Config_read(object):
    def __init__(self):
        self.basepath = GET().get_base_dir()
        self.config_file = os.path.join(self.basepath,'conf','system.ini')
        self.create_dir = CREATE()
        self.__getdefault()
        self.__getrange()

    def __getdefault(self):
        '''获取配置项的默认值字典'''
        self.default_config = Default().default_config()

    def __getrange(self):
        '''获取配置项的配置范围字典'''
        self.range_config = Range().range_config()

    def __self_logger(self,message):
        '''使用logging模块，将日志导出'''
        self.local_path = self.create_dir.create_dir(basepath=self.basepath,extra_path=self.get_value(sections='LOGGER_DIR',key='GLOBAL_LOG_FILE'))
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

    def get_value(self,sections,key):
        self.config = ConfigParser.SafeConfigParser(self.default_config[sections],allow_no_value=True)
        self.config.read(self.config_file)
        self.value = self.config.get(sections,key)
        '''检测配置项的值是否误配置为None或者空字符。如果是的话,返回默认值'''
        if self.value is None:
            self.return_value = self.default_config[sections][key]
        elif self.value == "":
            self.return_value = self.default_config[sections][key]
        else:
            self.return_value = self.value
        '''检测配置项目是否符合默认的范围规则'''
        for range_key,range_value in self.range_config.items():
            for sub_range_key,sub_range_value in range_value.items():
                if key in sub_range_key:
                    if self.value in sub_range_value:
                       self.return_value = self.value
                    else:
                        self.__self_logger(message='%s setting is not correct!'%key)

        '''返回结果值'''
        return self.return_value

if __name__ == '__main__':
    test = Config_read()
    print test.get_value(sections='LOGGER',key='STREAM_LOG_LEVEL')

