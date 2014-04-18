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
		for prop in self.soup.find_all("div",class_="resultBody"):
			#print(prop)

			# listing name
			name = self.get_name(prop)

			print(name)

			# price
			price = self.get_price(prop)

			print(price)
		

	def get_name(self,prop):
		return prop.find("a",rel="listingName").get_text()

	def get_price(self,prop):
		price_tag = prop.find("p", class_="price")

		price = price_tag.find("span").get_text()

		return price
		


parser = PropertyParser("./list0")
parser.process()