#!/usr/bin/python

from bs4 import BeautifulSoup
import util
import sys
sys.path.append('dao')
import address, property_

class PropertyParser:

	html_doc =""
	html = None
	soup = None

	def __init__(self, doc):
		self.html_doc = doc
		self.html = open(doc)
		self.soup = BeautifulSoup(self.html)

	def __del__(self):
		if self.html != None:
			self.html.close()

	def process(self):
		# addr
		addr = self.get_address()
		res = addr.upd_proc()
		addr_status = res[0]
		addr_id = res[1]

		# property
		prop = self.get_property(addr_id) 
		res = prop.upd_proc()
		prop_status = res[0]
		prop_id = res[1]

		# price
		price = self.get_price()
		
		# agent
		agents = self.get_agents()

		# agency
		agency  = self.get_agency()

		# inspection
		inspections = self.get_inspection()

		print(addr)
		print(addr_id)
		print(price)
		print(type_)
		print(features)
		print(agents)
		print(agency)
		print(inspections)

	def get_property(self,addr_id):
		# property id
		prop_ext_id = self.get_property_id()
		# features
		features = self.get_features()
		# type
		type_ = self.get_type()

		prpt_obj = property_.Property(prop_ext_id, addr_id, features["land_size"], type_)

		return prpt_obj


	def get_property_id(self):
		id_text = self.soup.find("span",class_="property_id").get_text()
		id_list = id_text.split()
		return id_list[len(id_list) - 1]

	def get_address(self):
		addr = self.soup.find("h1",itemprop="address")

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

		return addr_obj


	def get_price(self):
		price_tag = self.soup.find("p", class_="price")

		price = price_tag.find("span").get_text()

		return price
		
	def get_features(self):
		features = {}

		prop_features = self.soup.find("ul",class_="propertyFeatures")

		if prop_features != None:
			for f in prop_features.select("li"):
				key = f.find("img")["alt"]
				val = f.find("span").get_text()
				features[key] = val

		# land size
		features["land_size"] = self.get_land_size()

		return features

	def get_land_size(self):
		land_size=""

		for li in self.soup.find("div",class_="featureList").find_all("li"):
			if "Land Size:" in li.get_text():
				land_size = li.get_text()
				return land_size

		return land_size


	def get_type(self):
		return self.soup.find("span",class_="propertyType").get_text()


	def get_agents(self):
		agents = []
		# to avoid duplicate agent info make the seletor compilicated a bit
		for agent in self.soup.find("div",id="agentInfoExpanded").find_all("div",class_="agent"):
			name = agent.find("p",class_="agentName").find("strong").get_text()
			phone = agent.find("li",class_="phone").get_text()
			agents.append(name + "," + phone)

		return agents


	def get_agency(self):
		return self.soup.find("p",class_="agencyName").get_text()

	def get_inspection(self):
		inspection = self.soup.find("div",id="inspectionTimes")

		inspects = []
		for event in inspection.find_all("a",itemprop="events"):
			start = event.find("meta",itemprop="startDate")["content"]
			end = event.find("meta",itemprop="endDate")["content"]
			inspects.append(start + "," + end)

		return inspects


# test
p_parser = PropertyParser("./property/PARK_ORCHARDS/20140506_08/000_21-23_gosford_crescent_park_orchards_vic_3114")
p_parser.process()