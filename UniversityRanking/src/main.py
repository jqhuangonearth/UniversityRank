"""
@description: main portal
@author: Bolun
"""
import data_processing as dp
import algorithms as algo
import networkx as nx

def main():
    
#     bucket = {}
#     f = open("../result/result_top50_cs_newdata_apr09/year_statistical_from1995_to2015.csv","r")
#     f.readline()
#     for line in f:
#         lines = line.split(",")
#         try:
#             bucket.update({lines[0].strip() : int(lines[2].strip())})
#         except:
#             pass
#     f.close()
#     
#     node_list, edge_list = dp.read_data_in_range("../data/data_may28_new/data_top50_ee.csv", 
#                                                  "../data/data_may28_new/top50_ee_2015.txt",
#                                                  start_year = 1992, end_year = 2013, self_edge = True)
    
    node_list, edge_list = dp.read_data("../data/data_may28_new/data_top50_ee.csv", 
                                        "../data/data_may28_new/top50_ee_2015.txt", 
                                        self_edge = False, extended = False)
    print len(node_list), node_list
    print len(edge_list), edge_list
    
    exit(0)
    
    G = dp.construct_graph(node_list, edge_list)
    
    top_50 = []
    f = open("../data/data_may28_new/top50_ee_2015.txt","r")
    for line in f:
        line = line.strip().lower()
        top_50.append(line)
    f.close()
    
    print len(G.edges())
    print len(G.nodes())

    nodes = dp.rank_univ(G, t = "in_degree")
    f = open("../result/result_may28/ee/comparison/ee_1951-1991_indegree.csv","w")
    for node in nodes:
        if node[0] in top_50:
            f.write("%s;%d\n" %(node[0], node[1]))
    f.close()

    weighted_pagerank = algo.weighted_PR_wnorm(G, damping_factor = 0.85, max_iterations = 100, min_delta = 0.00001)
    result = sorted(weighted_pagerank.iteritems(), key = lambda asd:asd[1], reverse = True)
    f = open("../result/result_may28/ee/comparison/ee_1992-2013_weightedPR_w_norm.csv","w")
    for r in result:
        if r[0] in top_50:
            f.write("%s;%.5f\n" %(r[0], r[1]))
    f.close()
    
    weighted_pagerank = algo.weighted_PR_wonorm(G, damping_factor = 0.85, max_iterations = 100, min_delta = 0.00001)
    s = sum(weighted_pagerank.values())
    for rank in weighted_pagerank:
        weighted_pagerank[rank] = weighted_pagerank[rank]*50.0/s
    result = sorted(weighted_pagerank.iteritems(), key = lambda asd:asd[1], reverse = True)
    f = open("../result/result_may28/ee/comparison/ee_1992-2013_weightedPR_wo_norm.csv","w")
    for r in result:
        if r[0] in top_50:
            f.write("%s;%.5f\n" %(r[0], r[1]))
    f.close()
#    
#     hits = algo.HITS(G, max_iterations = 100, min_delta = 0.00001)
#     result = sorted(hits.iteritems(), key = lambda asd:asd[1], reverse = True)
#     f = open("../result/result_may28/me/extendedGwselfedges/cs_hits.csv","w")
#     for r in result:
#         if r[0] in top_50:
#             f.write("%s;%.5f\n" %(r[0], r[1]))
#     f.close()
       
    hits = algo.weighted_HITS(G, max_iterations = 100, min_delta = 0.00001)
    result = sorted(hits.iteritems(), key = lambda asd:asd[1], reverse = True)
    f = open("../result/result_may28/ee/comparison/ee_1992-2013_hits_weighted.csv","w")
    for r in result:
        if r[0] in top_50:
            f.write("%s;%.5f\n" %(r[0], r[1]))
    f.close()
    
    hubavg = algo.hubavg_HITS(G, max_iterations = 100, min_delta = 0.00001)
    result = sorted(hubavg.iteritems(), key = lambda asd:asd[1], reverse = True)
    f = open("../result/result_may28/ee/comparison/ee_1992-2013_hits_hubavg.csv","w")
    for r in result:
        if r[0] in top_50:
            f.write("%s;%.5f\n" %(r[0], r[1]))
    f.close()

#     salsa = algo.SALSA(G)
#     result = sorted(salsa.iteritems(), key = lambda asd:asd[1], reverse = True)
#     f = open("../result/result_top50_cs_newdata_apr09/result_top50_cs/univ_top50_cs_from2000_salsa.csv","w")
#     for r in result:
#         f.write("%s;%.5f\n" %(r[0], r[1]))
#     f.close()
#       
#     salsa = algo.modified_SALSA(G)
#     result = sorted(salsa.iteritems(), key = lambda asd:asd[1], reverse = True)
#     f = open("../result/result_top50_cs_extended/entire/univ_top40_me_from1946_to1990_salsa_modified.csv","w")
#     for r in result:
#         if r[0] in top_50:
#             f.write("%s;%.5f\n" %(r[0], r[1]))
#     f.close()
#  
#     credit = algo.CreditPropagation(G, original_rank = hits, cr = 0.8, max_iterations = 10000, min_delta = 0.00001)
#     result = sorted(credit.iteritems(), key = lambda asd:asd[1], reverse = True)
#     f = open("../result/result_top50_cs_newdata_apr09/result_top50_cs_subtracted_woselfedge/univ_top50_cs_wo_selfedges_CreditProp_hits.csv","w")
#     for r in result:
#         if r[0] in top_50:
#             f.write("%s;%.5f\n" %(r[0], r[1]))
#     f.close()


    """ new experiments on authavg and weightedHITS_normalized @ May 13th """
#     authavg = algo.authavg_HITS(G, max_iterations = 100, min_delta = 0.00001)
#     result = sorted(authavg.iteritems(), key = lambda asd:asd[1], reverse = True)
#     f = open("../result/me/univ_top40_me_from1946_to1990_hits_authavg.csv","w")
#     for r in result:
#         if r[0] in top_50:
#             f.write("%s;%.5f\n" %(r[0], r[1]))
#     f.close()
#     
#     hits_n = algo.weighted_HITS_normalized(G, max_iterations = 100, min_delta = 0.00001)
#     result = sorted(hits_n.iteritems(), key = lambda asd:asd[1], reverse = True)
#     f = open("../result/me/univ_top40_me_from1946_to1990_hits_weighted_normalized.csv","w")
#     for r in result:
#         if r[0] in top_50:
#             f.write("%s;%.5f\n" %(r[0], r[1]))
#     f.close()
    

    
if __name__ == "__main__":
    main()