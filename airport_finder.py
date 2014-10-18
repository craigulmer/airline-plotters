import sys
import gzip
import bz2
from math import *
from numpy import *
from collections import defaultdict

# Globals
cutoff=0


def parseWkt(s):
    s2 = s.replace("LINESTRING (","").replace(")","");
    vals = s2.split(",")

    array2d = [[float(digit) for digit in line.split()] for line in vals]
    return array2d;


if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = raw_input('Enter wkt file: ')



if filename.endswith(".gz"):
    file = gzip.open(filename)
elif filename.endswith(".bz2"):
    file = bz2.BZ2File(filename)
else:
    file = open(filename)

d=defaultdict(list)
num=0
for line in file:
    (np,tag,swkt)=line.split('\t');
    (plane,airline,src,dst)=tag.split('|')

    if (src=="") or (np<4):
        continue

    data = parseWkt(swkt)
    if (data[0][2] <= cutoff):
        continue

    val = data[0][0:2]
    d[src].append(val)

    num=num+1
    if (num>=500):
        break
    #    print d.items()
    #    exit(0)

print "Done: count ",num
for k,v in d.iteritems():
    centroid = mean(v,axis=0)
    print k,"-->",v,"-->",centroid
    
