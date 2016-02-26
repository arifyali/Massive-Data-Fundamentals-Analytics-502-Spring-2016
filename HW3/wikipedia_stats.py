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

class wikipedia_stats(MRJob):
	def mapper(self, _, line):
		article = line.split('\t')
		yield article[1], 1

	def reducer(self, key, value):
		yield key, sum(value)

	def mapper_two(self, key, value):
			yield "WikiMods", (key, value)

	def reducer_two(self, key, value):
			yield value[0], value[1]

	def steps(self):
		return [
			MRStep(mapper=self.mapper,
				   reducer=self.reducer),
			MRStep(mapper=self.mapper_two,
				   reducer=self.reducer_two) ]	

if __name__ == "__main__":
    wikipedia_stats.run()