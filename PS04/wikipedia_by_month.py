#!/usr/bin/spark-submit
#
# Problem Set #4
# Implement wordcount on the shakespeare plays as a spark program that:
# a.Removes characters that are not letters, numbers or spaces from each input line.
# b.Converts the text to lowercase.
# c.Splits the text into words.
# d.Reports the 40 most common words, with the most common first.

# Note:
# You'll have better luck debugging this with ipyspark

import sys
from operator import add
from pyspark import SparkContext

if __name__ == "__main__":
    
    ##
    ## Parse the arguments
    ##

    infile =  's3://gu-anly502/ps03/freebase-wex-2009-01-12-articles.tsv'

    ## 
    ## Run WordCount on Spark
    ##

    sc     = SparkContext( appName="Wikipedia Count" )
    lines  = sc.textFile( infile )
    ## YOUR CODE GOES HERE
    counts = lines.map(lambda line: line.split('\t'))\
                  .map(lambda article: (article[2])[0:7]) \
                  .map(lambda date: (date, 1)) \
                  .reduceByKey(add)
    ## PUT YOUR RESULTS IN counts
    sorted_counts = counts.sortBy(lambda x: x[1], ascending=False).collect()

    with open("wikipedia_by_month.txt","w") as fout:
        for (date, count) in sorted_counts:
            fout.write("{}\t{}\n".format(date,count))
    
    ## 
    ## Terminate the Spark job
    ##

    sc.stop()
