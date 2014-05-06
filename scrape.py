#!/usr/bin/python

from time import sleep
from subprocess import call
from bs4 import BeautifulSoup
import util
import sys
import time

# tmp="http://www.realestate.com.au/buy/in-templestowe%2c+vic+3106/list-1?activeSort=list-date&includeSurrounding=true"

user_agent="'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20070802 SeaMonkey/1.1.4'"
url_base="http://www.realestate.com.au/"
page="list-"
url_sort_date="activeSort=list-date"
includeSurrounding="includeSurrounding=false" # not include surrounding area for now, keep it simple.
cmd="wget -U {0} '{1}' -O {2}"
pl_output_dir_base="./listing/"
p_output_dir_base="./property/"

suburb_list = [ "warrandyte+south", "3134"]

# suburb_list = [ "donvale", "3111", "templestowe","3106", "warrandyte","3113","warrandyte south", "3114"]

suburb_format = "in-{0}%2c+vic+{1}"

suburb_iter = iter(suburb_list)

def get_property_list_url(cmd,user_agent,url_base,suburb_format,suburb,postcode,page,index,url_sort_date,output):
	return cmd.format(user_agent, url_base+"buy/"+suburb_format.format(suburb,postcode)+"/"+page+str(index)+"?"+url_sort_date+"&"+includeSurrounding, output)

def get_property_url(cmd, user_agent, url_base, href, output):
	return cmd.format(user_agent,url_base+href,output)

datetime = time.strftime("%Y%m%d_%H")

with open('Victoria-Postcodes.csv') as fp:
	for line in fp:
		suburbs = line.split('\r')
		
		for s in suburbs:
			s_ary = s.split(',')
			postcode=s_ary[0]
			suburb = "_".join(s_ary[1].split(" "))

			list_index=1

			# create listing_dir
			pl_output_dir = pl_output_dir_base + suburb+"/"+ datetime+"/"
			util.mkdir_p(pl_output_dir)	

			# create properties dir
			p_output_dir = p_output_dir_base + suburb+"/"+ datetime+"/"
			util.mkdir_p(p_output_dir)

			# to keep the order of properties in a suburb
			p_order = 0

			while (True):

				output = pl_output_dir+str(list_index)

				curr_cmd= get_property_list_url(cmd,user_agent,url_base,suburb_format,suburb,postcode,page,list_index,url_sort_date,output)

				print ("Run: " + curr_cmd)

				call(curr_cmd, shell=True)

				file_soup= BeautifulSoup(open(output))

				# check if run out of page
				if util.is_page_not_found(file_soup):
					print ("PAGE NOT FOUND :" + output)
					break

				list_index=list_index+1

				print ("downloaded "+ output)

				# download each property
				for vcard in file_soup.find_all("div",class_="vcard"):
					a = vcard.find("a")
					href = a["href"].encode('ascii', 'ignore')
					addr = util.normalize_addr(a.get_text())
					p_output = p_output_dir+"{0:0=3d}".format(p_order)+"_"+addr
					p_order = p_order + 1
					p_cmd = get_property_url(cmd,user_agent,url_base,href,p_output)
					p_cmd = get_property_url(cmd,user_agent,url_base,href,p_output.encode('ascii', 'ignore'))
					
					print ("	Run property qry : " + p_cmd)
					call(p_cmd, shell=True)
					

				sleep(util.delay()) 




