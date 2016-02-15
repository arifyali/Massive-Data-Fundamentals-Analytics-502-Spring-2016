#!/usr/bin/env python2

# Print the min and max datetime for each file in the weblog directory

import mrjob
from mrjob.job import MRJob
from weblog import Weblog       # imports class defined in weblog.py
import os

class WeblogBounds(MRJob):
    def mapper(self, _, line):
        # Get the name of the input file, per mrjob v0.4.6 documentation
        # https://pythonhosted.org/mrjob/utils-compat.html
        filename = mrjob.compat.jobconf_from_env("map.input.file")

        # parse the weblog input line
        log = Weblog(line)      
        
        # output <filename,datetime>
        yield filename,log.datetime


    def reducer(self, key, values):
        # find the minimum and the maximum date for each key
        # notice that we can't simply say min(values) and max(values), because we need to compute
        # both at the same time (we don't want to consume the values)
        vmin = None
        vmax = None
        for v in values:
            if v<vmin or not vmin: vmin=v
            if v>vmax or not vmax: vmax=v
        yield (key,(vmin,vmax))


if __name__=="__main__":
    WeblogBounds.run()
