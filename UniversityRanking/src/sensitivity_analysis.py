"""
@description: for hits algorithm, by adding none existing edges to see the diff of the rank of that univ

@author: Bolun
"""

import data_processing as dp
import algorithms as algo

def sensitive():
    top_50 = []
    f = open("../data/univ_top_50_cs.txt","r")
    for line in f:
        line = line.strip().lower()
        top_50.append(line)
    f.close()
    
    fo = open("../result/result_top50_cs_newdata_apr09/sensitivity/sensitivity_weightedPR_wo_norm_1995-2015+mit1.csv","w")
    node_list, edge_list = dp.read_data_in_range("../data/data_top50_cs_apr09.csv", start_year = 1995, end_year = 2015, self_edge = False)
    G = dp.construct_graph(node_list, edge_list)
    hits = algo.weighted_PR_wonorm(G, damping_factor = 0.85, max_iterations = 100, min_delta = 0.00001)
    result = sorted(hits.iteritems(), key = lambda asd:asd[1], reverse = True)
    G.clear()
    original_r = []
    for e in result:
        if e[0] in top_50:
            original_r.append(e[0])
    fo.write("origin,")
    for node in original_r:
        fo.write("%s," %node)
    fo.write("\n")
    for node in top_50:
        if not node == "mit":
            node_list, edge_list = dp.read_data_in_range("../data/data_top50_cs_apr09.csv", start_year = 1995, end_year = 2015, self_edge = False)
            G = dp.construct_graph(node_list, edge_list)
            G = add_non_existing_edges(G, node, "mit", weight = 1) ### add one edge from MIT to <node>
            hits = algo.weighted_PR_wonorm(G, damping_factor = 0.85, max_iterations = 100, min_delta = 0.00001)
            result = sorted(hits.iteritems(), key = lambda asd:asd[1], reverse = True)
            #result = sorted(hits.iteritems(), key = lambda asd:asd[1], reverse = True)
            G.clear()
            res1 = []
            for e in result:
                if e[0] in top_50:
                    res1.append(e[0])
            fo.write("%s," %node)
            for r in res1:
                fo.write("%s," %r)
            fo.write("\n")
    fo.close()
    
    
def sensitive_2():
    top_50 = []
    f = open("../data/univ_top_50_cs.txt","r")
    for line in f:
        line = line.strip().lower()
        top_50.append(line)
    f.close()
    
    fo = open("../result/result_top50_cs_newdata_apr09/sensitivity/mit+1/sensitivity_diff_CreditProp_hits_1995-2015+mit1.csv","w")
    node_list, edge_list = dp.read_data_in_range("../data/data_top50_cs_apr09.csv", start_year = 1995, end_year = 2015, self_edge = False)
    G = dp.construct_graph(node_list, edge_list)
    hits = algo.HITS(G, max_iterations = 100, min_delta = 0.00001)
    hits = algo.CreditPropagation(G, original_rank = hits, cr = 0.85, max_iterations = 100, min_delta = 0.00001)
    result = sorted(hits.iteritems(), key = lambda asd:asd[1], reverse = True)
    G.clear()
    original_r = []
    for e in result:
        if e[0] in top_50:
            original_r.append([e[0]])

    for k in range(len(original_r)):
        if not original_r[k][0] == "mit":
            node_list, edge_list = dp.read_data_in_range("../data/data_top50_cs_apr09.csv", start_year = 1995, end_year = 2015, self_edge = False)
            G = dp.construct_graph(node_list, edge_list)
            G = add_non_existing_edges(G, original_r[k][0], "mit", weight = 1) ### add one edge from MIT to <node>
            hits = algo.HITS(G, max_iterations = 100, min_delta = 0.00001)
            hits = algo.CreditPropagation(G, original_rank = hits, cr = 0.85, max_iterations = 100, min_delta = 0.00001)
            result = sorted(hits.iteritems(), key = lambda asd:asd[1], reverse = True)
            #result = sorted(hits.iteritems(), key = lambda asd:asd[1], reverse = True)
            G.clear()
            res1 = []
            for e in result:
                if e[0] in top_50:
                    res1.append(e[0])
            kr = 0
            for i in range(len(res1)):
                if res1[i] == original_r[k][0]:
                    kr = i
            original_r[k].append(k-kr)
    print original_r
    fo.write("univ,diff+mit1\n")
    for r in original_r:
        for i in range(len(r)):
            if i == 0:
                fo.write(str(r[i]))
            else:
                fo.write(","+str(r[i]))
        fo.write("\n")
    fo.close()


