# Compute the average salary per job title
# Then print the top 10 job titles. 
# 

from mrjob.job import MRJob
from mrjob.step import MRStep
cols = 'SchoolID,Name,State,Students'.split(",")

class schoolCount(MRJob):
    def mapper(self, _, line):
        row = dict(zip(cols, line.split("\t")))
        for rname in ["SchoolID","Students"]:
            row[rname] = int(row[rname])
        yield row["State"], row

    def reducer(self, key, values):
        sum = 0
        count = 0
        for row in values:
            sum += row["Students"]
            count += 1
        if count > 0:
            yield key, (sum, count)
        

if __name__=="__main__":
    schoolCount.run()


            
