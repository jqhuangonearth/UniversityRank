"""
@description: main portal
@author: Bolun
"""
import data_processing as dp
import algorithms as algo
import networkx as nx

def main():
    node_list, edge_list = dp.read_data("../data/data_top50_cs.csv")
    G = dp.construct_graph(node_list, edge_list)
    
    top_50 = []
    f = open("../data/univ_top_50_cs.csv","r")
    for line in f:
        line = line.strip().lower()
        top_50.append(line)
    f.close()
    
    weighted_pagerank = algo.weighted_PR_wnorm(G, damping_factor = 0.85, max_iterations = 100, min_delta = 0.00001)
    result = sorted(weighted_pagerank.iteritems(), key = lambda asd:asd[1], reverse = True)
    print result
    f = open("../result/result_top50_cs_extended/univ_top_50_cs_extended_weightedPR_w_norm.csv","w")
    for r in result:
        f.write("%s;%.5f\n" %(r[0], r[1]))
    f.close()
  
    weighted_pagerank = algo.weighted_PR_wonorm(G, damping_factor = 0.85, max_iterations = 100, min_delta = 0.00001)
    result = sorted(weighted_pagerank.iteritems(), key = lambda asd:asd[1], reverse = True)
    print result
    f = open("../result/result_top50_cs_extended/univ_top_50_cs_extended_weightedPR_wo_norm.csv","w")
    for r in result:
        f.write("%s;%.5f\n" %(r[0], r[1]))
    f.close()
  
    hits = algo.HITS(G, max_iterations = 100, min_delta = 0.00001)
    result = sorted(hits.iteritems(), key = lambda asd:asd[1], reverse = True)
    print result
    f = open("../result/result_top50_cs_extended/univ_top_50_cs_extended_hits.csv","w")
    for r in result:
        f.write("%s;%.5f\n" %(r[0], r[1]))
    f.close()
      
    hits = algo.weighted_HITS(G, max_iterations = 100, min_delta = 0.00001)
    result = sorted(hits.iteritems(), key = lambda asd:asd[1], reverse = True)
    print result
    f = open("../result/result_top50_cs_extended/univ_top_50_cs_extended_hits_weighted.csv","w")
    for r in result:
        f.write("%s;%.5f\n" %(r[0], r[1]))
    f.close()
  
    hubavg = algo.hubavg_HITS(G, max_iterations = 100, min_delta = 0.00001)
    result = sorted(hubavg.iteritems(), key = lambda asd:asd[1], reverse = True)
    print result
    f = open("../result/result_top50_cs_extended/univ_top_50_cs_extended_hits_hubavg.csv","w")
    for r in result:
        f.write("%s;%.5f\n" %(r[0], r[1]))
    f.close()
    
    salsa = algo.SALSA(G)
    result = sorted(salsa.iteritems(), key = lambda asd:asd[1], reverse = True)
    f = open("../result/result_top50_cs_extended/univ_top_50_cs_extended_salsa.csv","w")
    for r in result:
        f.write("%s;%.5f\n" %(r[0], r[1]))
    f.close()
    
    salsa = algo.modified_SALSA(G)
    result = sorted(salsa.iteritems(), key = lambda asd:asd[1], reverse = True)
    f = open("../result/result_top50_cs_extended/univ_top_50_cs_extended_salsa_modified.csv","w")
    for r in result:
        f.write("%s;%.5f\n" %(r[0], r[1]))
    f.close()
    
if __name__ == "__main__":
    main()