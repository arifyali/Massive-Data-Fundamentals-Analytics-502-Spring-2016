#!/usr/bin/env python
import re,csv

cols = "geoname_id,locale_code,continent_code,continent_name,country_iso_code,country_name".split(",")

def ipaddr_to_binary(ipaddr):
    return "".join([ bin(int(x))[2:].rjust(8,'0') for x in ipaddr.split(".")])    

if __name__=="__main__":
    # Read the geolite locations and cache them locally
    countries_by_geoname_id = {}
    for line in open("GeoLite2-Country-Locations-en.csv"):
        row = dict(zip(cols, [ a.strip() for a in csv.reader([line]).next()]))
        countries_by_geoname_id[row['geoname_id']] = row['country_name']

    # Read the geolite database as binary prefixes...
    geolite_parser = re.compile("([0-9.]+)/(\d+),(\d+)")
    countries_by_ipaddr_prefix = {}
    for line in open("GeoLite2-Country-Blocks-IPv4.csv"):
        m = geolite_parser.match(line)
        if m:
            (ipaddr,mask,geoname_id) = m.groups()
            ipbinary = ipaddr_to_binary(ipaddr)
            # Keep the significant digits
            ipbinary = ipbinary[0:int(mask)]
            countries_by_ipaddr_prefix[ipbinary] = countries_by_geoname_id[geoname_id]

    # Now read the list of top IP addresses and generate the output
    top_parser = re.compile('"([0-9.]+)"')
    for line in open("top1000ips.txt"):
        m = top_parser.search(line)
        if m:
            ipaddr = m.group(1)
            ipbinary = ipaddr_to_binary(ipaddr)
            # Now keep taking 1 bit off the address until we find a match
            while ipbinary!="":
                if ipbinary in countries_by_ipaddr_prefix:
                    print("%s\t%s" % (ipaddr,countries_by_ipaddr_prefix[ipbinary]))
                    break
                ipbinary = ipbinary[0:-1]
                
        
            
            
            

