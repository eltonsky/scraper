#!/usr/bin/python

import db_util, agent, features

class Inspection:
	"""Inspection"""

	_sale_id=""
	_start=""
	_end=""
	_cr_date=""
	_db_util=None

	def __init__(self,sale_id="",start="",end="",cr_date=""):
		self._sale_id = sale_id
		self._start = start
		self._end = end
		self._cr_date = cr_date

	def upd_proc(self):
		if self._db_util == None:
			self._db_util = db_util.DB_Util()

		if self._db_util.connect() < 0:
			return -1

		args=(self._sale_id,self._start,self._end)

		result = self._db_util.callproc("pUpdInspection", args)

		self._db_util.close()

		status = result[0]
		inspection_id = result[1]

		print ("Updated/Inserted inspection : " +str(inspection_id))

		return [status, inspection_id]


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
		return (self._sale_id + "," + self._start+","+self._end)

