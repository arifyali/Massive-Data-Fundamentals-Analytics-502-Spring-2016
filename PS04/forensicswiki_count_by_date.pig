--
-- part2 problem 4
-- Create a Pig program that reports the number of URLs served each day in 2012 by the forensicswiki.org website

-- Clear the output directory location
--
rmf count_by_date

--
-- Map locally defined functions to the Java functions in the piggybank
--
DEFINE EXTRACT       org.apache.pig.piggybank.evaluation.string.EXTRACT();

--
-- Uncomment the data source you wish to use:

-- This URL uses just one day
-- aw_logs = load 's3://gu-anly502/ps03/forensicswiki.2012-01.unzipped/access.log.2012-01-01' as (line:chararray);
--
-- This URL uses another day:
-- raw_logs = load 's3://gu-anly502/ps03/forensicswiki/access.log.2012-12-31.gz' as (line:chararray);

-- This URL reads a month:
-- raw_logs = load 's3://gu-anly502/ps03/forensicswiki.2012-01.unzipped/access.log.2012-01-??' as (line:chararray);
--
-- This URL reads all of 2012:
raw_logs = load 's3://gu-anly502/ps03/forensicswiki.2012.txt' as (line:chararray);

 
-- logs_base processes each of the lines 
-- FLATTEN takes the extracted values and flattens them into a single tupple
--
logs_base = 
  FOREACH
  raw_logs
  GENERATE
   FLATTEN ( EXTRACT( line,
     '^(\\S+) (\\S+) (\\S+) \\[([^\\]]+)\\] "(\\S+) (\\S+) \\S+" (\\S+) (\\S+) "([^"]*)" "([^"]*)"'
     ) ) AS (
     host: chararray, identity: chararray, user: chararray, datetime_str: chararray, verb: chararray, url: chararray, request: chararray, status: int,
     size: int, referrer: chararray, agent: chararray
     );

-- YOUR CODE GOES HERE
logs = FOREACH logs_base GENERATE ToDate(datetime_str,'dd/MMM/yyyy:HH:mm:ss Z') AS date, host, url, size;
logs2 = FOREACH logs GENERATE SUBSTRING(ToString(date),0,10) AS date, host, url, size;

by_date = GROUP logs2 BY (date);

date_counts = FOREACH by_date GENERATE
group AS date, -- the key you grouped on
COUNT(logs2); -- the number of log lines wiht this date

-- YOUR CODE SHOULD PUT THE RESULTS IN date_counts_sorted
date_counts_sorted = ORDER date_counts BY date;
store date_counts_sorted INTO 'count_by_date' USING PigStorage();


-- Get the results
--
fs -getmerge count_by_date forensicswiki_count_by_date.txt

