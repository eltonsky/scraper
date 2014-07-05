#!/usr/bin/python

import subprocess,sys,util

idx = []

suburb_list = sys.argv[1]
num_process=sys.argv[2]

file_len = util.file_len(suburb_list)

print('./scrape.py ' + suburb_list + ',' + str(file_len) +','+ str(num_process))

i=0
while i < int(num_process):
	idx.append(i)
	i=i+1

# launch multiple async calls:
procs = [subprocess.Popen(['./scrape.py', suburb_list, str(file_len), str(num_process), str(index)]) for index in idx]
# wait to finish.
for proc in procs:
    proc.wait()
# check for results:
if any(proc.returncode != 0 for proc in procs):
    print 'Something failed'