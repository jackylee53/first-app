#-*- coding:utf8 -*-
from ftplib import FTP
from lib.configuration import Config
from lib.logger import Log_marker
import datetime,os,shutil,time,re

'''
改进内容，支持多个qsid
支持html页面展示结果
支持后台守护
'''
class Get_whitelist(object):
    def __init__(self):
        self.config_reader = Config()
        self.logger = Log_marker().log_marker(log_path=self.config_reader.get_value(sections='LOGGER',key='LOG_PATH'),log_level=self.config_reader.get_value(sections='LOGGER',key='LOG_LEVEL'))
        self.today = datetime.datetime.now().strftime('%y%m%d')
        self.qsidlist = self.config_reader.get_value(sections='FTP',key='QSID').split(',')
        print self.qsidlist
        self.localdir = self.get_value(sections='PATH',key='WHITELIST_DIR')
        self.backdir = self.get_value(sections='PATH',key='BACKUP_DIR')
        self.remotedir = self.get_value(sections='FTP',key='REMOTE_DIR')
        if not self.localdir.endswith("/"):
            self.localpath = self.localdir + '/'
        else:
            self.localpath = self.localdir

        if not self.backdir.endswith("/"):
            self.backpath = self.backdir + '/'
        else:
            self.backpath = self.backdir
        if not self.remotedir.endswith("/"):
            self.remotepath = self.remotedir + '/'
        else:
            self.remotepath = self.remotedir

        print

    def ftpconnect(self):
        host = self.get_value(sections='FTP',key='HOST')
        user = self.get_value(sections='FTP',key='USER')
        password = self.get_value(sections='FTP',key='PASS')
        port = self.get_value(sections='FTP',key='PORT')
        timeout = float(self.get_value(sections='FTP',key='TIMEOUT'))
        try:
            self.ftp = FTP()
            self.ftp.set_debuglevel(1)
            self.ftp.connect(host,port,timeout)
            self.ftp.login(user,password)
            self.logger.debug('Server: %s User: %s Login successful' % (host, user))
        except Exception as e:
            self.logger.error(e)
            exit(1)

    def check(self):
        backfiletime = ''
        whitelistfiletime = ''
        self.qsid = ''
        for id in self.qsidlist:
            for i in self.ftp.nlst(self.remotedir):
                if re.match(id, os.path.basename(i)):
                    self.qsid = id

            for i in os.listdir(self.localpath):
                if re.match(self.qsid, i):
                    backfiletime = i.split('_')[1].split('.')[0]
                    continue
            a = {}
            for i in self.ftp.nlst(self.remotedir):
                if re.match(self.qsid, os.path.basename(i)):
                    a[time.mktime(time.strptime(os.path.basename(i).split('_')[1].split('.')[0],"%y%m%d"))] = os.path.basename(i).split('_')[1].split('.')[0]
                    continue

            for j in self.ftp.nlst(self.remotedir):
                if re.match(self.qsid, os.path.basename(j)):
                    if re.match('.*%s.*' % a[max(a)], os.path.basename(j)):
                        whitelistfiletime = os.path.basename(j).split('_')[1].split('.')[0]
                        continue
            if backfiletime == '':
                backfiletime = '010101'
            if time.mktime(time.strptime(whitelistfiletime,"%y%m%d")) <= time.mktime(time.strptime(backfiletime,"%y%m%d")):
                self.logger.info('File do not need to be replaced')
                #
                # exit(1)

    def download(self):
        self.check()
        try:
            for i in os.listdir(self.localpath):
                if re.match(self.qsid, i):
                    self.backfile = i
                    if not os.path.isfile(os.path.join(self.backpath, self.backfile)):
                        shutil.move(os.path.join(self.localpath, self.backfile), self.backpath)
                        self.logger.debug('%s File backup success' % self.backfile)
                    else:
                        os.remove(os.path.join(self.backpath, self.backfile))
                        shutil.move(os.path.join(self.localpath, self.backfile), self.backpath)
                        self.logger.debug('%s File backup success' % self.backfile)
                    continue
            a = {}
            for i in self.ftp.nlst(self.remotedir):
                if re.match(self.qsid,os.path.basename(i)):
                    a[time.mktime(time.strptime(os.path.basename(i).split('_')[1].split('.')[0], "%y%m%d"))] = \
                    os.path.basename(i).split('_')[1].split('.')[0]
                    continue
            for j in self.ftp.nlst(self.remotedir):
                if re.match(self.qsid,os.path.basename(j)):
                    if re.match('.*%s.*'%a[max(a)],os.path.basename(j)):
                        whitelistfile = os.path.basename(j)
                        continue
            whitelistpath = self.localpath + whitelistfile
            remotefile = self.remotepath + whitelistfile
            fp = open(whitelistpath,'wb')
            self.ftp.retrbinary('RETR ' + remotefile, fp.write)
            self.logger.debug('%s File send OK'% whitelistfile)
            self.logger.info('%s File update success' % whitelistfile)
        except Exception as e:
            self.logger.error('%s%s'%(remotefile,e))
            os.remove(whitelistpath)
            shutil.move(os.path.join(self.backpath, self.backfile), os.path.join(self.localpath, self.backfile))
            exit(1)

    def quit(self):
        self.ftp.quit()

    def play(self):
        self.ftpconnect()
        self.download()
        try:
            if not os.path.isfile('/mds/aac/aac_V1.0.2/bin/restart_auth.sh'):
                self.quit()
                self.logger.error('/mds/aac/aac_V1.0.2/bin/restart_auth.sh No such file or directory')
                exit(1)
            else:
                os.popen("sh /mds/aac/aac_V1.0.2/bin/restart_auth.sh")
                self.logger.info('authentication Service restart success')
                self.quit()
                exit(0)
        except Exception as e:
            self.logger.error(e)
            exit(1)


if __name__ == "__main__":
    ftp = Get_whitelist()
    ftp.play()



