from mrjob.job import MRJob
from mrjob.step import MRStep
import heapq, csv

names_cols = 'Table,NameID,Name,SchoolID'.split(",")
schools_cols = 'Table,SchoolID,Name,State'.split(",")

class SchoolJoin(MRJob):
    def mapper(self, _, line):
        row = [a.strip() for a in csv.reader([line]).next()]
        if row[0]=='Names':
            rowdict = dict(zip(names_cols,row))
            yield rowdict["SchoolID"], rowdict
        elif row[0]=='Schools':
            rowdict = dict(zip(schools_cols,row))
            yield rowdict["SchoolID"], rowdict
        else:
            self.increment_counter("warn","invalid input line",1)
            
    def reducer(self, key, values):
        # All of the values for the SchoolID will be grouped together
        # Find the school name, the school state, and all the students
        
        students = []
        schoolName  = None
        schoolState = None
        for v in values:
            if v["Table"]=="Schools":
                schoolName = v["Name"]
                schoolState = v["State"]
            elif v["Table"]=="Names":
                students.append(v["Name"])

        yield key, (schoolName,schoolState,students)

if __name__=="__main__":
    SchoolJoin.run()

