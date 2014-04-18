#!/usr/bin/python

from time import sleep
from subprocess import call

index=0

user_agent="'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20070802 SeaMonkey/1.1.4'"
url_base="http://www.realestate.com.au/buy/"
suburb="in-donvale%2c+vic+3111/"
output="list."
page="list-"
url_sort_date="?activeSort=list-date"
cmd="wget -U {0} {1} -O {2}"

while(True):
	curr_cmd=cmd.format(user_agent, url_base+suburb+page+"1"+url_sort_date, output+"1")

	print ("Run: " + curr_cmd)

	call(curr_cmd, shell=True)

	index=index+1

	print ("downloaded "+str(index) )
	
	sleep(1) 




