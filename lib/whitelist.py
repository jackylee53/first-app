#-*- coding:utf8 -*-
from lib.configuration import Config_reader
from lib.logger import Log_marker
from lib.ftp import FTP_marker
from lib.path import GET,CREATE
import os,shutil,time,re,glob,subprocess,signal
from lib.scheduler import Schedulers

'''
编写者：袁向豪
版本号：V1.0.1
添加一个将执行结果，更新文件与更新时间记录到sqite数据库的方法。
支持html页面展示结果
支持后台守护
'''
class Get_whitelist(object):
    def __init__(self):
        self.config = Config_reader()
        self.ftp = FTP_marker()
        self.createpath = CREATE()
        #检查目录是否存在，如果不存在创建日志文件
        self.createpath.create_path(extra_path=self.config.get_value(section='LOGGER',key='LOG_PATH'))
        #self.logger1 = Log_marker().log_marker(log_path=self.config.get_value(section='LOGGER',key='LOG_PATH'),
                                              #log_level=self.config.get_value(section='LOGGER',key='LOG_LEVEL'),
                                              #log_name='apscheduler.scheduler')
        self.logger = Log_marker().log_marker(log_path=self.config.get_value(section='LOGGER',key='LOG_PATH'),
                                              log_level=self.config.get_value(section='LOGGER',key='LOG_LEVEL'),
                                              log_name=self.config.get_value(section='LOGGER',key='LOG_NAME'))


    def ftp_get_whitelist(self,local,remote,localp,remotep):
        result = self.ftp.ftpget(localfile=local,
                                 remotefile=remote, localpath=localp,
                                 remotepath=remotep)
        if result == 'get_ok':
            self.logger.info('%s File update success' % remote)
            if not os.path.isfile('/mds/aac/aac_V1.0.2/bin/restart_auth.sh'):
                self.logger.error('/mds/aac/aac_V1.0.2/bin/restart_auth.sh No such file or directory')
            else:
                os.popen("sh /mds/aac/aac_V1.0.2/bin/restart_auth.sh")
                self.logger.info('authentication Service restart success')
            #执行成功后写入数据库的案例
            #a = 'OK'
            #return a
        else:
            msg, error = result
            self.logger.error(error)

    def whitelist(self):
        list=[]
        host = self.config.get_value(section='FTP',key='HOST')
        user = self.config.get_value(section='FTP',key='USER')
        password = self.config.get_value(section='FTP',key='PASS')
        port = self.config.get_value(section='FTP',key='PORT')
        timeout = self.config.get_value(section='FTP',key='TIMEOUT')
        qsidlist = self.config.get_value(section='FTP',key='QSID').split(',')
        #print qsidlist
        localpath = self.config.get_value(section='SYSTEM',key='WHITELIST_DIR')
        backpath = self.config.get_value(section='SYSTEM',key='BACKUP_DIR')
        remotepath = self.config.get_value(section='FTP',key='REMOTE_DIR')
        login = self.ftp.ftpconnect(host=host,user=user,password=password,port=port,timeout=timeout)
        if login == 'login_ok':
            self.logger.debug('230 Login successful')
            #使用qsid作为主循环，支持对多个券商ID进行更新
            year = time.strftime("%Y")
            month = time.strftime("%m")
            #print year,month
            # 检查本地文件是否与配置中的qsid匹配，匹配后记录文件中的时间戳
            for qsid in qsidlist:
                #先检查ftp中年月目录里面的日期，并生产为一个列表。通过max函数将列表中做最大的值去除。这样就取出了最新白名单文件所在的目录
                for daylist in self.ftp.list('%s%s/%s'%(remotepath,year,month)):
                    list.append(os.path.basename(daylist))
                day = max(list)
                #列出ftp中最新日期的所有文件，并匹配qsid和csv。取出需要下载的文件。
                for filelist in self.ftp.list('%s%s/%s/%s'%(remotepath,year,month,day)):
                    for file in self.ftp.list(filelist):
                        #正则匹配，取出符合qsid的并以csv结尾的文件
                        if re.match('%s.*.csv$'%qsid,os.path.basename(file)):
                            #print os.path.basename(file)
                            #print qsid
                            #查看当前目录中的qsid文件是否有文件，并取出时间戳进行时间的比对。时间大于当前时间的才进行更新，不大于的不进行更新
                            os.chdir(localpath)
                            if not glob.glob('%s*csv'%qsid):
                                print self.ftp_get_whitelist(local=os.path.basename(file),remote=os.path.basename(file),localp=localpath,remotep=os.path.dirname(file))
                            elif glob.glob('%s*csv'%qsid):
                                backfile = glob.glob('%s*csv'%qsid)[0]
                                if time.mktime(time.strptime(file.split('_')[1].split('.')[0], '%y%m%d')) > time.mktime(
                                        time.strptime(backfile.split('_')[1].split('.')[0], '%y%m%d')):
                                    if os.path.exists(backpath+backfile):
                                        os.remove(backpath+backfile)
                                    else:
                                        shutil.move(localpath + backfile, backpath)
                                    print self.ftp_get_whitelist(local=os.path.basename(file), remote=os.path.basename(file),
                                                       localp=localpath, remotep=os.path.dirname(file))
                                else:
                                    self.logger.debug('File do not need to be replaced')
            self.ftp.quit()
        else:
            msg, error = login
            self.logger.error(error)
            self.ftp.quit()

    def main(self):
        sched = Schedulers()
        sched.background(self.whitelist, week=self.config.get_value(section='SCHEDULER', key='WEEK'),
                         hour=self.config.get_value(section='SCHEDULER', key='HOUR'),
                         minute=self.config.get_value(section='SCHEDULER', key='MINUTE'),
                         second=self.config.get_value(section='SCHEDULER', key='SECOND'))

if __name__ == "__main__":
    play = Get_whitelist()
    play.main()





