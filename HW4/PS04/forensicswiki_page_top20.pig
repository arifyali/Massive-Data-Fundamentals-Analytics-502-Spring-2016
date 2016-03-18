--
-- part2 problem 4
-- Create a Pig program that reports the number of URLs served each day in 2012 by the forensicswiki.org website

-- Clear the output directory location
--
rmf forensicswiki_count_by_date

--
-- Map locally defined functions to the Java functions in the piggybank
--
DEFINE EXTRACT       org.apache.pig.piggybank.evaluation.string.EXTRACT();

-- This URL uses just one day
-- raw_logs = load 's3://gu-anly502/ps03/forensicswiki.2012-01.unzipped/access.log.2012-01-01' as (line:chararray);
--
-- This URL reads a month:
raw_logs = load 's3://gu-anly502/ps03/forensicswiki.2012-01.unzipped/access.log.2012-01-??' as (line:chararray);
--
-- This URL reads all of 2012:
--raw_logs = load 's3://gu-anly502/ps03/forensicswiki.2012.txt' as (line:chararray);

 
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

logs = FOREACH logs_base GENERATE ToDate(SUBSTRING(datetime_str,0,11),'dd/MMM/yyyy') AS date, url;
logs2 = FOREACH logs GENERATE SUBSTRING(ToString(date),0,10) AS date, url;
logs_2012 = FILTER logs2 BY SUBSTRING(date,0,4)=='2012';
logs3 = FOREACH logs_2012 GENERATE REGEX_EXTRACT(url,'(index.php\\?title=|/wiki/)([^ &]*)',2) AS wiki, date;

logs3_1 = FILTER logs3 BY wiki!='' and wiki!='-';
by_wiki = GROUP logs3_1 BY wiki;
wikicount = FOREACH by_wiki GENERATE group AS wiki, COUNT(logs3_1) AS counts;

-- PUT YOUR RESULTS IN output
sorted_counts =  ORDER wikicount BY counts DESC;
top20 = limit sorted_counts 20;
STORE top20 INTO 'forensicswiki_page_top20' USING PigStorage();


-- Get the results
--
fs -getmerge forensicswiki_page_top20 forensicswiki_page_top20.txt

