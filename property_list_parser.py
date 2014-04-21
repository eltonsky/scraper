#!/usr/bin/python

from bs4 import BeautifulSoup

class PropertyListParser:

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
		for prop in self.soup.find_all("div",class_="resultBody"):
			# listing name
			name = self.get_name(prop)

			# price
			price = self.get_price(prop)

			# type
			type_ = self.get_type(prop)

			# features
			features = self.get_features(prop)
			
			# agent
			agent = self.get_agent(prop)

			print(name)
			# print(price)
			# print(type_)
			# print(features)
			print(agent)



	def get_name(self,prop):
		return prop.find("a",rel="listingName").get_text()

	def get_price(self,prop):
		price_tag = prop.find("p", class_="price")

		price = price_tag.find("span").get_text()

		return price
		
	def get_features(self,prop):
		_dict = {}

		prop_features = prop.find("ul",class_="propertyFeatures")

		if prop_features != None:
			for f in prop.find("ul",class_="propertyFeatures").select("li"):
				key = f.find("img")["alt"]
				val = f.find("span").get_text()
				_dict[key] = val

		return _dict

	def get_type(self,prop):
		return prop.find("span",class_="propertyType").get_text()

	def get_agent(self,prop):
		listerName = prop.find("p",class_="listerName")
		agent=""

		if listerName != None:
			agent=listerName.find("span").get_text()

		return agent


# test
pl_parser = PropertyListParser("./list0")
pl_parser.process()