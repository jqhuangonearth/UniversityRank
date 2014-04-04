"""
@material: http://pages.cs.wisc.edu/~remzi/rank.html
@description: algorithms to rank the universities based on graph
@author: Bolun
"""

def weighted_pagerank(graph, damping_factor=0.85, max_iterations=100, min_delta=0.00001):
    """
    Compute and return the PageRank in an directed graph.    
    
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
                split_factor = 0.0
                on = graph.out_edges(referring_page[0], data = True)
                for nd in on:
                    split_factor += nd[2]['weight']
                rank += damping_factor * pagerank[referring_page[0]] * referring_page[2]['weight'] / split_factor
                
            diff += abs(pagerank[node] - rank)
            pagerank[node] = rank
        #stop if PageRank has converged
        print i
        if diff < min_delta:
            break
        
    return pagerank