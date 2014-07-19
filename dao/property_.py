#!/usr/bin/python

import db_util

class Property:
	"""property"""

	_land_size=""
	_ext_id=""
	_type=""
	_addr_id=""
	_cr_date=""
	_capture_date_time = ""
	_db_util=None

	_upd_proc = (
		"Call pUpdAddress('{0}', '{1}', '{2}' ,'{3}' ,'{4}');"
	  )	

	def __init__(self,ext_id="",addr_id="",land_size="",type_="",capture_date_time="",cr_date=""):
		self._ext_id = ext_id
		self._land_size = land_size
		self._type=type_
		self._cr_date = cr_date
		self._addr_id = addr_id
		self._capture_date_time=capture_date_time 

	def upd_proc(self):
		if self._db_util == None:
			self._db_util = db_util.DB_Util()

		if self._db_util.connect() < 0:
			return -1

		args=(self._ext_id,self._addr_id,self._land_size,self._type,self._capture_date_time)

		result = self._db_util.callproc("pUpdProperty", args)

		self._db_util.close()

		status = result[0]
		row_id = result[1]

		print ("Updated/Inserted property_id is " + str(row_id))

		return [status,row_id]


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
		return (self._ext_id + "," + self._land_size+","+self._type+","+self._cr_date)

