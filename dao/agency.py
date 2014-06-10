#!/usr/bin/python

import db_util

class Agency:
	"""Agency"""

	_name=""
	_cr_date=""
	_db_util=None

	def __init__(self,name="",cr_date=""):
		self._name=name
		self._cr_date = cr_date

	def upd_proc(self):
		if self._db_util == None:
			self._db_util = db_util.DB_Util()

		if self._db_util.connect() < 0:
			return -1

		args=[self._name]

		result = self._db_util.callproc("pUpdAgency", args)

		self._db_util.close()

		status = result[0]
		agency_id = result[1]

		print ("Updated/Inserted agency : " +str(agency_id))

		return [status, agency_id]


	def select(self,addr_id):
		if self._db_util == None:
			self._db_util = db_util.DB_Util()

		if self._db_util.connect() < 0:
			return -1

		args=(addr_id)

		cursor = self._db_util.qry(self._select_qry, args)

		for (street_no,street_name,locality,region,postcode,cr_date) in cursor:
		  print("{} , {} , {}, {}, {}, {}".format(
		    street_no,street_name,locality,region,postcode,cr_date))

		cursor.close()

		self._db_util.close()


	def __str__(self):
		return (self._name)

