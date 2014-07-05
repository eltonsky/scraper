#!/usr/bin/python

import logging, logging.config
import sys
from subprocess import call	

class LOG:
	_logger = None

	def __init__(self,log_conf,logger):
		logging.config.fileConfig(log_conf)
		self._logger = logging.getLogger(logger)
		sys.stdout = self._logger
		sys.stderr = self._logger 


	def getLogger(self):
		return self._logger	


# logger = LOG("log.conf","scraper").getLogger()

# # 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warn('warn message')
# logger.error('error message')
# logger.critical('critical message')

# cmd = "wget -U 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20070802 SeaMonkey/1.1.4' 'http://www.realestate.com.au/buy/in-wheelers+hill%2c+vic+3150%3b/list-1?activeSort=list-date'"
# call(cmd, shell=True)
