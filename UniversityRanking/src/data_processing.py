#!/usr/bin/env python

"""
@author: Bolun
"""
import networkx as nx
import matplotlib.pyplot as plt


def read_data(filename):
    """
    @type filename: string
    @param filename: input file path and name
    
    @return: list of nodes
    @return: list of edges
    """
    top_50 = []
    f = open("../data/univ_top_50_cs.csv","r")
    for line in f:
        line = line.strip().lower()
        top_50.append(line)
    f.close()
    
    s = {}
    edge_list_all = []
    f = open(filename,"r")
    f.readline() # skip the first row
    for line in f:
        line = line.lower()
        lines = line.split(";")
        if len(lines) == 2:
#             if lines[0].strip() in top_50 and lines[1].strip() in top_50:
                edge = []
                for w in lines:
                    edge.append(w.strip())
                    if s.has_key(w.strip()):
                        s[w.strip()] += 1
                    else:
                        s.update({w.strip() : 1})
                edge_list_all.append(edge)
    f.close()
    univlist = sorted(s.iteritems(), key = lambda asd:asd[0], reverse = False)
    fo = open("../data/out_extended.csv","w")
    for i in univlist:
        fo.write("%s;%d\n" %(i[0],i[1]))
    fo.close()
    print len(edge_list_all)
    ## re-organize the edge with weights
    edge_dict = {}
    for edge in edge_list_all:
        key = edge[0]+"#"+edge[1]
        if edge_dict.has_key(key):
            edge_dict[key] += 1.0
        else:
            edge_dict.update({key : 1.0})
    edge_list = []
    for item in edge_dict.iteritems():
        edge = []
        edge.extend(item[0].split("#"))
        edge.append(item[1])
        edge_list.append(edge)
            
    node_list = sorted(s.keys(), reverse = False)
#     print len(node_list), node_list
#     print len(edge_list), edge_list
    return node_list, edge_list

def construct_graph(node_list, edge_list):
    """
    @type node_list: list
    @param node_list: list of uid of users
        
    @type edge_list: list of two tuple list
    @param edge_list: list of edges represented by [uid1, uid2]
    
    @type G: nx directed graph
    @return G: nx directed graph
    """
    G = nx.DiGraph()
    for node in node_list:
        G.add_node(node)
    for edge in edge_list:
        G.add_edge(edge[0], edge[1], weight = edge[2])
    return G


def draw_graph(G):
    """
    @type G: DiGraph
    @param G: DiGraph
    """
    nx.draw(G, pos = nx.random_layout(G, dim = 2), randomcmap = plt.get_cmap('jet'), node_color = "blue", \
            alpha = 0.5, width = 1, node_size = 200, with_labels=True)
    plt.show()

def rank_univ(G, t = "edge_degree"):
    """
    @description: rank the nodes by in_degree/out_degree/in_degree+out_degree in descending order
    
    @type G: networkx DiGraph
    @param G: directed graph
    
    @type t: string
    @param t: type of metric; could be "in_degree", "out_degree" or "edge_degree"
    
    @return sorted list of universities
    """
    nodes = []
    for node in G.nodes():
        nodes.append([node])
    if t == "in_degree":
        for node in nodes:
            in_degree = 0.0
            for i in G.in_edges(node[0], data = True):
                in_degree += i[2]["weight"]
            node.append(in_degree)
    elif t == "out_degree":
        for node in nodes:
            out_degree = 0.0
            for i in G.out_edges(node[0], data = True):
                out_degree += i[2]["weight"]
            node.append(out_degree)
    elif t == "edge_degree":
        for node in nodes:
            degree = 0.0
            for i in G.in_edges(node[0], data = True):
                degree += i[2]["weight"]
            for i in G.out_edges(node[0], data = True):
                degree += i[2]["weight"]
            node.append(degree)
    else:
        """ do nothing """
    nodes = sorted(nodes, key = lambda asd:asd[1], reverse = True)
    return nodes

node_list, edge_list = read_data("../data/data_top50_cs.csv")
G = nx.DiGraph()
G = construct_graph(node_list, edge_list)

# top_50 = []
# f = open("../data/univ_top_50_cs.csv","r")
# for line in f:
#     line = line.strip().lower()
#     top_50.append(line)
# f.close()
# 
# #rank in degree
# nodes = rank_univ(G, t = "in_degree")
# f = open("../result/result_top50_cs_extended/univ_top_50_cs_indegree.csv","w")
# for node in nodes:
#     if node[0] in top_50:
#         f.write("%s;%d\n" %(node[0], node[1]))
# f.close()
# 
# #rank out degree
# nodes = rank_univ(G, t = "out_degree")
# f = open("../result/result_top50_cs_extended/univ_top_50_cs_outdegree.csv","w")
# for node in nodes:
#     if node[0] in top_50:
#         f.write("%s;%d\n" %(node[0], node[1]))
# f.close()
# #rank edge degree
# nodes = rank_univ(G, t = "edge_degree")
# f = open("../result/result_top50_cs_extended/univ_top_50_cs_edgedegree.csv","w")
# for node in nodes:
#     if node[0] in top_50:
#         f.write("%s;%d\n" %(node[0], node[1]))
# f.close()

# draw_graph(G)
