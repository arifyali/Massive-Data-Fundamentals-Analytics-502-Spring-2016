#!/usr/bin/env python2

# Perform a join of:
# * Observations in Table 1
# * Elements in Table 2


from mrjob.job import MRJob
import heapq

class JoinDemo(MRJob):
    def mapper(self, _, line):
        fields = line.split(", ")
        if len(fields)==3:
            self.increment_counter("Info","Obs Count",1)
            yield fields[1], ("Obs", fields)
        elif len(fields)==2:
            self.increment_counter("Info","Name Count",1)
            yield fields[0], ("Name",fields)
        else:
            self.increment_counter("Warn","Invalid Data",1)

    def reducer(self, key, values):
        name = None
        for v in values:
            if len(v)!=2:
                self.increment_counter("Warn","Invalid Join",1)
                continue
            if v[0]=='Name':
                name = v[1]
                continue
            if v[0]=='Obs':
                obs = v[1]
                if name:
                    assert key==name[0]
                    assert key==obs[1]
                    yield obs[0],(obs[1],name[1],obs[2])
                else:
                    self.increment_counter("Warn","Obs without Name")
                    yield obs[0],(obs[1],"n/a",obs[2])



if __name__=="__main__":
    JoinDemo.run()
