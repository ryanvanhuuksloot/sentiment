import logging
import os
import datetime

class logger(logging.Logger):
    def __init__(self, name : str, log_to_console : bool = False):
        super().__init__(name)
        formatter = logging.Formatter('LOGGER:%(asctime)s [%(levelname)-5.5s]  %(message)s')
        self.LOGGER = logging.getLogger()
        self.LOGGER.setLevel(logging.DEBUG)

        if not os.path.exists('logs'):
            os.makedirs('logs')

        logPath = "logs/"
        fileName = 'log'

        now = datetime.datetime.now()
        yyyymmdd_hhmmss = str(now.year) + str(now.month) + str(now.day) + '_' + '{:02d}'.format(now.hour) + '{:02d}'.format(now.minute) + str(now.second)

        fileHandler = logging.FileHandler("{0}/{1}_{2}.log".format(logPath, yyyymmdd_hhmmss, fileName))
        fileHandler.setFormatter(formatter)
        self.LOGGER.addHandler(fileHandler)

        if log_to_console:
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(formatter)
            self.LOGGER.addHandler(consoleHandler)

    def getLogger(self):
        return self.LOGGER
