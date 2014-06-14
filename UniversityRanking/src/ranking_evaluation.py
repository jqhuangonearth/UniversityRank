"""
@description: evaluate the results with ground truth using somewhat like "edit distance" metrics
@author: Bolun
"""
import math
import random

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


def diff_distribution(list1 = [], list2 = []):
    distribution = {}
    for n in list1:
        distribution.update({n : {"diff": 0.0, "type": "/"}})
    dist = 0.0
    if len(list1) == 0 and len(list2) == 0:
        return dist
    elif len(list1) == 0:
        return distribution
    elif len(list2) == 0:
        return distribution
    elif len(list1) != len(list2):
        return distribution
    else:
        dict1 = {}
        dict2 = {}
        for i in range(len(list1)):
            dict1.update({list1[i] : i})
        for i in range(len(list2)):
            dict2.update({list2[i] : i})

        for key in dict1:
            if dict2.has_key(key):
                if dict1[key] < dict2[key]:
                    distribution[key]["diff"] = math.fabs(dict1[key] - dict2[key])
                    distribution[key]["type"] = "-"
                elif dict1[key] > dict2[key]:
                    distribution[key]["diff"] = math.fabs(dict1[key] - dict2[key])
                    distribution[key]["type"] = "+"
                else:
                    distribution[key]["diff"] = 0.0
                    distribution[key]["type"] = "/"
            else:
                print "diff key detected: %s" %key
                
        return distribution
    
def rank():
    list1 = []
    list2 = []
    f = open("../data/data_may28_new/top50_ee_2015.txt","r")
    for line in f:
        list1.append(line.strip().lower())
    f.close()
    
#     f = open("../result/result_may28/cs/huangs/extendedGwoselfedges/cs_indegree.csv","r")
#     for line in f:
#         lines = line.split(";")
#         list1.append(lines[0].strip())
#     f.close()
    
    f = open("../result/result_may28/ee/comparison/ee_1951-1991_indegree.csv","r")
    for line in f:
        lines = line.split(";")
        list2.append(lines[0].strip())
    f.close()
#     s = 0
#     for i in range(1000):
#         list2 = list(list1)
#         random.shuffle(list2)
#         print list1
#         print list2
#         s += rank_dist(list1, list2)
#     print s / float(1000)
#      
#     exit(0)
    
    distr = diff_distribution(list1, list2)
    distr = sorted(distr.iteritems(), key = lambda asd:asd[1]["diff"], reverse = True)
    print distr
    f = open("../result/result_may28/ee/comparison/ee_1951-1991_diff_indegree.csv","w")
    f.write("univ,ab_diff,+/-\n")
    for item in distr:
        f.write("%s,%.1f,%s\n" %(item[0], item[1]["diff"], item[1]["type"]))
    f.close()
    
    print rank_dist(list1, list2)
    exit(0)
    
    list2 = list(list1)
    random.shuffle(list2)
    print rank_dist(list1, list2)
    
    list1_1 = list1[0:len(list1)/2]
    list1_2 = list1[len(list1)/2:]
    list2 = []
    list2.extend(list1_2)
    list2.extend(list1_1)
    print rank_dist(list1, list2)
    
    list2 = []
    for i in range(len(list1)):
        list2.append(list1[len(list1)-1-i])
    print rank_dist(list1, list2)
    
rank()