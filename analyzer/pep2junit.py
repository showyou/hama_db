#!/usr/bin/env python
import sys
import re

def convert(input):
    candidate = re.search("([^:]+)?:([^:]+)?:([^:]+)?:(.+)?",input)
    temp = candidate.groups()[:-1]
    temp2= candidate.groups()[-1].split()
    return temp, temp2

def readFile(filename):
    f = open(filename)
    data = f.read()
    f.close()
    lines = data.split('\n')
    for line in lines:
        print line
        print convert(line)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        readFile(sys.argv[1])
    else:
        print "usage: pep2junit filename"

