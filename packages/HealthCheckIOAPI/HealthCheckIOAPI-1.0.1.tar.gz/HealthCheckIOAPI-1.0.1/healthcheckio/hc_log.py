import logging
import os
import sys

class log():
    def __init__(self, module, debug=False):
        self.module = module
        self.toDEBUG = debug
        self.logger = logging.getLogger(self.module)
        self.log = logging.StreamHandler()
        self.logformatter = logging.Formatter(fmt='[%(asctime)s][%(name)s][%(levelname)s]: %(message)s', datefmt='%m-%d-%Y %H:%M:%S')

        if debug is True:
            logging.getLogger(self.module).setLevel(logging.DEBUG)
        else:
            logging.getLogger(self.module).setLevel(logging.INFO)
        
        self.logger.handlers.clear()
        if not self.logger.hasHandlers():
            self.log.setFormatter(self.logformatter)
            self.logger.addHandler(self.log)

    def setLevel(self, level='DEBUG'):
        try:
            if level == 'DEBUG':
                logging.getLogger(self.module).setLevel(logging.DEBUG)
            elif level == 'INFO':
                logging.getLogger(self.module).setLevel(logging.INFO)
            elif level == 'WARNING':
                logging.getLogger(self.module).setLevel(logging.WARNING)
            elif level == 'ERROR':
                logging.getLogger(self.module).setLevel(logging.ERROR)
            elif level == 'CRITICAL':
                logging.getLogger(self.module).setLevel(logging.CRITICAL) 
            else:
                return False
            return True
        except:
            return False

    def setDebug(self, setdebug=False):
        try:
            if not setdebug is False:
                self.toDEBUG = True
                self.setLevel('DEBUG')
            else:
                self.toDEBUG = False
                self.setLevel('INFO')
        except:
            return False

    def debug(self, msg):
        try:
            return self.logger.debug(msg)
        except:
            return False

    def info(self, msg):
        try:
            return self.logger.info(msg)
        except:
            return False

    def warning(self, msg):
        try:
            return self.logger.warning(msg)
        except:
            return False

    def error(self, msg):
        try:
            return self.logger.error(msg)
        except:
            return False

    def critical(self, msg):
        try:
            return self.logger.critical(msg)
        except:
            return False