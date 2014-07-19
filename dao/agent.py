#!/usr/bin/python

import db_util

class Agent:
	"""Agent"""

	_name=""
	_phone=""
	_agency_id=""
	_capture_date_time=""
	_cr_date=""
	_db_util=None

	def __init__(self,name="",phone="",agency_id="",capture_date_time="",cr_date=""):
		self._name=name
		self._phone=phone
		self._agency_id=agency_id
		self._capture_date_time = capture_date_time
		self._cr_date = cr_date

	def upd_proc(self):
		if self._db_util == None:
			self._db_util = db_util.DB_Util()

		if self._db_util.connect() < 0:
			return -1

		args=(self._agency_id, self._name, self._phone,self._capture_date_time)

		result = self._db_util.callproc("pUpdAgent", args)

		self._db_util.close()

		status = result[0]
		agent_id = result[1]

		print ("Updated/Inserted agent : " +str(agent_id))

		return [status, agent_id]


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
		return (self._agency_id+","+self._name+","+self._phone)

