#!/usr/bin/python

import db_util, agent, features

class Sale:
	"""Sale"""

	_sale_id=""
	_prop_id=""
	_agency_id=""
	_price=""
	_price_type=""
	_sale_status=""
	_cr_date=""
	_capture_date_time=""
	_features=None
	_db_util=None

	def __init__(self,sale_id="",prop_id="",agency_id="",price="",price_type="",sale_status="", features=None, capture_date_time="", cr_date=""):
		self._sale_id = sale_id
		self._prop_id = prop_id
		self._agency_id = agency_id
		self._price=price
		self._price_type=price_type
		self._sale_status=sale_status
		self._features = features
		self._capture_date_time = capture_date_time
		self._cr_date = cr_date

	def upd_proc(self):
		if self._db_util == None:
			self._db_util = db_util.DB_Util()

		if self._db_util.connect() < 0:
			return -1

		args=(self._prop_id,self._agency_id,self._sale_status,self._price,self._price_type,
			self._features._bedrooms, self._features._bathrooms, self._features._car_spaces,
			self._features._land_size,self._capture_date_time)

		result = self._db_util.callproc("pUpdSale", args)

		self._db_util.close()

		status = result[0]
		sale_id = result[1]
		price_id = result[2]

		print ("Updated/Inserted sale : " +str(sale_id)+ " & price :" + str(price_id) + " status :" + str(status))

		return [status, sale_id, price_id]


	def upd_sale_agent(self,agent_ids):
		if self._db_util == None:
			self._db_util = db_util.DB_Util()

		if self._db_util.connect() < 0:
			return -1

		for agent_id in agent_ids:

			args=(self._sale_id,agent_id,self._capture_date_time)

			result = self._db_util.callproc("pUpdSaleAgent", args)

			sale_agent_id = result[1]

			print ("Updated/Inserted sale agent id: " +str(sale_agent_id))

		self._db_util.close()


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

