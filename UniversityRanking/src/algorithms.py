"""
@description: algorithms to rank the universities based on graph
@author: Bolun
"""
import math
from numpy import linalg as la
import numpy as np

class bipartite_graph:
    def __init__(self):
        self.v_hub = {}
        self.v_auth = {}
        self.edge = {}
        
    def convert(self, graph):
        """
        convert DiGraph to bipartite graph
        
        @type graph: digraph
        @param graph: Digraph
        """
        s = set()
        s.intersection()
        
        
        nodes = graph.nodes()
        for node in nodes:
            if graph.in_degree(node) > 0: # authority
                for inode in graph.in_edges(node, data = True):
                    if not self.v_auth.has_key(node):
                        self.v_auth.update({node:set()})
                        self.v_auth[node].add(inode[0])
                    else:
                        self.v_auth[node].add(inode[0])
#                     key = self.const_key(inode[0], node)
#                     self.edge.update({key : inode[2]["weight"]})
            if graph.out_degree(node) > 0: # hubs
                for onode in graph.out_edges(node, data = True):
                    if not self.v_hub.has_key(node):
                        self.v_hub.update({node:set()})
                        self.v_hub[node].add(onode[1])
                    else:
                        self.v_hub[node].add(onode[1])
#                     key = self.const_key(node, onode[1])
#                     self.edge.update({key:onode[2]["weight"]})
        for e in graph.edges(data = True):
            key = self.const_key(e[0], e[1])
            self.edge.update({key : e[2]["weight"]})
    
    def get_auth_degree(self, key):
        degree = 0.0
        for node in self.v_auth[key]:
            k = self.const_key(node, key) # node(hub) -> key(auth)
            if self.edge.has_key(k):
                degree += self.edge[k]
            else:
                pass
        #degree += len(self.v_auth[key])
        if degree == 0.0:
            degree = 1.0 # force it to 1.0
        return degree
    
    def get_hub_degree(self, key):
        degree = 0.0
        for node in self.v_hub[key]:
            k = self.const_key(key, node) # key(hub) -> node(auth)
            if self.edge.has_key(k):
                degree += self.edge[k]
            else:
                pass
        #degree += len(self.v_hub[key])
        if degree == 0.0:
            degree = 1.0 # force it to 1.0
        return degree
    
    def const_key(self, key1, key2):
        """
        construct key in the format of "key1#key2"
        """
        key = key1+"#"+key2
        return key
    
    def get_trans_matrix(self):
        auth_list = self.v_auth.keys()
        hub_list = self.v_hub.keys()
        
        AHMatrix = [[0.0 for j in range(len(hub_list))] for i in range(len(auth_list))]
        for i in range(len(AHMatrix)):
            for j in range(len(AHMatrix[i])):
                if self.edge.has_key(hub_list[j]+"#"+auth_list[i]):
                    AHMatrix[i][j] = self.edge[hub_list[j]+"#"+auth_list[i]] \
                     / self.get_hub_degree(hub_list[j])
        # normalization: each row sum up to 1
        for i in range(len(AHMatrix)):
            t = sum(AHMatrix[i])
            for j in range(len(AHMatrix[i])):
                AHMatrix[i][j] = AHMatrix[i][j] / float(t)
        # factorization
        for i in range(len(AHMatrix)):
            factor = self.get_auth_degree(auth_list[i])
            for j in range(len(AHMatrix[i])):
                AHMatrix[i][j] = AHMatrix[i][j]*float(factor)
                
        return AHMatrix
    
    def get_hub_matrix(self):
        auth_list = self.v_auth.keys()
        hub_list = self.v_hub.keys()
#         print len(hub_list), hub_list
#         print len(auth_list), auth_list
        
        HubMatrix = [[0.0 for j in range(len(auth_list))] for i in range(len(hub_list))]
        for i in range(len(HubMatrix)):
            for j in range(len(HubMatrix[i])):
                if self.edge.has_key(hub_list[i]+"#"+auth_list[j]):
                    HubMatrix[i][j] = self.edge[hub_list[i]+"#"+auth_list[j]] / \
                    self.get_auth_degree(auth_list[j])
        # normalization: each row sum up to 1
        for i in range(len(HubMatrix)):
            t = sum(HubMatrix[i])
            for j in range(len(HubMatrix[i])):
                HubMatrix[i][j] = HubMatrix[i][j] / float(t)
        # factorization
        for i in range(len(HubMatrix)):
            factor = self.get_hub_degree(hub_list[i])
            for j in range(len(HubMatrix[i])):
                HubMatrix[i][j] = HubMatrix[i][j]*float(factor)
        return HubMatrix
    
    def test(self):
        print "len_v_auth", len(self.v_auth)
        print "len_v_hub", len(self.v_hub)
        print "len_edge", len(self.edge)
        for n in self.v_auth:
            if len(self.v_auth[n]) < 1:
                print n
        print
        for n in self.v_hub:
            if len(self.v_hub[n]) < 1:
                print n

