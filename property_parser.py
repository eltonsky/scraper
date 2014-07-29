#!/usr/bin/python

from bs4 import BeautifulSoup
import util, string
import sys
sys.path.append('dao')
import address, property_, sale, agency, agent, features, inspection


class PropertyParser:

	_html = None
	soup = None
	_date_time = None

	def __init__(self):
		pass

	# def __init__(self, doc):
	# 	self.html_doc = doc
	# 	self.html = util.gunzip_file(doc)
	# 	self.soup = BeautifulSoup(self.html)

	# def __del__(self):
	# 	if self.html is not None:
	# 		self.html.close()

	def process(self, doc, date_time):

		try:
			# generate html obj
			self._html = util.gunzip_file(doc)
			self.soup = BeautifulSoup(self._html)
			self._date_time = date_time

			# addr
			addr = self.get_address()
			if addr is None:
				return -1

			res = addr.upd_proc()
			addr_status = res[0]
			addr_id = res[1]

			# features
			features = self.get_features()

			# property
			prop = self.get_property(addr_id,features._land_size) 
			res = prop.upd_proc()
			prop_status = res[0]
			prop_id = res[1]

			# agency
			agency  = self.get_agency()
			res = agency.upd_proc()
			agency_id = res[1]

			# sale/price
			sale = self.get_sale(prop_id, agency_id, features)
			res = sale.upd_proc()
			sale_status = res[0]
			sale_id = res[1]
			price_id = res[2]

			setattr(sale,"_sale_id",sale_id)
			
			# agent
			agents = self.get_agents(agency_id)
			agent_ids=[]
			for agent in agents:
				res = agent.upd_proc()
				if res[1] > 0:
					agent_ids.append(res[1])

			# sale agent
			sale.upd_sale_agent(agent_ids)

			# inspection
			inspections = self.get_inspection(sale_id)
			for insp in inspections:	
				res = insp.upd_proc()

			return 1

		except Exception, e:
			print("Failed to process doc : " + doc + " due to : " + str(e))
			return -1


		# print(addr)
		# print(addr_id)
		# print(price)
		# print(type_)
		# print(features)
		# print(agents)
		# print(agency)
		# print(inspections)

	def get_property(self,addr_id, land_size):
		# property id
		prop_ext_id = self.get_property_id()

		# type
		type_ = self.get_type()

		prpt_obj = property_.Property(prop_ext_id, addr_id, land_size, type_, self._date_time)

		return prpt_obj


	def get_property_id(self):
		id_text = self.soup.find("span",class_="property_id").get_text()
		id_list = id_text.split()
		return id_list[len(id_list) - 1]

	def get_address(self):
		addr = self.soup.find("h1",itemprop="address")

		if addr is None:
			print ("Failed to find addr !! Check it!")
			return None

		addr_obj = address.Address()

		for span in addr.find_all("span"):
			key = span["itemprop"]
			val = span.get_text()

			if key == "streetAddress":
				street = util.split_street_addr(val)

				setattr(addr_obj,"_street_no",street[0].strip())
				setattr(addr_obj,"_street_name",street[1].strip())
			elif key == "addressLocality":
				setattr(addr_obj,"_locality",val)
			elif key == "addressRegion":
				setattr(addr_obj,"_region",val)
			elif key == "postalCode":
				setattr(addr_obj,"_postcode",val)

		setattr(addr_obj,"_capture_date_time",self._date_time)

		return addr_obj


	def get_sale(self,prop_id,agency_id, features):
		price_tag = self.soup.find("div", id="listing_info").find("p", class_="price")

		price_text = price_tag.find("span").get_text()

		# if it's in auction
		auction_tag = self.soup.find("p", class_="auctionDetails")
		if auction_tag is not None:
			# call it price type rather than sale_type, cause one sale may change
			# from normal sale to auction or vice versa. It's flexible to track 
			# it in price.

			# auction
			price_type = 'A'
		else :
			# normal sale
			price_type = 'N'		

		# TODO: track auction details

		# "Under Contract"/Under Offer etc.
		sale_status = self.soup.find("div", class_="auction_details").find("strong").get_text()

		sale_ = sale.Sale(0,prop_id, agency_id, price_text, price_type, sale_status, features, self._date_time)

		return sale_
		
	def get_features(self):
		features_ = features.Features()

		prop_features = self.soup.find("div", id="listing_info").find("ul",class_="propertyFeatures")

		if prop_features is not None:
		# Bedrooms
		# Bathrooms
		# Car Spaces
			for f in prop_features.select("li"):
				key = f.find("img")["alt"]
				val = f.find("span").get_text()
				setattr(features_,"_"+string.replace(key.lower()," ","_"),val)

		# land size
		setattr(features_,"_land_size",self.get_land_size())
		
		return features_

	def get_land_size(self):
		land_size=""

		for li in self.soup.find("div",class_="featureList").find_all("li"):
			if "Land Size:" in li.get_text():
				land_size = li.find("span").get_text()
				return land_size

		return land_size


	def get_type(self):
		return self.soup.find("div", id="listing_info").find("span",class_="propertyType").get_text()


	def get_agents(self,agency_id):
		agents = []
		# to avoid duplicate agent info make the seletor compilicated a bit
		for agent_tag in self.soup.find("div",id="agentInfoExpanded").find_all("div",class_="agent"):
			name = agent_tag.find("p",class_="agentName")
			if name is not None:
				name = name.find("strong").get_text()

			phone = agent_tag.find("li",class_="phone").get_text()

			agents.append(agent.Agent(name,phone,agency_id,self._date_time))
		return agents


	def get_agency(self):
		name = self.soup.find("p",class_="agencyName").get_text()
		agency_ = agency.Agency(name,self._date_time)
		return agency_

	def get_inspection(self,sale_id):
		inspection_tag = self.soup.find("div",id="inspectionTimes")

		if inspection_tag is None:
			return []

		inspects = []

		for event in inspection_tag.find_all("a",itemprop="events"):
			start = event.find("meta",itemprop="startDate")["content"]
			end = event.find("meta",itemprop="endDate")["content"]
			inspects.append(inspection.Inspection(sale_id,start,end,self._date_time))

		return inspects


# # test
# p_parser = PropertyParser()
# p_parser.process("./property/PARK_ORCHARDS/20140506_08/000_21-23_gosford_crescent_park_orchards_vic_3114")


class BuyPropertyParser(PropertyParser):

	def __init__(self):
		PropertyParser.__init__(self)



class SoldPropertyParser(PropertyParser):

	def __init__(self):
		PropertyParser.__init__(self)


	def get_sale(self,prop_id,agency_id, features):
		price_tag = self.soup.find("div", id="listing_info").find("p", class_="price")

		price_text = price_tag.find("span", class_="priceText").get_text()

		sale_status = util.SaleStatus.SOLD

		sale_ = sale.Sale(0,prop_id, agency_id, price_text, util.PriceType.SOLD, sale_status, features, self._date_time)

		return sale_


# # test
# p_parser = SoldPropertyParser()
# p_parser.process("property/WANTIRNA_SOUTH/20140506_08/sold/inbox/test1.gz","2014-07-29")


