#!/usr/bin/env python2
#
# 
#
from weblog import Weblog       # imports class defined in weblog.py
import heapq
import os


import mrjob
import mrjob.compat
from mrjob.job import MRJob
from mrjob.step import MRStep
import sys

from weblog import Weblog  # imports class defined in weblog.py

TOPN=10
class First50Join(MRJob):
    def mapper(self, _, line):
        SORT_VALUES = True
        # Is this a weblog file, or a MaxMind GeoLite2 file?
        filename = mrjob.compat.jobconf_from_env("map.input.file")
        import sys
        if "top1000ips_to_country.txt" in filename:
            # Handle as a GeoLite2 file
            #
            self.increment_counter("Status", "top1000_ips_to_country file found", 1)
            try:
                (ipaddr, country) = line.strip().split("\t")
                yield ipaddr, ("country", country)
            except ValueError as e:
                pass
        else:
            # Handle as a weblog file
            try:
                o = Weblog(line)
            except ValueError:
                sys.stderr.write("Invalid logfile line: {}\n".format(line))
                return
            if o.wikipage() == "Main_Page":
                yield o.ipaddr, ("ip", line)

    # Perform a "first 50" operation in the  join operation

    def reducer(self, key, values):
        name = None
        for v in values:
            
            if v[0]=='country':
                name = v[1]
                continue
            if v[0]=='ip':
                obs = v[1]
                if name:
                    yield name, 1
                else:
                    self.increment_counter("Warn","countries without Name")
                   

    def mapper_counter(self, key, values):
        yield key, 1

    def reducer_counter(self, key, values):
        yield key, sum(values)


    def top10_mapper(self, word, count):
        # notice that we put the counts first!
        yield "Top10", (count,word) 

    def top10_reducer(self, key, values):
        for values in heapq.nlargest(TOPN,values):
            yield v[1], v[0]

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),

            MRStep(mapper=self.mapper_counter,
                   reducer=self.reducer_counter),

            MRStep(mapper=self.top10_mapper,
                   reducer=self.top10_reducer) ]        


if __name__ == "__main__":
    First50Join.run()
