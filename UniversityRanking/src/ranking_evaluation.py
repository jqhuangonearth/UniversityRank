"""
@description: evaluate the results with ground truth using somewhat like "edit distance" metrics
@author: Bolun
"""
import math

def rank_dist(list1 = [], list2 = []):
    dist = 0.0
    if len(list1) == 0 and len(list2) == 0:
        return dist
    elif len(list1) == 0:
        return float('inf')
    elif len(list2) == 0:
        return float('inf')
    elif len(list1) != len(list2):
        return float('inf')
    else:
        dict1 = {}
        dict2 = {}
        for i in range(len(list1)):
            dict1.update({list1[i] : i})
        for i in range(len(list2)):
            dict2.update({list2[i] : i})
        for key in dict1:
            if dict2.has_key(key):
                dist += math.fabs(dict1[key]-dict2[key])
            else:
                return float('inf')
        dist /= float(len(list1))
    return dist


def rank():
    list1 = []
    list2 = []
    f = open("../data/univ_top_50_cs.csv","r")
    for line in f:
        list1.append(line.strip())
    f.close()
    
    