#-*- coding: utf-8 -*-
import os,ConfigParser
from lib.default_cfg import Default
from lib.path import GET

class Config_reader(object):
    def __init__(self):
        path = GET()
        self.rootpath = path.get_root_path()
        self.confpath = path.get_conf_path()
        self.config_file = os.path.join(self.confpath,'conf.ini')
        self.__getdefault()

    def __getdefault(self):
        '''获取配置项的默认值字典'''
        self.default_config = Default().default_config()

    def get_value(self,section,key):
        self.config = ConfigParser.SafeConfigParser(self.default_config[section],allow_no_value=True)
        self.config.read(self.config_file)
        self.value = self.config.get(section,key)
        '''检测配置项的值是否误配置为None或者空字符。如果是的话,返回默认值'''
        if self.value is None:
            self.return_value = self.default_config[section][key]
        elif self.value == "":
            self.return_value = self.default_config[section][key]
        else:
            self.return_value = self.value
        '''返回结果值'''
        return self.return_value

if __name__ == '__main__':
    test = Config_reader()
    print test.get_value(section='LOGGER',key='LOG_LEVEL')
    print test.get_value(section='LOGGER',key='LOG_PATH')
    print test.get_value(section='FTP',key='HOST')
    print test.get_value(section='FTP',key='USER')
    print test.get_value(section='FTP',key='PASS')
    print test.get_value(section='FTP',key='PORT')


