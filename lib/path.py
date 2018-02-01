#-*- coding:utf8 -*-
import os

'''GET类：判断程序更目录、配置文件目录、日志目录、数据库目录、等'''
class GET(object):
    def __init__(self):
        self.get_root_path()
        #self.rootpath = ''

    #根目录
    def get_root_path(self):
        if os.path.basename(os.path.abspath('.')) == 'lib':
            self.rootpath = os.path.dirname(os.path.abspath('.'))
        else:
            self.rootpath = os.path.abspath('.')
        #print self.rootpath
        return self.rootpath
    #配置文件目录
    def get_conf_path(self):
        #print os.path.join(self.rootpath,'ini')
        return os.path.join(self.rootpath,'ini')
    #日志文件目录
    def get_log_path(self):
        #print os.path.join(self.rootpath,'log')
        return os.path.join(self.rootpath,'log')
    #数据库文件目录
    def get_db_path(self):
        return os.path.join(self.rootpath,'db')

'''CREATE类：创建程序需要使用到的可配置目录'''
class CREATE(object):

    def __init__(self):
        pass;
    def create_path(self,extra_path):
        #获取extra_path的绝对路径，并创建目录
        #print os.path.dirname(os.path.abspath(extra_path))
        if not os.path.isdir(os.path.dirname(os.path.abspath(extra_path))):
            os.makedirs(os.path.dirname(os.path.abspath(extra_path)))
        else:
            return




if __name__  == "__main__":
    test = GET()
    print test.get_root_path()
    print test.get_conf_path()
    print test.get_log_path()
    test2 = CREATE()
    test2.create_path(extra_path='../../test.log')
    #print test2.create_dir(extra_path='../../test.log')
    #print test2.create_dir(extra_path='../haha')
   # print test2.create_dir(extra_path='./haha')
    #print test.


