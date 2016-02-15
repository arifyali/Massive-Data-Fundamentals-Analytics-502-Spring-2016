#!/usr/bin/env python2

# Output the number of URLs served on each day
# input is a weblog

import mrjob
from mrjob.job import MRJob
from weblog import Weblog       # imports class defined in weblog.py
import os

class URLTally(MRJob):
    def mapper(self, _, line):

        # add code here to filter out the Special: pages, which are the pages that
        # have "Special:" in the URL

        # add your code here to extract the date field from line and yield the <key,value>
        # where the key is the date of the web log value and the value is 1


    def reducer(self, key, values):
        # Add your code here to sum the number of values for each key
        # and yield the results


if __name__=="__main__":
    URLTally.run()
