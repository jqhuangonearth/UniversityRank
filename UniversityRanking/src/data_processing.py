#!/usr/bin/env python

"""
@author: Bolun

@comments: when substracting the graph, please examine whether both end points of an edge are within
the top_50 list; when retaining the entire graph, please comment out *line 38*

"""
import networkx as nx
import matplotlib.pyplot as plt
import stats
import random

class case_analysis:
    def __init__(self):
        self.in_edges = {}
        self.out_edges = {}
        f = open("../data/data_top50_cs_apr09.csv", "r")
        f.readline() # skip the first row
        for line in f:
            line = line.lower()
            line = line.strip() # remove those "\r\n"
            lines = line.split(",") ## subject to change
            if len(lines) >= 2:
                ## in edges
                inedge = []
                inedge.append(lines[0].strip())
                if len(lines) > 2 and len(lines[2]) == 4:
                    inedge.append(int(lines[2].strip()))
                if not self.in_edges.has_key(lines[1].strip()):
                    self.in_edges.update({lines[1].strip() : [inedge]})
                else:
                    self.in_edges[lines[1].strip()].append(inedge)
                ## out edges
                outedge = []
                outedge.append(lines[1].strip())
                if len(lines) > 2 and len(lines[2]) == 4:
                    outedge.append(int(lines[2].strip()))
                if not self.out_edges.has_key(lines[0].strip()):
                    self.out_edges.update({lines[0].strip() : [outedge]})
                else:
                    self.out_edges[lines[0].strip()].append(outedge)
        f.close()
        
    def get_in_edges(self, univ):
        """
        @type univ: String
        @param univ: the name of the university to look into
        """
        res = []
        if not self.in_edges.has_key(univ):
            return "error: %s doesn't have any incoming edge" %univ
        else:
            res = self.in_edges[univ]
        return res
        
    def get_out_edges(self, univ):
        """
        @type univ: String
        @param univ: the name of the university to look into
        """
        res = []
        if not self.out_edges.has_key(univ):
            return "error: %s doesn't have any outgoing edge" %univ
        else:
            res = self.out_edges[univ]
        return res

    def save_to_csv(self, reslist = [], univ = "harvard", type = "in_edges"):
        """
        @type reslist: list
        @param reslist: result list
        
        @type univ: String
        @param univ: university name
        
        @type type: String
        @param type: "in_edges" or "out_edges"
        """
        path = "../result/result_top50_cs_newdata_apr09/case_studies/"
        sav_path = path+type+"_"+univ+".csv"
        f = open(sav_path, "w")
        f.write("univ,year\n")
        for node in reslist:
            for i in range(len(node)):
                if i == 0:
                    f.write(str(node[i]))
                else:
                    f.write(","+str(node[i]))
            f.write("\n")
        f.close()


# ## case analysis
# ca = case_analysis()
# ca.save_to_csv(ca.get_in_edges("sunystonybrook"), "sunystonybrook", type = "in_edges")
# ca.save_to_csv(ca.get_in_edges("uminnesota"), "uminnesota", type = "in_edges")
# ca.save_to_csv(ca.get_in_edges("northcarolinastate"), "northcarolinastate", type = "in_edges")
# ca.save_to_csv(ca.get_in_edges("duke"), "duke", type = "in_edges")
# ca.save_to_csv(ca.get_in_edges("rice"), "rice", type = "in_edges")
# ca.save_to_csv(ca.get_in_edges("yale"), "yale", type = "in_edges")
# ca.save_to_csv(ca.get_in_edges("harvard"), "harvard", type = "in_edges")
# ca.save_to_csv(ca.get_in_edges("nyu"), "nyu", type = "in_edges")
# 
# exit(0)

def read_data(filename, self_edge = True):
    """
    @type filename: string
    @param filename: input file path and name
    
    @type self_edge: Boolean
    @param self_edge: whether self edges are included or not; True-yes, False-not
    
    @return: list of nodes
    @return: list of edges
    """
    top_50 = []
    f = open("../data/univ_top_40_me.txt","r")
    for line in f:
        line = line.strip().lower()
        top_50.append(line)
    f.close()
    
    ## statistical analysis
    hist = stats.histogram()
    
    stat = {}
    
    s = {}
    edge_list_all = []
    f = open(filename,"r")
