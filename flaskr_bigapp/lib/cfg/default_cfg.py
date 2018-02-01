from flaskr_bigapp.lib.sys.make import GET
class Default(object):
    def __init__(self):
        self.dir = GET()

    def default_config(self):
        self.dicts = {
            'LOGGER': {
                'GLOBAL_LOG_LEVEL': 'DEBUG',
                'FILE_LOG_LEVEL': 'DEBUG',
                'STREAM_LOG_LEVEL': 'DEBUG',
            },
            'LOGGER_DIR': {
                'GLOBAL_LOG_FILE': '%s/messages.log'%self.dir.get_log_dir(),
                'ANSIBLE_LOG_FILE': '%s/ansibles.log'%self.dir.get_log_dir(),
            },
            'ANSIBLE': {
                'INVENTORY_CONFIG': '/etc/ansible/hosts',
                'FORKS': 5,
            },
            'DATABASE': {
                'TYPE': 'sqlite3',
                'DATABASE_NAME': 'devops.db',
            }
        }
        return self.dicts
if __name__ == '__main__':
    test = Default()
    print test.default_config()