def weighted_PR_wnorm(graph, damping_factor=0.85, max_iterations=100, min_delta=0.00001):
    """
    Compute and return the PageRank in an directed graph with normalization
    
    @type  graph: digraph
    @param graph: Digraph.
    
    @type  damping_factor: number
    @param damping_factor: PageRank dumping factor.
    
    @type  max_iterations: number 
    @param max_iterations: Maximum number of iterations.
    
    @type  min_delta: number
    @param min_delta: Smallest variation required to have a new iteration.
    
    @rtype:  Dict
    @return: Dict containing all the nodes PageRank.
    """
    
    nodes = graph.nodes()
    graph_size = len(nodes)
    if graph_size == 0:
        return {}
    min_value = (1.0-damping_factor)/graph_size #value for nodes without inbound links
    
    # itialize the page rank dict with 1/N for all nodes
    pagerank = dict.fromkeys(nodes, 1.0/graph_size)
    
    for i in range(max_iterations):
        diff = 0 #total difference compared to last iteraction
        # computes each node PageRank based on inbound links
        for node in nodes:
            rank = min_value
            ## the incoming nodes
            for referring_page in graph.in_edges(node, data = True):
                """ split factor is normalization factor """
                split_factor = 0.0
                ns = graph.out_edges(referring_page[0], data = True)
                for nd in ns:
                    split_factor += nd[2]['weight']
                rank += damping_factor * pagerank[referring_page[0]] * referring_page[2]['weight'] / split_factor
                
            diff += abs(pagerank[node] - rank)
            pagerank[node] = rank
        #stop if PageRank has converged
        if diff < min_delta:
            break
    
    return pagerank

def weighted_PR_wonorm(graph, damping_factor=0.85, max_iterations=100, min_delta=0.00001):
    """
    Compute and return the PageRank in an directed graph with normalization
    
    @type  graph: digraph
    @param graph: Digraph.
    
    @type  damping_factor: number
    @param damping_factor: PageRank dumping factor.
    
    @type  max_iterations: number 
    @param max_iterations: Maximum number of iterations.
    
    @type  min_delta: number
    @param min_delta: Smallest variation required to have a new iteration.
    
    @rtype:  Dict
    @return: Dict containing all the nodes PageRank.
    """
    
    nodes = graph.nodes()
    graph_size = len(nodes)
    if graph_size == 0:
        return {}
    min_value = (1.0-damping_factor)/graph_size #value for nodes without inbound links
    
    # itialize the page rank dict with 1/N for all nodes
    pagerank = dict.fromkeys(nodes, 1.0/graph_size)
    
    for i in range(max_iterations):
        diff = 0 #total difference compared to last iteraction
        # computes each node PageRank based on inbound links
        for node in nodes:
            rank = min_value
            ## the incoming nodes
            for referring_page in graph.in_edges(node, data = True):
                """ graph size is the fixed normalization factor so that each edge takes equal effect"""
                rank += damping_factor * pagerank[referring_page[0]] * referring_page[2]['weight'] / graph_size
                
            diff += abs(pagerank[node] - rank)
            pagerank[node] = rank
        #stop if PageRank has converged
        if diff < min_delta:
            break
    
    return pagerank


