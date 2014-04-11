"""
@decription: this piece of code exclusively examine how the cr parameter impacts the result of credit propagation

@author: Bolun
"""
import data_processing as dp
import algorithms as algo
import networkx as nx
import ranking_evaluation as reval

list1 = []
f = open("../data/univ_top_50_cs.csv","r")
for line in f:
    list1.append(line.strip())
f.close()

node_list, edge_list = dp.read_data("../data/data_top50_cs.csv")
G = dp.construct_graph(node_list, edge_list)

# orank = algo.weighted_PR_wonorm(G, damping_factor = 0.85, max_iterations = 100, min_delta = 0.00001)
# s = sum(orank.values()) 
# for rank in orank:
#     orank[rank] = orank[rank]*50.0/s
# result = sorted(orank.iteritems(), key = lambda asd:asd[1], reverse = True)

orank = algo.HITS(G, max_iterations = 100, min_delta = 0.00001)
result = sorted(orank.iteritems(), key = lambda asd:asd[1], reverse = True)
print result

f = open("../result/result_top50_cs/CreditPropagation_hits_evaluation.csv","w")
f.write("cr;dist\n")
i = 0.0
while (i <= 1.0):
    credit = algo.CreditPropagation(G, original_rank = orank, cr = i, max_iterations = 100, min_delta = 0.00001)
    result = sorted(credit.iteritems(), key = lambda asd:asd[1], reverse = True)
    #print result

    list2 = [e[0] for e in result]
    #distr = reval.diff_distribution(list1, list2)
    dist = reval.rank_dist(list1, list2)
    f.write("%.2f;%.2f\n" %(i, dist))
    i += 0.02
    print dist
    
f.close()