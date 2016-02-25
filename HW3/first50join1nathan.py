#!/usr/bin/env python2
#
# 
#

import mrjob
import mrjob.compat
from mrjob.job import MRJob
from mrjob.step import MRStep
import sys

from weblog import Weblog  # imports class defined in weblog.py


class First50Join(MRJob):
    SORT_VALUES = True

    def mapper(self, _, line):
        # Is this a weblog file, or a MaxMind GeoLite2 file?
        filename = mrjob.compat.jobconf_from_env("map.input.file")
        import sys
        if "top1000ips_to_country.txt" in filename:
            # Handle as a GeoLite2 file
            #
            self.increment_counter("Status", "top1000_ips_to_country file found", 1)
            try:
                (ipaddr, country) = line.strip().split("\t")
                yield ipaddr, "+" + country
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
                yield o.ipaddr, line

    # Perform a "first 50" operation in the  join operation
    def reducer_init(self):
        self.lowest = []

    def reducer(self, key, values):
        # values has all the lines for this key
        country = None
        for v in values:
            if v[0] == "+":  # found the location!
                country = v[1:]
                continue
            if not country:  #
                self.increment_counter("Warning", "No Country Found", 1)
                continue
            # If we get here, v is a logfile line. Parse it again
            o = Weblog(v)
            self.increment_counter("Join", "Geolocated", 1)
            self.lowest.append((o.datetime, country, v))
            self.lowest = sorted(self.lowest)[:50]

    def reducer_final(self):
        """Output the lowest 50"""
        for joined_data in self.lowest:
            yield "FIRST50Geolocated", joined_data 

    # Let MapReduce do the sorting this time!
    # All of the keys are the same, so just take the first 50 values...
    def first50reducer_init(self):
        self.counter = 0

    def first50reducer(self, key, values):
        # Implement a reducer that only outputs for the first 50...
        for (date, country, line) in values:
            if self.counter < 50:
                self.counter += 1
                yield key, [date, country, line]

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer_init=self.reducer_init,
                   reducer=self.reducer,
                   reducer_final=self.reducer_final),
            MRStep(reducer_init=self.first50reducer_init,
                   reducer=self.first50reducer) ]

if __name__ == "__main__":
    First50Join.run()
