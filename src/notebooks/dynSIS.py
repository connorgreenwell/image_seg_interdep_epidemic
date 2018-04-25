import numpy as np
from math import log

def dyn_run(nw, samples, run_time, init): 

    def weight(edge):
        # return np.exp(8.0 / (0.1 + edge[2]['weight'])) / 500
        return np.exp(8 * edge[2]['weight']) / 1000000000 - 1

    def unaffected(edge):
        return sigma[edge[1]] == 0

    def weighted_degree(ver):
        return sum(map(weight, nw.edges(ver, data=True)))

    def filtered_weighted_degree(ver):
        return sum(map(weight, filter(unaffected, nw.edges(ver, data=True))))
    
    i = 0
    while i < samples:
        i += 1
        sigma = dict.fromkeys({ i : 0 for i in nw.nodes()}, 0)
        infected_nodes = []
        edges_infected = 0
        for ver in np.random.permutation(nw.nodes()):
            infected_nodes.append(ver)
            sigma[ver] = 3
            edges_infected += filtered_weighted_degree(ver)
            if len(infected_nodes) == init:
                break
        t = 0
        increasing = 10
        while t < run_time and increasing > 0:
            increasing -= 1
            x = np.random.uniform() * edges_infected
            for sourceVer in infected_nodes:
                x -= filtered_weighted_degree(sourceVer)
                if x <= 0:
                    break
            edges = list(filter(unaffected, nw.edges(sourceVer, data=True)))
            if len(edges) == 0:
                continue
            edge = max(edges, key=weight)
            t += 1 / weight(edge)
            ver = edge[1]
            sigma[ver] = 1
            edges_infected += 2 * filtered_weighted_degree(ver) - weighted_degree(ver)
            infected_nodes.append(ver)
            increasing += 1
        yield sigma
