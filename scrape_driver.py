#!/usr/bin/python

import subprocess,sys,util

# check args
if len(sys.argv) != 4:
	print "WARN: Usage : scrape_driver {suburb_list_file} {mode (buy|sold)} {num_process}"
	exit(0)

idx = []

suburb_list_file = sys.argv[1]
mode = sys.argv[2]
num_process=sys.argv[3]

# if start & end suburb index are passed in
start=-1
end = -1
if len(sys.argv) > 4:
	start = sys.argv[4]
	end = sys.argv[5]

file_len = util.file_len(suburb_list_file)

print('./scrape.py ' + suburb_list_file + ',' + str(file_len) +','+ str(num_process) + "," + str(start)+","+str(end))

i=0
while i < int(num_process):
	idx.append(i)
	i=i+1

# launch multiple async calls:
procs = [subprocess.Popen(['./scrape.py', suburb_list_file, mode, str(file_len), str(num_process), str(index), str(start), str(end)]) for index in idx]
# wait to finish.
for proc in procs:
    proc.wait()
# check for results:
if any(proc.returncode != 0 for proc in procs):
    print 'Something failed'
    

