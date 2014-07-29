#!/usr/bin/python

from bs4 import BeautifulSoup
from random import randint
import os, errno, gzip, string, shutil

valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)

def gzip_file(src):
	f_in = open(src, 'rb')
	f_out = gzip.open(src+".gz", 'wb')
	f_out.writelines(f_in)
	f_out.close()
	f_in.close()
	os.remove(src)

def gunzip_file(src):
	f = gzip.open(src, 'rb')
	file_content = f.read()
	f.close()
	return file_content


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def is_page_not_found(file):
	if file.find("p",class_="noMatch") is not None:
		return True
	
	return False

def normalize_addr(addr):
	"""
		Used for get an file name for each property.
		Not necessarily needed, as addr is retrieved from the file.
	"""
	mark="-"

	addr_ = addr.strip()
	# if addr is too long and end wtih ..., truncate it at the last ","
	if addr_.endswith("..."):
		last_comma = addr_.rfind(",")
		addr_ = addr_[0:last_comma]

	addr_ = addr_.replace("/",mark).replace(",",mark).replace(" ",mark)

	i=0
	prev_is_us=False
	curr_is_us=False

	new_addr=""

	while i <len(addr_):
		if addr_[i] == mark and prev_is_us:
			i+=1
			continue
		elif addr_[i] == mark:
			prev_is_us = True
		else:
			prev_is_us = False

		new_addr+=addr_[i]
		i+=1

	return ''.join(c for c in new_addr.lower() if c in valid_chars)


def split_street_addr(str_addr):
	ary = str_addr.split()
	street_no = ""
	for i in range(0,len(ary)):
		if ary[i].isalpha():
			break
		street_no += ary[i]

	street_name = str_addr[len(street_no):]

	return (street_no,street_name)


def delay():
	return randint(1,3)*0.86


def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc: # Python >2.5
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else: raise


def move(src,dest,gzip=0):
	try:
		if gzip:
			gzip_file(src)
			src = src + ".gz"

		shutil.move(src,dest)
	except:
		print("failed to compreass or mv "+src+" to " + dest+ "(gzip"+gzip+")")
		return -1

	return 1



class PriceType:
	SOLD = "S"
	NORMAL="N"
	AUCTION="A"


class SaleStatus:
	SOLD = "SOLD"
	LISTED = "LISTED"