-- wordcount_shakespeare3.pig
--
-- Find the top-20 most popular words beginning with a "h",
-- ignoring case.
--
-- Clear the output directory location
--
rmf sorted_words3

--
-- Run the script

shakespeare = LOAD 's3://gu-anly502/ps04/Shakespeare.txt' as (line:chararray);
words = foreach shakespeare generate flatten(TOKENIZE(line)) as word;
grouped = GROUP words by LOWER(word);
hgrouped = FILTER grouped by STARTSWITH(group, 'h');
wordcount = FOREACH hgrouped GENERATE group, COUNT(words);
-- YOUR CODE GOES HERE

-- PUT YOUR RESULTS IN sorted_words20
sorted_words = ORDER wordcount BY $1 DESC;
sorted_words20 = limit sorted_words 20;

STORE sorted_words20 INTO 'sorted_words3' USING PigStorage();
 
-- Get the results
--
fs -getmerge sorted_words3 wordcount_shakespeare3.txt
