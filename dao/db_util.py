#!/usr/bin/python

import mysql.connector
from mysql.connector import errorcode

class DB_Util:
	_cnx = None
	_conf = None
	config = {
	  'user': 'root',
	  'host': '127.0.0.1',
	  'database': 'rea_test1',
	  'password' : 'et19br24',
	  'raise_on_warnings': True
	}

	def __init__(self, conf):
		self._conf = conf

	def __init__(self):
		self._conf = self.config
		
	def connect(self):
		try:
		  self._cnx = mysql.connector.connect(**self._conf)
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your conf")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exists")
			else:
				print(err)

			return -1
		else:
			print("connect sucessfully")
			return 0


	def close(self):
		self._cnx.close()

	def execute(self,qry,args):
		cursor = self._cnx.cursor(buffered=True)

		cursor.execute(qry,(args))

		rowid = cursor.lastrowid

		cursor.close()

		self._cnx.commit()

		return rowid

	def qry(self,qry,args):
		cursor = self._cnx.cursor(buffered=True)

		cursor.execute(qry,(args))

		return cursor


	def execproc(self,qry):
		cursor = self._cnx.cursor(buffered=True)
		print qry
		cursor.execute(qry, multi=True)

		result = cursor.fetchone()

		cursor.close()

		self._cnx.commit()

		return result

	def callproc(self,qry,args):
		cursor = self._cnx.cursor(buffered=True)

		cursor.callproc(qry,args)

		for r in cursor.stored_results():
			result = r.fetchone()

		cursor.close()

		self._cnx.commit()

		return result

# # test code

# config = {
#   'user': 'root',
#   'host': '127.0.0.1',
#   'database': 'rea',
#   'password' : 'et19br24',
#   'raise_on_warnings': True
# }

# insert_addr = (
#   "INSERT INTO taddr(street_no,street_name,locality,region,postcode) "
#   "VALUES (%s, %s, %s, %s, %s)")

# args = ('29-31',' Granard Avenue','Park Orchards','Vic','3114')

# db_util = DB_Util(config)
# db_util.connect()

# db_util.execute(insert_addr,args)

# db_util.close()

