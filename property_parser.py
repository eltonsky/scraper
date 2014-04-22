#!/usr/bin/python

from bs4 import BeautifulSoup

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
		# property id
		prop_id = self.get_property_id()

		# addr
		addr = self.get_address()

		# price
		price = self.get_price()

		# type
		type_ = self.get_type()

		# features
		features = self.get_features()
		
		# agent
		agents = self.get_agents()

		# agency
		agency  = self.get_agency()

		# inspection
		inspections = self.get_inspection()

		print(prop_id)
		print(addr)
		print(price)
		print(type_)
		print(features)
		print(agents)
		print(agency)
		print(inspections)


	def get_property_id(self):
		id_text = self.soup.find("span",class_="property_id").get_text()
		id_list = id_text.split()
		return id_list[len(id_list) - 1]

	def get_address(self):
		addr = self.soup.find("h1",itemprop="address")

		addr_ = {}

		for span in addr.find_all("span"):
			key = span["itemprop"]
			val = span.get_text()
			addr_[key] = val

		return addr_


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
p_parser = PropertyParser("./property/29-31_Granard_Avenue_Park_Orchards_Vic_3114")
p_parser.process()