def HITS(graph, max_iterations=100, min_delta=0.00001):
    """
    Compute and return the HITS score in an directed graph.
    from incoming edges
    
    @type  graph: digraph
    @param graph: Digraph.
    
    @type  damping_factor: number
    @param damping_factor: PageRank dumping factor.
    
    @type  min_delta: number
    @param min_delta: Smallest variation required to have a new iteration.
    
    @rtype:  Dict
    @return: Dict containing the auth score of all nodes
    """
    
    nodes = graph.nodes()
    graph_size = len(nodes)
    if graph_size == 0:
        return {}
    
    # itialize the page rank dict with 1/N for all nodes
    auth = dict.fromkeys(nodes, 1.0)
    hub = dict.fromkeys(nodes, 1.0)
    
    i = 0
    for i in range(max_iterations):
        for p in nodes:
            hub_list = [hub.get(q[0]) for q in graph.in_edges(p)]
            #print hub_list
            auth[p] = sum(hub_list)

        auth = normalize(auth)

        old_hub = dict()
        for p in nodes:
            old_hub[p] = hub[p]
            auth_list = [auth.get(r[1]) for r in graph.out_edges(p)]
            #print auth_list
            hub[p] = sum(auth_list)

        hub = normalize(hub)

        delta = sum((abs(old_hub[k] - hub[k]) for k in hub))
        if delta <= min_delta:
            return auth
    return auth


def weighted_HITS(graph, max_iterations=100, min_delta=0.00001):
    """
    Compute and return the HITS score in an directed graph, considering the **weights** for each edge
    from incoming edges
    
    @type  graph: digraph
    @param graph: Digraph.
    
    @type  damping_factor: number
    @param damping_factor: PageRank dumping factor.
    
    @type  min_delta: number
    @param min_delta: Smallest variation required to have a new iteration.
    
    @rtype:  Dict
    @return: Dict containing the auth score of all nodes
    """
    
    nodes = graph.nodes()
    graph_size = len(nodes)
    if graph_size == 0:
        return {}
    
    # itialize the page rank dict with 1/N for all nodes
    auth = dict.fromkeys(nodes, 1.0)
    hub = dict.fromkeys(nodes, 1.0)
    
    i = 0
    for i in range(max_iterations):
        for p in nodes:
            hub_list = [hub.get(q[0])*q[2]["weight"] for q in graph.in_edges(p, data = True)]
            #print hub_list
            auth[p] = sum(hub_list)

        auth = normalize(auth)

        old_hub = dict()
        for p in nodes:
            old_hub[p] = hub[p]
            auth_list = [auth.get(r[1])*r[2]["weight"] for r in graph.out_edges(p, data = True)]
            #print auth_list
            hub[p] = sum(auth_list)

        hub = normalize(hub)

        delta = sum((abs(old_hub[k] - hub[k]) for k in hub))
        if delta <= min_delta:
            return auth
    return auth


def hubavg_HITS(graph, max_iterations=100, min_delta=0.00001):
    """
    Compute and return the HITS score in an directed graph, *averaging the hub by the number of outgoing edges*
    from incoming edges
    
    @type  graph: digraph
    @param graph: Digraph.
    
    @type  damping_factor: number
    @param damping_factor: PageRank dumping factor.
    
    @type  min_delta: number
    @param min_delta: Smallest variation required to have a new iteration.
    
    @rtype:  Dict
    @return: Dict containing the auth score of all nodes
    """
    
    nodes = graph.nodes()
    graph_size = len(nodes)
    if graph_size == 0:
        return {}
    
    # itialize the page rank dict with 1/N for all nodes
    auth = dict.fromkeys(nodes, 1.0)
    hub = dict.fromkeys(nodes, 1.0)
    
    i = 0
    for i in range(max_iterations):
        for p in nodes:
            hub_list = [hub.get(q[0])*q[2]["weight"] for q in graph.in_edges(p, data = True)]
            #print hub_list
            auth[p] = sum(hub_list)

        auth = normalize(auth)

        old_hub = dict()
        for p in nodes:
            old_hub[p] = hub[p]
            out_edges = graph.out_edges(p, data = True)
            split_factor = 0.0
            for e in out_edges:
                split_factor += e[2]["weight"]
            auth_list = [auth.get(r[1])*r[2]["weight"]/split_factor for r in out_edges]
            #print auth_list
            hub[p] = sum(auth_list)

        hub = normalize(hub)

        delta = sum((abs(old_hub[k] - hub[k]) for k in hub))
        if delta <= min_delta:
            return auth
    return auth


