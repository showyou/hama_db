#!/usr/bin/env python
import sys
import re

def convert(input):
    candidate = re.search("([^:]+)?:([^:]+)?:([^:]+)?:(.+)",input)
    if candidate == None: return ""
    temp = candidate.groups()[:-1]
    temp2 = candidate.groups()[-1].split()
    result = list(temp)+temp2
    return result

def readFile(filename):
    f = open(filename)
    data = f.read()
    f.close()
    lines = data.split('\n')
    print '<?xml version="1.0" encoding="UTF-8"?><testsuite name="nosetests" tests="1" errors="0" failures="1" skip="0">'
    for line in lines:
        #print line
        a = convert(line)
        #print a
        if len(a) > 2:
            print "<testcase classname=\"analyzer.testQuickAnalyzer\" name=\"pep8\" time=\"0\"><failure type=\"exceptions.AssertionError\">",\
                a[3]," ".join(a[4:]),"</failure></testcase>"
    print '</testsuite>'

if __name__ == "__main__":
    if len(sys.argv) > 1:
        readFile(sys.argv[1])
    else:
        print "usage: pep2junit filename"

