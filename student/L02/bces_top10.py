from mrjob.job import MRJob
import heapq, csv


TOPN=10
cols = 'Name,JobTitle,AgencyID,Agency,HireDate,AnnualSalary,GrossPay'.split(",")

class salarymax(MRJob):
    def mapper_init(self):
        self.increment_counter("warn", "missing salary", 0)
        self.increment_counter("warn", "missing gross", 0)

    def mapper(self, _, line):
        if line[0]!=' ':
            row = dict(zip(cols, [ a.strip() for a in csv.reader([line]).next()]))
            try:
                yield "salary", (float(row["AnnualSalary"][1:]), line)
            except ValueError:
                self.increment_counter("warn", "missing salary", 1)
            try:
                yield "gross", (float(row["GrossPay"][1:]), line)
            except ValueError:
                self.increment_counter("warn", "missing gross", 1)

    def reducer(self, key, values):
        for p in heapq.nlargest(TOPN,values):
            yield key, p

    combiner = reducer

if __name__=="__main__":
    salarymax.run()