def authavg_HITS(graph, max_iterations=100, min_delta=0.00001):
    """
    Compute and return the HITS score in an directed graph, *averaging the auth by the number of incoming edges*
    
    @type  graph: digraph
    @param graph: Digraph.
    
    @type  damping_factor: number
    @param damping_factor: PageRank dumping factor.
    
    @type  min_delta: number
    @param min_delta: Smallest variation required to have a new iteration.
    
    @rtype:  Dict
    @return: Dict containing the auth score of all nodes
    """
    
    nodes = graph.nodes()
    graph_size = len(nodes)
    if graph_size == 0:
        return {}
    
    # itialize the page rank dict with 1/N for all nodes
    auth = dict.fromkeys(nodes, 1.0)
    hub = dict.fromkeys(nodes, 1.0)
    
    i = 0
    for i in range(max_iterations):
        for p in nodes:
            in_edges = graph.in_edges(p, data = True)
            split_factor = 0.0
            for e in in_edges:
                split_factor += e[2]["weight"]
            hub_list = [hub.get(q[0])*q[2]["weight"]/split_factor for q in in_edges]
            #print hub_list
            auth[p] = sum(hub_list)

        auth = normalize(auth)

        old_hub = dict()
        for p in nodes:
            old_hub[p] = hub[p]
            auth_list = [auth.get(r[1])*r[2]["weight"] for r in graph.out_edges(p, data = True)]
            #print auth_list
            hub[p] = sum(auth_list)

        hub = normalize(hub)

        delta = sum((abs(old_hub[k] - hub[k]) for k in hub))
        if delta <= min_delta:
            return auth
    return auth


def weighted_HITS_normalized(graph, max_iterations=100, min_delta=0.00001):
    """
    Compute and return the HITS score in an directed graph, *averaging the auth by the number of incoming edges* &&
    *averaging the auth by the number of incoming edges*
    
    @type  graph: digraph
    @param graph: Digraph.
    
    @type  damping_factor: number
    @param damping_factor: PageRank dumping factor.
    
    @type  min_delta: number
    @param min_delta: Smallest variation required to have a new iteration.
    
    @rtype:  Dict
    @return: Dict containing the auth score of all nodes
    """
    
    nodes = graph.nodes()
    graph_size = len(nodes)
    if graph_size == 0:
        return {}
    
    # itialize the page rank dict with 1/N for all nodes
    auth = dict.fromkeys(nodes, 1.0)
    hub = dict.fromkeys(nodes, 1.0)
    
    i = 0
    for i in range(max_iterations):
        for p in nodes:
            in_edges = graph.in_edges(p, data = True)
            split_factor = 0.0
            for e in in_edges:
                split_factor += e[2]["weight"]
            hub_list = [hub.get(q[0])*q[2]["weight"] for q in in_edges]
            #print hub_list
            auth[p] = sum(hub_list)

        auth = normalize(auth)

        old_hub = dict()
        for p in nodes:
            old_hub[p] = hub[p]
            out_edges = graph.in_edges(p, data = True)
            split_factor = 0.0
            for e in out_edges:
                split_factor += e[2]["weight"]
            auth_list = [auth.get(r[1])*r[2]["weight"] for r in out_edges]
            #print auth_list
            hub[p] = sum(auth_list)

        hub = normalize(hub)

        delta = sum((abs(old_hub[k] - hub[k]) for k in hub))
        if delta <= min_delta:
            return auth
    return auth


def SALSA(graph):
    """
    Compute and return the auth and hub score using salsa (stochastic approach for link-structure \
    analysis) algorithm from incoming edges
    @comments: consider the backward ramdom walk in web surfing (not good for our problem)
    
    @type  graph: digraph
    @param graph: Digraph.
    
    @rtype:  Dict
    @return: Dict containing the auth score of all nodes
    """
    bg = bipartite_graph()
    bg.convert(graph)
    auth_list = bg.v_auth.keys()
    
    A = [[0.0 for i in range(len(auth_list))] for i in range(len(auth_list))]
#     print A
    for i in range(len(A)):
        for j in range(len(A[i])):
            val = 0.0
            klist = list(bg.v_auth[auth_list[i]].intersection(bg.v_auth[auth_list[j]]))
            for k in klist:
                val += bg.edge[k+"#"+auth_list[i]] * bg.edge[k+"#"+auth_list[j]] / bg.get_auth_degree(auth_list[i]) / bg.get_hub_degree(k)
            A[j][i] = val
#     print A
    for i in range(len(A)):
        s = sum(A[i])
        for j in range(len(A[i])):
            #print A[i][j], s
            #print float(A[i][j])/float(s)
            A[i][j] = A[i][j]/s
            #print A[i][j]
