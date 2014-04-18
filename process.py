#!/usr/bin/python

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
	def __init__(self):
		super().__init__()
		self.reset()
		self.fed = []

	def handle_starttag(self, tag, attrs):
		print("Encountered a start tag:", tag)
    
	def handle_endtag(self, tag):
		print("Encountered an end tag :", tag)
    
	def handle_data(self, data):
		print("Encountered some data  :", data)

parser = MyHTMLParser()
parser.feed('<html><head><title>Test</title></head>'
            '<body><h1>Parse me!</h1></body></html>')

parser.close()

