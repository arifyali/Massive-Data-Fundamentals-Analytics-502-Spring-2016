#!/usr/bin/env python2
#
# 
# To get started with the join, 
# try creating a new directory in HDFS that has both the fwiki data AND the maxmind data.

import mrjob
from mrjob.job import MRJob
from weblog import Weblog       # imports class defined in weblog.py
import os

class First50Join(MRJob):
    def mapper(self, _, line):
        # Is this a weblog file, or a MaxMind GeoLite2 file?
        filename = mrjob.compat.jobconf_from_env("map.input.file")
        if "top1000_ips_to_country.txt" in filename:
            # Handle as a GeoLite2 file
            #
            yield SOMETHING
        else:
            # Handle as a weblog file
            yield SOMETHING
        

    def reducer(self, key, values):
        # Implement your join here, matching up the geolocations and the IP addresses
        yield CHANGEME

    def first50mapper(self,key,value):
        # Implement a "yield" below that gives all of the joins from reducer() above the same
        # key
        yield CHANGEME

    def first50reducer_init(self,key,value):
        self.counter = 0

    def first50reducer(self,key,value):
        # Implement a reducer that only outputs for the first 50...
        if self.counter<50:
            self.counter += 1
            yeild CHANGEME
        

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
           
            MRStep(mapper=self.first50mapper,
                   reducer_init=self.first50reducer_init,
                   reducer=self.first50reducer),
            ]

    


if __name__=="__main__":
    First50Join.run()