#     print A
    An = np.array(A)
    ATn = list(An.transpose())
#     print ATn
#     exit(0)
    D,V = la.eig(ATn)
    print D
    print V
    maxeigval = float("-inf")
    index = 0
    for i in range(len(D)):
        if D[i] > maxeigval:
            maxeigval = D[i]
            index = i
        else:
            pass
    print index
    print auth_list
    print V[index]
    
    res = {}
    for i in range(len(auth_list)):
        res.update({auth_list[i] : V[index][i]})
    
    #print sorted(res.iteritems(), key = lambda asd:asd[1], reverse = True)
    
    return res


def modified_SALSA(graph, max_iterations=100, min_delta=0.00001):
    """
    
    """
    bg = bipartite_graph()
    bg.convert(graph)
    
    auth_list = bg.v_auth.keys()
    hub_list = bg.v_hub.keys()
    
    auth_index = {}
    hub_index = {}
    
    for i in range(len(auth_list)):
        auth_index.update({auth_list[i] : i})
        
    for i in range(len(hub_list)):
        hub_index.update({hub_list[i] : i})
    
    auth_matrix = bg.get_trans_matrix()
    hub_matrix = bg.get_hub_matrix()
    
    auth = dict.fromkeys(auth_list, 1.0)
    hub = dict.fromkeys(hub_list, 1.0)
    
    i = 0
    for i in range(max_iterations):
        
        old_auth = dict(auth)
        for p in auth_list:
            hub_l = [hub.get(q[0])*auth_matrix[auth_index[p]][hub_index[q[0]]] for q in graph.in_edges(p)]
            #print hub_l
            auth[p] = sum(hub_l)
        
        auth = normalize(auth)
        
        for p in hub_list:
            auth_l = [auth.get(q[1])*hub_matrix[hub_index[p]][auth_index[q[1]]] for q in graph.out_edges(p)]
            hub[p] = sum(auth_l)

        hub = normalize(hub)

        delta = sum((abs(old_auth[k] - auth[k]) for k in auth_list))
        if delta <= min_delta:
            return auth
        
    return auth

def CreditPropagation(graph, original_rank = {}, cr = 0.15, max_iterations=100, min_delta=0.00001):
    """
    Compute and return the credit score in an directed graph
    @comment: This algorithm should be applied on the base of pagerank/hits so as to reinforce the score distribution
    
    @type  graph: digraph
    @param graph: Digraph.
    
    @type original_rank: Dict
    @param original_rank: dictionary of initial rankings(credits) of nodes
    
    @type  damping_factor: number
    @param damping_factor: PageRank dumping factor.
    
    @type  min_delta: number
    @param min_delta: Smallest variation required to have a new iteration.
    
    @rtype:  Dict
    @return: Dict containing the auth score of all nodes
    """
    
    nodes = graph.nodes()
    graph_size = len(nodes)
    if graph_size == 0:
        return {}

    # itialize the page rank dict with 1/N for all nodes
    credit = dict(original_rank)

    i = 0
    for i in range(max_iterations):
        old_credit = dict(credit) # make a copy of the previous credit scores
        for p in nodes:
            auth_score = 0.0
            auth_factor = 0.0
            in_edges = graph.in_edges(p, data = True)
            for e in in_edges:
                auth_factor += e[2]["weight"]
            for e in in_edges:
                auth_score += (1.0+cr)*old_credit[e[0]]#*e[2]["weight"]
            
            hub_score = 0.0
            hub_factor = 0.0
            out_edges = graph.out_edges(p, data = True)
            for e in out_edges:
                hub_factor += e[2]["weight"]
            for e in out_edges:
                hub_score += (1.0-cr)*old_credit[e[1]]#*e[2]["weight"]
            credit[p] = auth_score + hub_score + old_credit[p]#*(len(in_edges)+len(out_edges))# update the credits

        credit = normalize(credit)

        delta = sum((math.fabs(old_credit[k] - credit[k]) for k in credit))
        if delta <= min_delta:
            return credit
    return credit


def normalize(dictionary):
    length = len(dictionary)
    """ Normalize the values of a dictionary to sum up to 1. """
    norm = sum((dictionary[p] for p in dictionary))
    if norm!=0:
        return {k: (v / float(norm))*length for (k, v) in dictionary.items()}
    else:
        return {k: v for (k, v) in dictionary.items()}
    
    
