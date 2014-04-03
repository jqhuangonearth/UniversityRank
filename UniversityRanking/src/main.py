"""
@description: main portal
@author: Bolun
"""
import data_processing as dp
import algorithms as algo
import networkx as nx

def main():
    node_list, edge_list = dp.read_data("../data/data_top50_cs.csv")
    G = nx.DiGraph()
    G = dp.construct_graph(node_list, edge_list)
    weighted_pagerank = algo.weighted_pagerank(G, damping_factor = 0.85, max_iterations = 100, min_delta = 0.00001)
    
    result = sorted(weighted_pagerank.iteritems(), key = lambda asd:asd[1], reverse = True)
    
    f = open("../result/univ_top_50_cs_weightedpagerank.csv","w")
    for r in result:
        f.write("%s;%.5f\n" %(r[0], r[1]))
    f.close()
    
if __name__ == "__main__":
    main()