# Compute the average salary per job title
# Then print the top 10 job titles. 
# 

from mrjob.job import MRJob
import csv
cols = 'Name,JobTitle,AgencyID,Agency,HireDate,AnnualSalary,GrossPay'.split(",")

class SalaryAvg(MRJob):
    def mapper(self, _, line):
        if line[0]==' ': return
        row = dict(zip(cols, [ a.strip() for a in csv.reader([line]).next()]))
        self.increment_counter("depts",row["Agency"], 1)
        yield row["JobTitle"], int(float(row["AnnualSalary"][1:]))

    def reducer(self, key, values):
        count = 0
        total = 0
        for value in values:
            count += 1
            total += value
        yield key, total / count
        
if __name__=="__main__":
    SalaryAvg.run()


            
