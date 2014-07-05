#!/usr/bin/python

import db_util

class Address:
	"""property address"""

	_street_no=""
	_street_name=""
	_locality=""
	_region=""
	_postcode=""
	_capture_date_time=""
	_cr_date=""
	_db_util=None

	_insert_qry = (
	  "INSERT INTO taddr(street_no,street_name,locality,region,postcode) "
	  "VALUES (%s, %s, %s, %s, %s)"
	  )


	_upd_proc = (
		"Call pUpdAddress('{0}', '{1}', '{2}' ,'{3}' ,'{4}');"
	  )	

	_update_qry = (
	  "Update taddr set street_no = %s, street_name= %s, locality=%s, region = %s, postcode = %s)"
	  )

	_select_qry = ("SELECT street_no,street_name,locality,region,postcode,cr_date FROM taddr"
         "WHERE addr_id = %s")
	
	def __init__(self,street_no="",street_name="",locality="",region="",postcode="",capture_date_time="",cr_date=""):
		self._street_no = street_no
		self._street_name = street_name
		self._locality = locality
		self._region = region
		self._postcode = postcode
		self._capture_date_time = capture_date_time
		self._cr_date = cr_date

	def insert(self):
		if self._db_util == None:
			self._db_util = db_util.DB_Util()

		if self._db_util.connect() < 0:
			return -1

		args=(self._street_no,self._street_name,self._locality,self._region,self._postcode,self._capture_date_time)

		row_id = self._db_util.execute(self._insert_qry, args)

		self._db_util.close()

		return row_id


	def upd_proc(self):
		if self._db_util == None:
			self._db_util = db_util.DB_Util()

		if self._db_util.connect() < 0:
			return -1

		args=(self._street_no,self._street_name,self._locality,self._region,self._postcode,self._capture_date_time)

		result = self._db_util.callproc("pUpdAddress", args)

		self._db_util.close()

		status = result[0]
		row_id = result[1]

		print ("Inserted/Updated addr_id is " + str(row_id))

		return [status,row_id]


	def update(self):
		if self._db_util == None:
			self._db_util = db_util.DB_Util()

		if self._db_util.connect() < 0:
			return -1

		args=(self._street_no,self._street_name,self._locality,self._region,self._postcode,self._capture_date_time)

		row_id = self._db_util.execute(self._update_qry, args)

		self._db_util.close()

		return row_id

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
		return (self._street_no + "," + self._street_name+","+self._locality+
			","+self._region+","+self._postcode+","+self._cr_date)