#     print f.readline() # skip the first row
    for line in f:
        line = line.lower()
        line = line.strip() # remove those "\r\n"
        lines = line.split(";") ## subject to change
        if len(lines) == 2 or len(lines) == 3:
#             if lines[0].strip() in top_50 and lines[1].strip() in top_50:
                edge = []
                for i in range(2):
                    edge.append(lines[i].strip())
                    if s.has_key(lines[i].strip()):
                        s[lines[i].strip()] += 1
                    else:
                        s.update({lines[i].strip() : 1})
                if len(lines) == 2: # without year data
                    edge.append("-")
                    
                    if not stat.has_key(lines[0]):
                        stat.update({lines[0] : {'total' : 1, 'wyear' : 0}})
                    else:
                        stat[lines[0]]['total'] += 1
                else: 
                    #print lines
                    if len(lines[2]) > 0: # with year data
                        edge.append(lines[2].strip())
                        hist.add(lines[2].strip())
                        
                        if not stat.has_key(lines[0]):
                            stat.update({lines[0] : {'total' : 1, 'wyear' : 1}})
                        else:
                            stat[lines[0]]['total'] += 1
                            stat[lines[0]]['wyear'] += 1
                    else: # without year data
                        if not stat.has_key(lines[0]):
                            stat.update({lines[0] : {'total' : 1, 'wyear' : 0}})
                        else:
                            stat[lines[0]]['total'] += 1
                        
                    
                    
                edge_list_all.append(edge)
    f.close()
    
#     # statistical
#     f = open("../result/me/year_statistical.csv","w")
#     f.write("univ,total,wyear\n")
#     for key in stat:
#         f.write("%s,%d,%d\n" %(key, stat[key]['total'], stat[key]['wyear']))
#     f.close()
#     
#     index, dist, cdf = hist.cdf()
#     print hist._max, hist._min
#     print len(index), index
#     print len(dist), dist
#     print len(cdf), cdf
#   
#     # the CDF of year distribution
#     f = open("../result/me/year_cdf.csv","w")
#     f.write("year,freq,percentile\n")
#     for i in range(len(index)):
#         f.write("%s,%d,%.3f\n" %(index[i], int(dist[i]), cdf[i]))
#     f.close()
#  
#     exit(0)

#     univlist = sorted(s.iteritems(), key = lambda asd:asd[0], reverse = False)
#     fo = open("../data/out_me.csv","w")
#     for i in univlist:
#         fo.write("%s,%d\n" %(i[0],i[1]))
#     fo.close()
#     exit(0)

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
        if self_edge == True:
            edge = []
            edge.extend(item[0].split("#"))
            edge.append(item[1])
            edge_list.append(edge)
        else:
            edge = []
            nodes = item[0].split("#")
            if not nodes[0] == nodes[1]:
                edge.extend(nodes)
                edge.append(item[1])
                edge_list.append(edge)
        
    node_list = sorted(s.keys(), reverse = False)

    return node_list, edge_list


def read_data_in_range(filename = "./", start_year = 2000, end_year = 2014, self_edge = True):
    """
    @description: read the recent data back until specified <cutting_year>
    
    @type filename: string
    @param filename: input file path and name
    
    @type start_year: integer
    @param start_year: the earliest year to be considered

    @type end_year: integer
    @param end_year: the latest year to be considered
    
    @type self_edge: Boolean
    @param self_edge: whether self edges are included or not; True-yes, False-not
    
    @return: list of nodes
    @return: list of edges
    """
    top_50 = []
    f = open("../data/univ_top_40_me.txt","r")
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
        line = line.strip() # remove those "\r\n"
        lines = line.split(";") ## subject to change
        
        if len(lines) == 2 or len(lines) == 3:
