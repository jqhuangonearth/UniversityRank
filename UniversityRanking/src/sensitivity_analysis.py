"""
@description: for hits algorithm, by adding none existing edges to see the diff of the rank of that univ

@author: Bolun
"""

import data_processing as dp
import algorithms as algo
import networkx as nx

def sensitive():
    node_list, edge_list = dp.read_data_in_range("../data/data_top50_cs_apr09.csv", start_year = 1995, end_year = 2015)
    G = dp.construct_graph(node_list, edge_list)
#     print len(G.nodes()), G.nodes()
#     print len(G.edges(data = True)), G.edges(data = True)
#     
#     print G.in_edges("harvard")
    
    top_50 = []
    f = open("../data/univ_top_50_cs.txt","r")
    for line in f:
        line = line.strip().lower()
        top_50.append(line)
    f.close()
    
    weighted_pagerank = algo.weighted_PR_wonorm(G, damping_factor = 0.85, max_iterations = 100, min_delta = 0.00001)
    result = sorted(weighted_pagerank.iteritems(), key = lambda asd:asd[1], reverse = True)
    
    res1 = []
    for e in result:
        if e[0] in top_50:
            res1.append(e)
    G = add_non_existing_edges(G, univ = "yale", fake_node = "mit", weight = 2)
    weighted_pagerank = algo.weighted_PR_wonorm(G, damping_factor = 0.85, max_iterations = 100, min_delta = 0.00001)
    result = sorted(weighted_pagerank.iteritems(), key = lambda asd:asd[1], reverse = True)
    
    res2 = []
    for e in result:
        if e[0] in top_50:
            res2.append(e)
            
    G = add_non_existing_edges(G, univ = "yale", fake_node = "mit", weight = 4)
    weighted_pagerank = algo.weighted_PR_wonorm(G, damping_factor = 0.85, max_iterations = 100, min_delta = 0.00001)
    result = sorted(weighted_pagerank.iteritems(), key = lambda asd:asd[1], reverse = True)
    
    res3 = []
    for e in result:
        if e[0] in top_50:
            res3.append(e)
            
    G = add_non_existing_edges(G, univ = "yale", fake_node = "mit", weight = 6)
    weighted_pagerank = algo.weighted_PR_wonorm(G, damping_factor = 0.85, max_iterations = 100, min_delta = 0.00001)
    result = sorted(weighted_pagerank.iteritems(), key = lambda asd:asd[1], reverse = True)
    
    res4 = []
    for e in result:
        if e[0] in top_50:
            res4.append(e)
            
    G = add_non_existing_edges(G, univ = "yale", fake_node = "mit", weight = 8)
    weighted_pagerank = algo.weighted_PR_wonorm(G, damping_factor = 0.85, max_iterations = 100, min_delta = 0.00001)
    result = sorted(weighted_pagerank.iteritems(), key = lambda asd:asd[1], reverse = True)
    
    res5 = []
    for e in result:
        if e[0] in top_50:
            res5.append(e)

    f = open("../result/result_top50_cs_newdata_apr09/sensitivity/sensitivity_yale_weightedPR_wo_norm_1995-2015.csv", "w")
    f.write("original,mit-2,mit-4,mit-6,mit-8\n")
    for i in range(len(res1)):
        f.write("%s,%s,%s,%s,%s\n" %(res1[i][0],res2[i][0],res3[i][0],res4[i][0],res5[i][0]))
    f.close()
    

def add_non_existing_edges(G, univ = "harvard", fake_node = "mit", weight = 1):
    """
    @type G: DiGraph
    @param G: the graph
    
    @type uinv: String
    @param univ: name of university
    
    @return: new graph with added edges
    """
    G.add_edge("mit", univ, {"weight" : weight})
    return G

    
sensitive()