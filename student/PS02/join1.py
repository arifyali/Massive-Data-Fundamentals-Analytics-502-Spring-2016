#!/usr/bin/env python2

# To get started with the join, 
# try creating a new directory in HDFS that has both the fwiki data AND the maxmind data.

import mrjob
from mrjob.job import MRJob
from weblog import Weblog       # imports class defined in weblog.py
import os

class FwikiMaxmindJoin(MRJob):
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
        yield CHANGEME


if __name__=="__main__":
    FwikiMaxmindJoin.run()