#             if lines[0].strip() in top_50 and lines[1].strip() in top_50:
                edge = []
                for i in range(2):
                    edge.append(lines[i].strip())
                    if s.has_key(lines[i].strip()):
                        s[lines[i].strip()] += 1
                    else:
                        s.update({lines[i].strip() : 1})
                if len(lines) == 2: # without year data
                    edge.append("-") ## never enter this loop
                else: 
                    #print lines
                    if len(lines[2]) > 0: # with year data
                        edge.append(lines[2].strip())
                    else: # without year data
                        pass
                edge_list_all.append(edge)
    f.close()
    
    ## statistical analysis
    hist = stats.histogram()
    stat = {}
    cnt = 0
    ## re-organize the edge with weights
    edge_dict = {}
    for edge in edge_list_all:
        if len(edge) == 3 and int(edge[2]) >= start_year and int(edge[2]) <= end_year: ## filtering the recent faculty data
            cnt += 1
            key = edge[0]+"#"+edge[1]
            
            hist.add(edge[2].strip())
            
            if not stat.has_key(edge[0]):
                stat.update({edge[0] : {'total' : 1, 'wyear' : 1}})
            else:
                stat[edge[0]]['total'] += 1
                stat[edge[0]]['wyear'] += 1
            
            if edge_dict.has_key(key):
                edge_dict[key] += 1.0
            else:
                edge_dict.update({key : 1.0})
        else:
            if not stat.has_key(edge[0]):
                stat.update({edge[0] : {'total' : 1, 'wyear' : 0}})
            else:
                stat[edge[0]]['total'] += 1

#     # statistics
#     index, dist, cdf = hist.cdf()
#     print hist._max, hist._min
#     print len(index), index
#     print len(dist), dist
#     print len(cdf), cdf
#     
#     f = open("../result/result_top50_cs_newdata_apr09/year_statistical_from%d_to%d_extended.csv" %(start_year, end_year),"w")
#     f.write("univ,total,wyear\n")
#     for key in stat:
#         f.write("%s,%d,%d\n" %(key, stat[key]['total'], stat[key]['wyear']))
#     f.close()
#     
#     # the CDF of year distribution
#     f = open("../result/result_top50_cs_newdata_apr09/year_cdf_from%d_to%d_extended.csv" %(start_year, end_year),"w")
#     f.write("year,freq,percentile\n")
#     for i in range(len(index)):
#         f.write("%s,%d,%.3f\n" %(index[i], int(dist[i]), cdf[i]))
#     f.close()


    edge_list = []
    for item in edge_dict.iteritems():
        edge = []
        univs = item[0].split("#")
        if not self_edge == True:
            if not univs[0].strip() == univs[1].strip():
                edge.append(univs[0].strip())
                edge.append(univs[1].strip())
                edge.append(item[1])
                edge_list.append(edge)
            else:
                pass
        else:
            edge.append(univs[0].strip())
            edge.append(univs[1].strip())
            edge.append(item[1])
            edge_list.append(edge)
    
    #print len(edge_list), edge_list
    
    node_list = sorted(s.keys(), reverse = False)
    return node_list, edge_list

# read_data_in_range("../data/data_top50_cs_apr09.csv", start_year = 1995, end_year = 2015, self_edge = False)
# exit(0)

def read_data_subtracted_sample(filename, bucket = {}):
    """
    @description: randomly sample a subgraph with is equally the size of half data
    """
    top_50 = []
    f = open("../data/univ_top_50_cs.txt","r")
    for line in f:
        line = line.strip().lower()
        top_50.append(line)
    f.close()
    
    f = open(filename,"r")
    f.readline() # skip the first row
    data = {}
    for line in f:
        line = line.lower()
        line = line.strip() # remove those "\r\n"
        lines = line.split(",") ## subject to change
        
#         if lines[0].strip() in top_50 and lines[1].strip() in top_50:
        if len(lines) >= 2:
            if not data.has_key(lines[0].strip()):
                data.update({lines[0].strip() : [lines[1].strip()]})
            else:
                data[lines[0].strip()].append(lines[1].strip())
    
    for key in data:
        pool = data[key]
        l = len(pool)-1
        limit = bucket[key] # the amount of data we should get
        visited = set()
        cut = []
        if limit <= l:
            while len(visited) < limit:
                r = random.randint(0,l)
                if not r in visited:
                    visited.add(r)
                else:
                    pass
            for e in visited:
                cut.append(pool[e])
        else:
            cut = pool
        data[key] = cut ## cut the dataset to fit the range
    
    node_list = sorted(data.keys())
    edge_dict = {}
    edge_list = []
    cnt = 0
    for key in data:
        for e in data[key]:
            cnt += 1
            if not edge_dict.has_key(key+"#"+e):
                edge_dict.update({key+"#"+e : 1})
            else:
                edge_dict[key+"#"+e] += 1
