"""
@description: algorithms to rank the universities based on graph
@author: Bolun
"""

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


def weighted_HITS(graph, max_iterations=100, min_delta=0.00001):
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
    @return: Dict containing the hits score of all nodes
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
        old_auth = dict(auth)
        for p in nodes:
            auth_list = [auth.get(q[0]) for q in graph.in_edges(p)]
            #print hub_list
            auth[p] = sum(auth_list)

        auth = normalize(auth)

#         old_hub = dict()
#         for p in nodes:
#             old_hub[p] = hub[p]
#             auth_list = [auth.get(r[1]) for r in graph.out_edges(p)]
#             #print auth_list
#             hub[p] = sum(auth_list)
# 
#         hub = normalize(hub)

        delta = sum((abs(old_auth[k] - auth[k]) for k in hub))
        if delta <= min_delta:
            return auth
    return auth


def normalize(dictionary):
    length = len(dictionary)
    """ Normalize the values of a dictionary to sum up to 1. """
    norm = sum((dictionary[p] for p in dictionary))
    if norm!=0:
        return {k: (v / float(norm))*length for (k, v) in dictionary.items()}
    else:
        return {k: v for (k, v) in dictionary.items()}