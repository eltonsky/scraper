#!/usr/bin/python

import db_util

class Features:
	"""Features"""

	_sale_id=""
	_bedrooms=""
	_bathrooms=""
	_car_sapces=""
	_land_size=""
	_cr_date=""
	_db_util=None

	def __init__(self,sale_id="",bed="",bath="",car_sapces="",land_size="",cr_date=""):
		self._sale_id = sale_id
		self._bedrooms = bed
		self._bathrooms = bath
		self._car_sapces= car_sapces
		self._land_size= land_size
		self._cr_date = cr_date

	def upd_proc(self):
		if self._db_util == None:
			self._db_util = db_util.DB_Util()

		if self._db_util.connect() < 0:
			return -1

		args=(self._prop_id,self._agency_id,self._sale_status,self._price,self._price_type)

		result = self._db_util.callproc("pUpdSale", args)

		self._db_util.close()

		status = result[0]
		sale_id = result[1]
		price_id = result[2]

		print ("Updated/Inserted sale : " +str(sale_id)+ " & price :" + str(price_id))

		return [status,sale_id,price_id]


	def upd_sale_agent(self,agent_ids):
		if self._db_util == None:
			self._db_util = db_util.DB_Util()

		if self._db_util.connect() < 0:
			return -1

		for agent_id in agent_ids:

			args=(self._sale_id,agent_id)

			result = self._db_util.callproc("pUpdSaleAgent", args)

			self._db_util.close()

			sale_agent_id = result[0]

		print ("Updated/Inserted sale agent id: " +str(sale_agent_id))


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
		return (self._prop_id + "," + self._agency_id+","+self._sale_status+","+self._price+","+self._price_type)

