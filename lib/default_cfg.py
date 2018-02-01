from lib.path import GET
class Default(object):
    def __init__(self):
        self.logpath = GET().get_log_path()

    def default_config(self):
        self.dicts = {
            'LOGGER': {
                'LOG_LEVEL': 'INFO',
                'LOG_PATH': '%s/whitelist.log'%self.logpath,
                'LOG_NAME': 'whitelist'
            },
            'FTP': {
                'HOST': '114.80.155.43',
                'USER': 'sysop',
                'PASS': 'SsePwd&123',
                'PORT': 7710,
                'TIMEOUT': 10,
                'REMOTE_DIR' : '/sysop/otrsarticle/csv/',
                'QSID': '00640',
            },
            'SYSTEM': {
                'WHITELIST_DIR': '/mds/aac/aac_V1.0.2/whitelist/',
                'BACKUP_DIR': '/home/mds/old_whitelist/',
            },
            'SCHEDULER': {
                'WEEK': 'mon-fri',
                'HOUR': '16-20',
                'MINUTE': '*/30',
                'SECOND': '*',
            }
        }
        return self.dicts

if __name__ == '__main__':
    test = Default()
    print test.default_config()
