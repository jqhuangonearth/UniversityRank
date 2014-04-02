#!/usr/bin/env python

"""
@author: Bolun
"""

def read_data():
    s = {}
    
    f = open("../data/data_top50_cs.csv","r")
    f.readline()
    for line in f:
        lines = line.split(",")
        for w in lines:
            if s.has_key(w.strip()):
                s[w.strip()] += 1
            else:
                s.update({w.strip() : 1})
    f.close()
    univlist = sorted(s.iteritems(), key=lambda asd:asd[0], reverse = False)
    fo = open("../data/out.csv","w")
    for i in univlist:
        fo.write("%s,%d\n" %(i[0],i[1]))
    fo.close()
    
read_data()