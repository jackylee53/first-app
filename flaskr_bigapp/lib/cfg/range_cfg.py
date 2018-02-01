#from flaskr_bigapp.lib.sys.make import GET
class Range(object):
    def __init__(self):
        pass;
        #self.dir = GET().GETDIR()

    def range_config(self):
        self.range_dicts = {
            'LOGGER': {
                'GLOBAL_LOG_LEVEL': ['DEBUG','INFO','WARNING','ERROR','CRITICAL'],
                'FILE_LOG_LEVEL': ['DEBUG','INFO','WARNING','ERROR','CRITICAL'],
                'STREAM_LOG_LEVEL': ['DEBUG','INFO','WARNING','ERROR','CRITICAL'],
            },
            'LOGGER_DIR': {
            },
            'ANSIBLE': {
            },
        }
        return self.range_dicts
