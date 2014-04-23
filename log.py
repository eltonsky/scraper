#!/usr/bin/python

import logging
import logging.config

	
class LOG:
	_logger = None

	def __init__(self,log_conf,logger):
		logging.config.fileConfig(log_conf)
		self._logger = logging.getLogger(logger)

	def getLogger(self):
		return self._logger	


# logger = LOG("log.conf","rea").getLogger()

# # 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warn('warn message')
# logger.error('error message')
# logger.critical('critical message')
