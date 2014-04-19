#!/usr/bin/python

from time import sleep
from subprocess import call
from bs4 import BeautifulSoup
import util

tmp="http://www.realestate.com.au/buy/in-templestowe%2c+vic+3106/list-1?activeSort=list-date&includeSurrounding=true"

user_agent="'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20070802 SeaMonkey/1.1.4'"
url_base="http://www.realestate.com.au/"
page="list-"
url_sort_date="activeSort=list-date"
includeSurrounding="includeSurrounding=true"
cmd="wget -U {0} {1} -O {2}"
pl_output_dir="./listing/"
p_output_dir="./property/"

suburb_list = [ "donvale", "3111", "templestowe","3106"]
suburb_format = "in-{0}%2c+vic+{1}"

suburb_iter = iter(suburb_list)

def get_property_list_url(cmd,user_agent,url_base,suburb_format,suburb,postcode,page,index,url_sort_date,output):
	return cmd.format(user_agent, url_base+"buy/"+suburb_format.format(suburb,postcode)+"/"+page+str(index)+"?"+url_sort_date, output)

def get_property_url(cmd, user_agent, url_base, href, output):
	return cmd.format(user_agent,url_base+href,output)

for suburb in suburb_iter:

	postcode = next(suburb_iter)

	index=1

	while (True):
		output = pl_output_dir+suburb+"_"+str(postcode)+"_"+str(index)

		curr_cmd= get_property_list_url(cmd,user_agent,url_base,suburb_format,suburb,postcode,page,index,url_sort_date,output)

		print ("Run: " + curr_cmd)

		call(curr_cmd, shell=True)

		file_soup= BeautifulSoup(open(output))

		# check if run out of page
		if util.is_page_not_found(file_soup):
			print ("PAGE NOT FOUND :" + output)
			break

		index=index+1

		print ("downloaded "+ output)
		
		# download each property
		for vcard in file_soup.find_all("div",class_="vcard"):
			a = vcard.find("a")
			href = a["href"]
			addr = util.normalize_addr(a.get_text())
			p_output = p_output_dir+addr
			p_cmd = get_property_url(cmd,user_agent,url_base,href,p_output)
			
			print ("	Run property qry : " + p_cmd)
			call(p_cmd, shell=True)
			

		sleep(util.delay()) 




