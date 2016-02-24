#!/usr/bin/env python2

# To get started with the join, 
# try creating a new directory in HDFS that has both the fwiki data AND the maxmind data.

import mrjob
from mrjob.job import MRJob
from weblog import Weblog       # imports class defined in weblog.py
import os

class FwikiMaxmindJoin(MRJob):
    # Handle non-ASCII characters in some of the forensicswiki lines
    INTERNAL_PROTOCOL = mrjob.protocol.PickleValueProtocol
    OUTPUT_PROTOCOL = mrjob.protocol.PickleValueProtocol

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
        
        # output <date,1>
        yield CHANGEME


    def reducer(self, key, values):
        yield CHANGEME


if __name__=="__main__":
    FwikiMaxmindJoin.run()
