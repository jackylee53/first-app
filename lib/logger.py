import logging,logging.handlers
class Log_marker(object):
    def __init__(self):
        pass

    def log_marker(self,log_path,log_level,log_name=''):
        #local_path = self.get_value(sections='LOGGER' ,key='LOG_PATH')
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_level)
        st_handler = logging.StreamHandler()
        st_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'))
        rf_handler = logging.handlers.TimedRotatingFileHandler(log_path, when='midnight', interval=1 ,backupCount=7, )
        rf_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'))
        self.logger.addHandler(rf_handler)
        self.logger.addHandler(st_handler)
        return self.logger

if __name__ == '__main__':
    from lib.configuration import Config_read
    test = Log_marker()
    configure = Config_read()
    logger = test.log_marker(log_path=configure.get_value(sections='LOGGER',key='LOG_PATH'),log_level=configure.get_value(sections='LOGGER',key='LOG_LEVEL'))

