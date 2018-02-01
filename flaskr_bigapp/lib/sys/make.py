#-*- coding:utf8 -*-
import os

class GET(object):
    '''获取程序目录类'''
    def __init__(self):
        self.basedir, path = os.path.split(os.path.dirname(os.path.abspath('')))

    def get_base_dir(self):
        return self.basedir

    def get_conf_dir(self):
        return os.path.join(self.basedir,'conf')

    def get_log_dir(self):
        return os.path.join(self.basedir,'log')

    def get_db_dir(self):
        return os.path.join(self.basedir,'db')

class CREATE(object):
    '''创建目录类'''
    def __init__(self):
        pass;
    def create_dir(self,extra_path,basepath=None):
        if os.path.dirname(extra_path) == '..' or os.path.dirname(extra_path) == '.' or os.path.dirname(extra_path) == '':
            if not os.path.exists(os.path.dirname(os.path.join(basepath,extra_path)).strip()):
                os.makedirs(os.path.dirname(os.path.join(basepath,extra_path)).strip())
            return os.path.join(basepath,extra_path)
        else:
            if not os.path.exists(os.path.dirname(extra_path).strip()):
                os.makedirs(os.path.dirname(extra_path).strip())
                os.path.dirname(extra_path).strip()
            return extra_path



if __name__  == "__main__":
    test = GET()
    print test.get_dir()


