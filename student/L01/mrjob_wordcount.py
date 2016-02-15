from mrjob.job import MRJob
import string
import nltk

# Just a helper function that is going to stip all the punctuation away
def clean(s):
    return "".join(c for c in s if not c in string.punctuation)

# The list of stopwords form nltk
# stopwords are words that are common and don't ahve much meaning alone, like "the"

STOPWORDS = nltk.corpus.stopwords.words("english")

# We start with a class that inherits from MRJob (what we imported earlier)
class WordCount(MRJob):
    # The mapper function takes in one item, line by line
    # The string of the line gets passed into "line" 
    # "_" here is the position in the file, which we don't use
    def mapper(self, _, line):
        # clean up the line
        line = unicode(clean(line.lower()), errors="ignore")
        
        # split the line into toeksn on whitespace
        for token in line.split():
            # If the word is a stopword, just ignore it
            if token in STOPWORDS:
                continue
            
            # yield is used to "return" words to the MapReduce framework from the mapper
            # In this case, we are basically saying "we saw 'token' once
            yield token, 1

    # The reducer function receives a single key and list (generator) or values
    def reducer(self, key, values):
        # for example, key might be "python" and the values might be "[1,1,1,1,1]"
        s = sum(values)
        # only output words that were seen more than 3 times
        if s > 3:
            # yeild is used again here to tell MapReduce framework what to output:
            yield key, s
    # The combiner is a mini-reduc that is performed on the map side
    # It basically does a word count on just one input partition and has the same logic as the
    # reducer here
    combiner = reducer

if __name__ == "__main__":
    wordCount.run()


