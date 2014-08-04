#!/usr/bin/python

from time import sleep
from subprocess import call
from bs4 import BeautifulSoup
import util
import sys
import time

#TODO:
# 1. use log
# 2. set a log header : ts,level,process idx
# 3. use config

# tmp="http://www.realestate.com.au/buy/in-templestowe%2c+vic+3106/list-1?activeSort=list-date&includeSurrounding=true"
log_dir="./logs/"
user_agent="'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20070802 SeaMonkey/1.1.4'"
url_base="http://www.realestate.com.au/"
page="list-"
url_sort_date="activeSort=list-date"
includeSurrounding="includeSurrounding=false" # not include surrounding area for now, keep it simple.
cmd="wget -U {0} '{1}' -O {2}"
pl_output_dir_base="./listing/"
p_output_dir_base="./property/"
p_inbox="inbox"
p_outbox="outbox"
p_progress="progress"
p_errbox="err"

# only get "sold"s for last 2 months; data prior should be in the system already
SOLD_PAGE_START_FROM = 3650
SOLD_PAGE_COUNT = 80
SOLD_DATE_NA = "N/A"

#suburb_list = [ "warrandyte+south", "3134"]
#suburb_list = [ "donvale", "3111", "templestowe","3106", "warrandyte","3113","warrandyte south", "3114"]

suburb_format = "in-{0}%2c+vic+{1}"

def get_property_list_url(cmd,user_agent,url_base,mode,suburb_format,suburb,postcode,page,index,url_sort_date,output):
	return cmd.format(user_agent, url_base+mode+"/"+suburb_format.format(suburb,postcode)+"/"+page+str(index)+"?"+url_sort_date+"&"+includeSurrounding, output)

def get_property_url(cmd, user_agent, url_base, href, output):
	return cmd.format(user_agent,url_base+href,output)

def get_sold_date(vcard):
	sold_date = vcard.findParents('div',class_="resultBody")

	# sometimes, the sold page will display a property on the right side bar
	# which has different html format. ignore that one

	if len(sold_date) == 0:
		return None

	sold_date_text = sold_date[0].find("p",class_="soldDate").get_text()

	return sold_date_text.split(" ")[2]

#
# read arguments
#
datetime = time.strftime("%Y%m%d_%H")
# to decide when to stop scraping "sold"s
sentinal_sold_date = None
sentinal_page_count = 0

# suburb list
suburb_list = sys.argv[1]
start = 0
end = 99999

mode = sys.argv[2]
file_len = int(sys.argv[3])
num_process = int(sys.argv[4])
index = int(sys.argv[5])
start= int(sys.argv[6])
end = int(sys.argv[7])

sys.stdout = open(log_dir+str(index)+"_scraper.log", 'w')

if start == -1:
	start = (file_len/num_process)*index

if end == -1:
	end = file_len*(index+1)/num_process

print ("Starting scraper... reading suburb from " + suburb_list + ", ranging from " + str(start) + " to " + str(end))

# finish reading arguments
#

fp=open(suburb_list)

for i, line in enumerate(fp):
	if i >= start and i < end:

		s_ary = line.split()
		postcode=s_ary[0]
		suburb = "_".join(s_ary[1].split(" "))

		print (str(index) + " : Processing " + postcode + " " + suburb)

		list_index=1

		# create listing_dir
		pl_output_dir = pl_output_dir_base + suburb+"/"+ datetime+"/"
		util.mkdir_p(pl_output_dir)	

		# create properties dir
		#inbox
		p_output_dir = p_output_dir_base + suburb+"/"+ datetime+"/"+mode+"/"+p_inbox+"/"
		util.mkdir_p(p_output_dir)
		#outbox
		util.mkdir_p(p_output_dir_base + suburb+"/"+ datetime+"/" + mode+"/"+ p_outbox)
		#progress
		util.mkdir_p(p_output_dir_base + suburb+"/"+ datetime+"/" + mode+"/"+p_progress)
		#errbox
		util.mkdir_p(p_output_dir_base + suburb+"/"+ datetime+"/" + mode+"/"+p_errbox)

		# to keep the order of properties in a suburb
		p_order = 0
		sentinal_sold_date = None
		sentinal_page_count = 0

		# we don't know how many pages are there..
		while (True):

			output = pl_output_dir+str(list_index)

			curr_cmd= get_property_list_url(cmd,user_agent,url_base,mode,suburb_format,suburb,postcode,page,list_index,url_sort_date,output)

			# only download SOLD_PAGE_COUNT pages for 'sold's
			sentinal_page_count = sentinal_page_count + 1

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

				try:
					a = vcard.find("a")
					href = a["href"].encode('ascii', 'ignore')
					addr = util.normalize_addr(a.get_text())
					p_output = p_output_dir+"{0:0=3d}".format(p_order)+"_"+addr
					p_order = p_order + 1
					p_cmd = get_property_url(cmd,user_agent,url_base,href,p_output.encode('ascii', 'ignore'))
					
					print ("	Run property qry : " + p_cmd)
					call(p_cmd, shell=True)
					util.gzip_file(p_output)

					# update current sold date. only update it when it's not none
					sold_date = get_sold_date(vcard)
					if sold_date is not None and sold_date != SOLD_DATE_NA:
						sentinal_sold_date = sold_date

				except:
					print "Unexpected error:", sys.exc_info()[0]

			# if this is for "sold", we only get data for specified time range.
			# check if we should continue for next page
			if not util.if_contine(sentinal_sold_date,sentinal_page_count,SOLD_PAGE_START_FROM,SOLD_PAGE_COUNT):
				break

			sleep(util.delay()) 


fp.close()

