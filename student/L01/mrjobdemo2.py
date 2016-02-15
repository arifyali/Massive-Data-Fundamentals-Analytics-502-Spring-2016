from mrjob.job import MRJob

# this demo shows that the values to the reducer are sorted.

class MRSortDemo(MRJob):

    def mapper(self, _, line):
        print("mapper. _=",_,"line:",line)
        key,value = line.split("\t")
        yield int(key),int(value)

    def reducer(self, key, values):
        print("key=",key)
        print("values=",list(values))
        yield key, sum(values)


if __name__ == '__main__':
    MRSortDemo.run()