def sensitive_3():
    top_50 = []
    f = open("../data/univ_top_50_cs.txt","r")
    for line in f:
        line = line.strip().lower()
        top_50.append(line)
    f.close()
    
    fo = open("../result/result_top50_cs_newdata_apr09/sensitivity/all/sensitivity_diff_hits_weighted-inedge1.csv","w")
    node_list, edge_list = dp.read_data("../data/data_top50_cs_apr09.csv", self_edge = False)
    G = dp.construct_graph(node_list, edge_list)
    hits = algo.weighted_HITS(G, max_iterations = 100, min_delta = 0.00001)
    result = sorted(hits.iteritems(), key = lambda asd:asd[1], reverse = True)
    G.clear()
    
    rank = []
    for e in result:
        if e[0] in top_50:
            rank.append(e[0])

    original_r = []
    for e in result:
        if e[0] in top_50:
            original_r.append([e[0]])

    for k in range(len(original_r)):
#         if not original_r[k][0] == "mit":
            node_list, edge_list = dp.read_data("../data/data_top50_cs_apr09.csv", self_edge = False)
            G = dp.construct_graph(node_list, edge_list)
            G = remove_significant_edge(G, original_r[k][0], rank = rank) ### add one edge from MIT to <node>
            hits = algo.weighted_HITS(G, max_iterations = 100, min_delta = 0.00001)
            result = sorted(hits.iteritems(), key = lambda asd:asd[1], reverse = True)
            #result = sorted(hits.iteritems(), key = lambda asd:asd[1], reverse = True)
            G.clear()
            res1 = []
            for e in result:
                if e[0] in top_50:
                    res1.append(e[0])
            kr = 0
            for i in range(len(res1)):
                if res1[i] == original_r[k][0]:
                    kr = i
            original_r[k].append(k-kr)
    print original_r
    fo.write("univ,diff+mit1\n")
    for r in original_r:
        for i in range(len(r)):
            if i == 0:
                fo.write(str(r[i]))
            else:
                fo.write(","+str(r[i]))
        fo.write("\n")
    fo.close()


def remove_significant_edge(G, univ = "harvard", rank = []):
    """
    @description: remove one existing significant in_edge from <univ>;
    if there is no in_edge, remove one existing significant out_edge from <univ>

    @type G: DiGraph
    @param G: directed graph
    
    @type univ: String
    @param univ: name of the university
    
    @return: new graph with remove edge
    """
    inedges = G.in_edges(univ, data = True)
    innodes = [e[0] for e in inedges]
    target = ""
    if len(inedges) > 0: # remove in_edge
        for r in rank:
            if r in innodes:
                target = r
                break
        if G.get_edge_data(target, univ, default = None)['weight'] == 1:
            G.remove_edge(target, univ)
        else:
            newweight = G.get_edge_data(target, univ, default = None)['weight']-1
            G.add_edge(target, univ, {'weight' : newweight})
    else: # remove out_edge
        outedges = G.out_edges(univ, data = True)
        outnodes = [o[1] for o in outedges]
        for r in rank:
            if r in outnodes:
                target = r
                break
        if G.get_edge_data(univ, target, default = None)['weight'] == 1:
            G.remove_edge(univ, target)
        else:
            newweight = G.get_edge_data(univ, target, default = None)['weight']-1
            G.add_edge(univ, target, {'weight' : newweight})
    return G


def add_non_existing_edges(G, univ = "harvard", fake_node = "mit", weight = 1):
    """
    @description: add <weight> non-existing edge(s) from mit to <univ>
    
    @type G: DiGraph
    @param G: the graph
    
    @type uinv: String
    @param univ: name of university
    
    @return: new graph with added edge
    """
    newweight = 1
    if G.has_edge(fake_node, univ):
        newweight += G.get_edge_data(fake_node, univ, default=None)['weight']
    else:
        pass
    G.add_edge(fake_node, univ, {"weight" : newweight})
    return G

def main():
    sensitive_3()
    
if __name__ == "__main__":
    main()