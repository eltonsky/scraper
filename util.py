#!/usr/bin/python

from bs4 import BeautifulSoup
from random import randint

def is_page_not_found(file):
	if file.find("p",class_="noMatch") != None:
		return True
	
	return False

def normalize_addr(addr):
	addr_ = addr.strip()
	# if addr is too long and end wtih ..., truncate it at the last ","
	if addr_.endswith("..."):
		last_comma = addr_.rfind(",")
		addr_ = addr_[0:last_comma]

	addr_ = addr_.replace("/","_").replace(",","_").replace(" ","_")

	i=0
	prev_is_us=False
	curr_is_us=False

	new_addr=""

	while i <len(addr_):
		if addr_[i] == '_' and prev_is_us:
			i+=1
			continue
		elif addr_[i] == '_':
			prev_is_us = True
		else:
			prev_is_us = False

		new_addr+=addr_[i]
		i+=1

	print new_addr.lower()		
	return new_addr.lower()

def delay():
	return randint(1,3)*0.86