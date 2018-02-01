#-*- coding:utf8 -*-
from ftplib import FTP
from lib.logger import Log_marker
from lib.configuration import Config_reader
import os
class FTP_marker(object):
    def __init__(self):
        self.config = Config_reader()
        #self.logger = Log_marker().log_marker(log_path=self.config.get_value(section='LOGGER',key='LOG_PATH'),log_level=self.config.get_value(section='LOGGER',key='LOG_LEVEL'))
    '''
    ftpconnect函数：ftp服务器登录
    '''
    def ftpconnect(self,host,user,password,port,timeout):
        try:
            self.ftp = FTP()
            self.ftp.set_debuglevel(0)
            self.ftp.connect(host,port,float(timeout))
            self.ftp.login(user,password)
            return 'login_ok'
            #self.logger.debug('Server: %s User: %s Login successful' % (host, user))
        except Exception as e:
            return 'login_failed', e

    def list(self,remotepath):
        if not remotepath.endswith("/"):
            remotepath = remotepath + '/'
        else:
            remotepath = remotepath
        try:
            return self.ftp.nlst(remotepath)
        except Exception as e:
            return 'list_failed', e
    '''
    ftpget函数：下载文件
    '''
    def ftpget(self,localfile,remotefile,localpath,remotepath):
        if not localpath.endswith("/"):
            localpath = localpath + '/'
        else:
            localpath = localpath

        if not remotepath.endswith("/"):
            remotepath = remotepath + '/'
        else:
            remotepath = remotepath
        try:
            fp = open(localpath + localfile,'wb')
            self.ftp.cwd(remotepath)
            self.ftp.retrbinary('RETR ' + remotefile, fp.write)
            return 'get_ok'
            #self.logger.debug('%s File send OK'% remotefile)
        except Exception as e:
            os.remove(localpath + localfile)
            return 'get_failed', e
    '''
    ftpput函数：上传文件
    '''
    def ftpput(self,localfile,remotefile,localpath,remotepath):
        if not localpath.endswith("/"):
            localpath = localpath + '/'
        else:
            localpath = localpath

        if not remotepath.endswith("/"):
            remotepath = remotepath + '/'
        else:
            remotepath = remotepath
        try:
            fp = open(localpath + localfile, 'rb')
            self.ftp.cwd(remotepath)
            self.ftp.storbinary('STOR ' + remotefile, fp)
            return 'put_ok'
        except Exception as e:
            return 'put_failed', e

    def quit(self):
        self.ftp.quit()

if __name__ == '__main__':
    config = Config_reader()
    host=config.get_value(section='FTP',key='HOST')
    test = FTP_marker()
    test1 = test.ftpconnect(host=host,user='ssetest',password='68791151',port='21',timeout='10')
    if test1 == 'login_ok':
        print test1
        test2 = test.ftpget(localfile='123',remotefile='lib.zip',localpath='/root/',remotepath='/MAAS/yxh/')
        if test2 == 'get_ok':
            print test2
        else:
            a, b = test2
            print 'fuck1 %s' % b
        test3 = test.ftpput(localfile='123',remotefile='123.zip',localpath='/root/',remotepath='/MAAS/yxh')
        print test3
    else:
        a,b = test1
        print 'fuck2 %s' %b
