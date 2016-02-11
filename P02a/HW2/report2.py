#!/usr/bin/env python2

# Output the number of URLs served on each day
# input is a weblog

import mrjob
from mrjob.job import MRJob
from weblog import Weblog       # imports class defined in weblog.py
import os

class URLTally(MRJob):
    def mapper(self, _, line):
	filename = mrjob.compat.jobconf_from_env("map.input.file")
        log = Weblog(line)
        # add code here to filter out the Special: pages, which are the pages that
        # have "Special:" in the URL
	# Couldn't get filer to work so used this instead
	# http://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-substring-method
	if "Special:" not in log.url:
		yield (log.date,1)
	else:
		yield (log.date,0)		
	
        # add your code here to extract the date field from line and yield the <key,value>
        # where the key is the date of the web log value and the value is 1


    def reducer(self, key, values):
	yield (key,sum(values))
        # Add your code here to sum the number of values for each key
        # and yield the results


if __name__=="__main__":
    URLTally.run()
