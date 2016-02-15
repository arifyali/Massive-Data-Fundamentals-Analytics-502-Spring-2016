# Compute the average salary per job title
# Then print the top 10 job titles. 
# 

from mrjob.job import MRJob
from mrjob.step import MRStep
import csv
import datetime

# Exercise:
# Build a mapping of years of service to mean salary on the baltimore data
# Here are some sample records:

# Here is what I'd like to the output to look like:
# [Years of service], [mean salary, count of people with this many yars]
# e.g.
# ...
# 10      [45581, 480]
# 23      [62000, 121]

# At the bottom of this file there is a number of TOdO's that you need to fill in
# Use the other mrjob examples ot help figure out what you need to do!

# THESE FUNCTIONS ARE TO HELP YOU OUT, DON'T CHANGE THEM
cols = 'Name,JobTitle,AgencyID,Agency,HireDate,AnnualSalary,GrossPay'.split(",")

# This function takes in the raw line from the baltimore data
# It returns a dictionary where the keys are the column names (See "cols" above)
# and the values are the stored values as strings
def parse_line(line_str):
    return dict(zip(cols, [ a.strip() for a in csv.reader([line_str]).next()]))

# This function takes in a string in the form "MM/DD/YYYY"
# HireData in the Baltimore salary data is in this form.
# (You would always use ISO-8601 in your code)
# It reutrns the number of yers ago (rounded down) that date was
def parse_HireDate(date_str):
    if date_str == "":
        return -1
    hd = datetime.datetime.strptime(date_str, "%m/%d/%Y")
    years = (datetime.datetime.now() - hd).days / 365
    return years

# This function takes the AnnualSalary and converts it to an integer
# In the Baltimore salary data, it is stored as "$53414.00"
def parse_AnnaulSalary(salary_str):
    return int(float(salary_str.strip().strip("$")))

### End of helper functions
# TODO: Define a class that inherents off of MRJob
class SeniorityVsSalary(MRJob):

    # Inside the class, TODO: Define a mapper function
    def mapper(self, _, line):
        # inside the mapper function, TODO:
        # 1. parse the line from its current CSV form
        pl = parse_line(line)
        # 2. get the number of years of service based on HireDate
        years = parse_HireDate(pl['HireDate'])
        # 3. get the annual salary from AnnualSalary
        salary = parse_AnnaulSalary(pl['AnnualSalary'])
        # 4. yield a key and a value
        yield years, salary

    # Inside the reducer function, TODO:
    def reducer(self, key, values):
        # 1. convert the generator to a list (since we'll be doing stuff to the list)
        values = list(values)

        # 2. calculate the mean of the list
        med = sum(values) / len(values)

        # 3. get the length of the list
        ll = len(values)

        # 4. yield the information we need
        yield key, (med, ll)

# TODO: use .run() on the class you defined above
SeniorityVsSalary.run()

