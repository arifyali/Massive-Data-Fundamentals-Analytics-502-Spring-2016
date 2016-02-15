from mrjob.job import MRJob
from mrjob.step import MRStep
import heapq, csv

cols = 'Name,JobTitle,AgencyID,Agency,HireDate,AnnualSalary,GrossPay'.split(",")

class salarymax(MRJob):
    def mapper(self, _, line):
        row = dict(zip(cols, [ a.strip() for a in csv.reader([line]).next()]))
        yield "salary", (float(row["AnnualSalary"][1:]), line)
        yield "gross", (float(row["GrossPay"][1:]), line)

    def reducer(self, key, values):
        for p in heapq.nlargest(10,values):
            yield key, p

    combiner = reducer

if __name__=="__main__":
    salarymax.run()

