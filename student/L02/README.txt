This directory contains the wordcount and wordcount top-10 demos from L02.

It also contains an analysis of the Baltimore City Employees Sallaries which computes the highest
paying job and the top-10 highest paying jobs.

You will note that the top-10 in wordcount needs to use a
mapper_init(), mapper() and mapper_final(), while the BCSE job
performs the top-N in the reducer alone. How is this possible? It
turns out that the wordcount reducer has to reduce multiple values to
sum them---there is a transformation from the input values to the
output values happening in the reducer. To enable this transformation,
the key is the word that is being counted. 

However, the BCSE job is not transforming the data at all---it is
simply selecting a 10 key/value pairs from the input. So the "key" is
the word "salary" and the word "gross", and the value is a tuple
containing the salary (or gross) and the original line. Thus the
reduce sees *all* of the values and it can select the top-10. This all
happens in the heapq.nlargest() function call, which consumes all of
the values for the given key (which is either "salary" or "gross")

bcse_2step.py demonstrates a 2-step job. It computes the average
salary for the top 5 job categories.


To run the Shakespear wordcount demos on Hadoop:

Run inline:
$ python wordcount.py -r inline hamlet.txt
$ python wordcount_top10.py -r inline hamlet.txt

Run locally:
$ python wordcount.py -r local hamlet.txt
$ python wordcount_top10.py -r local hamlet.txt

Run on hadoop:
$ export HADOOP_HOME=/usr/lib/hadoop-mapreduce
$ python wordcount.py -r hadoop --hadoop-bin=/usr/bin/hadoop hamlet.txt
$ python wordcount_top10.py -r hadoop --hadoop-bin=/usr/bin/hadoop hamlet.txt