#     print "count", cnt
    for item in edge_dict.iteritems():
        edge = []
        edge.extend(item[0].split("#"))
        edge.append(item[1])
        edge_list.append(edge)
    
    return node_list, edge_list


def diff_distribution(file1 = "", file2 = ""):
    """
    @description: generate the diff distribution 

    @type file1: string
    @param file1: diff file path and name 1
    
    @type file2: string
    @param file2: diff file path and name 2
    """
    top_50 = []
    f = open("../data/univ_top_50_cs.txt","r")
    for line in f:
        line = line.strip().lower()
        top_50.append(line)
    f.close()

    mydict = {}

    f = open(file1,"r")
    f.readline()
    for line in f:
        lines = line.split(",")
        diff = 0
        if lines[2].strip() == "-":
            diff = -float(lines[1].strip())
        else:
            diff = float(lines[1].strip())
        if not mydict.has_key(lines[0].strip()):
            mydict.update({lines[0].strip() : [int(diff)]})
        else:
            mydict[lines[0].strip()].append(int(diff))
    f.close()
    
    f = open(file2,"r")
    f.readline()
    for line in f:
        lines = line.split(",")
        diff = 0
        if lines[2].strip() == "-":
            diff = -float(lines[1].strip())
        else:
            diff = float(lines[1].strip())
        if not mydict.has_key(lines[0].strip()):
            mydict.update({lines[0].strip() : [int(diff)]})
        else:
            mydict[lines[0].strip()].append(int(diff))
    f.close()
    
    for key in mydict:
        diff = abs(mydict[key][0] - mydict[key][1])
        mydict[key].append(diff)
    result = sorted(mydict.iteritems(), key = lambda asd:asd[1][2], reverse = True)
    return result

# ## calculate the diff distribution
# res = diff_distribution("../result/me/comparison/diff_distribution_from1946_to1990_indegree.csv",
#                         "../result/me/comparison/diff_distribution_from1991_to2014_indegree.csv")
#    
# f = open("../result/me/comparison/diff_distribution_summary_indegree.csv","w")
# f.write("univ,1946,1991,diff\n")
# for i in range(len(res)):
#     f.write("%s,%d,%d,%d\n" %(res[i][0], res[i][1][0], res[i][1][1], res[i][1][2]))
# f.close()
# exit(0)

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

#  
# bucket = {}
# f = open("../result/result_top50_cs_newdata_apr09/year_statistical_from1995_to2015.csv","r")
# f.readline()
# for line in f:
#     lines = line.split(",")
#     try:
#         bucket.update({lines[0] : int(lines[2])})
#     except:
#         pass
# f.close()
 
# #node_list, edge_list = read_data("../data/data_top50_cs_apr09.csv")
# node_list, edge_list = read_data_in_range("../data/data_top40_me.csv", start_year = 1991, end_year = 2014, self_edge = False)
# #node_list, edge_list = read_data_subtracted_sample("../data/data_top50_cs_apr09.csv", bucket)
# G = nx.DiGraph()
# G = construct_graph(node_list, edge_list)
#  
# # print "graph nodes", len(G.nodes()), G.nodes()
# # print "graph edges", len(G.edges()), G.edges()
#  
# top_50 = []
# f = open("../data/univ_top_40_me.txt","r")
# for line in f:
#     line = line.strip().lower()
#     top_50.append(line)
# f.close()
#   
# #rank in degree
# nodes = rank_univ(G, t = "in_degree")
# f = open("../result/me/univ_top40_me_from1991_to2014_indegree.csv","w")
# for node in nodes:
#     if node[0] in top_50:
#         f.write("%s;%d\n" %(node[0], node[1]))
# f.close()
#  
# #rank out degree
# nodes = rank_univ(G, t = "out_degree")
# f = open("../result/me/univ_top40_me_from1991_to2014_outdegree.csv","w")
# for node in nodes:
#     if node[0] in top_50:
#         f.write("%s;%d\n" %(node[0], node[1]))
# f.close()
# #rank edge degree
# nodes = rank_univ(G, t = "edge_degree")
# f = open("../result/me/univ_top40_me_from1991_to2014_edgedegree.csv","w")
# for node in nodes:
#     if node[0] in top_50:
#         f.write("%s;%d\n" %(node[0], node[1]))
# f.close()
 
# draw_graph(G)
