#!/usr/bin/python

# TODO:
# 1.handle Ctrl+C
# 2.log

from time import sleep
from subprocess import call
from bs4 import BeautifulSoup
import util, property_parser
import sys, glob, shutil
import time

# 1. find start & end of suburbs
# 2. pick up next batch of .gz files (in the suburbs), order by ts
# 3. for each file,
#	check the gz file integrity (gzip -t)
#	move to progress
#	parse 
#	move to outbox if success / to err if failed

log_dir="./logs/"
p_output_dir_base="./property/"
p_inbox="inbox"
p_outbox="outbox"
p_progress="progress"
p_errbox="err"
p_batch_size = 50


def get_property_list_url(cmd,user_agent,url_base,suburb_format,suburb,postcode,page,index,url_sort_date,output):
	return cmd.format(user_agent, url_base+"buy/"+suburb_format.format(suburb,postcode)+"/"+page+str(index)+"?"+url_sort_date+"&"+includeSurrounding, output)

def get_property_url(cmd, user_agent, url_base, href, output):
	return cmd.format(user_agent,url_base+href,output)

def get_parser(mode):
	if mode == "buy":
		return parser_buy
	else:
		return parser_sold

# suburb list
suburb_list = sys.argv[1]
start = 0
end = 99999

file_len = int(sys.argv[2])
num_process = int(sys.argv[3])
index = int(sys.argv[4])

sys.stdout = open(log_dir+str(index)+"_processor.log", 'w')

start = (file_len/num_process)*index

if index == num_process - 1:
	end = file_len
else:
	end = file_len/num_process*(index+1)

# FOR TEST
# start = 0
# end = 2

print ("Starting processor... reading suburb from " + suburb_list + ", ranging from " + str(start) + " to " + str(end))

# keep running, cos scraper will put new files in.
# while (True):

fp=open(suburb_list)
parser_buy = property_parser.BuyPropertyParser()
parser_sold= property_parser.SoldPropertyParser()

for i, line in enumerate(fp):
	if i >= start and i < end:

		s_ary = line.split()
		postcode=s_ary[0]
		suburb = "_".join(s_ary[1].upper().split(" "))

		print (str(index) + " : Processing " + postcode + " " + suburb)

		list_index=1

		# create properties dir
		#inbox
		curr_inbox = p_output_dir_base + suburb+"/*/*/" + p_inbox + "/*.gz"

		print (curr_inbox)

		# get gz files
		# files will be sorted, it ensures :
		# 1."buy"s are picked up b4 "sold"s
		# 2. files are orderred by date
		for file_inbox in sorted(glob.glob(curr_inbox)):

			try:

				# get file capture date. This will be inserted for most tables.
				date_time = file_inbox.split("/")[3]

				# mv to progress
				file_progress = file_inbox.replace(p_inbox,p_progress)
				if util.move(file_inbox,file_progress) < 0:
					continue

				print ("moved " + file_inbox + " to " + file_progress)

				# get parser by mode
				p_parser = get_parser(file_inbox.split("/")[4])

				# process
				if p_parser.process(file_progress, date_time) < 0:
					print("failed to process " + file_progress)

					file_errbox = file_inbox.replace(p_inbox,p_errbox)
					if util.move(file_progress,file_errbox):
						print ("moved " + file_progress + " to " + file_errbox)
					continue

				file_outbox = file_inbox.replace(p_inbox,p_outbox)

				if util.move(file_progress,file_outbox):
					print ("moved " + file_progress + " to " + file_outbox)  

			except Exception, e:
				print ("failed to process " + file_inbox + " due to : " + str(e))

fp.close()

