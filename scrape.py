#!/usr/bin/python

from time import sleep
from subprocess import call

index=0
cmd="wget -U 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20070802 SeaMonkey/1.1.4' http://www.realestate.com.au/buy/in-donvale%2c+vic+3111/list-1?activeSort=list-date -O list"

while(True):
    call(cmd + str(index), shell=True)

    index=index+1

    print "downloaded "+str(index)

    sleep(1) 
