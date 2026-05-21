import numpy as np
import random
from utils import ls_random_select

def vns(routes, ls, max_iter = 100, ls_iter = 1000):
    """ Variable Neighborhood Search """ 
    print("Variable Neighborhood Search")

    for i in range(max_iter):
        print(f"Iteration: {i}/{max_iter}\tCost: {routes.get_best_cost():0.2f}", end = '\r')

        # choose perturbation
        ls_method = ls_random_select(reloc_perc = 0.2, exch_perc = 0.5, opt_perc = 0.3)

        # apply a local search method and get the attributes
        route1, node1, route2, node2, delta = ls.apply_local_search(routes.edges, routes.edges_inv, routes.load, node_route = routes.node_route, method = ls_method)
    
        # if the LS method failed, continue
        if route1 is None:
            continue
    
        # apply the turbulation
        routes.commit(route1, node1, route2, node2, method = ls_method)
    
        # apply local search algorithms and only keep better solutions
        for _ in range(ls_iter):
            route1, node1, route2, node2, delta = ls.apply_local_search(routes.edges, routes.edges_inv, routes.load, node_route = routes.node_route, method = ls_method)
    
            # if the LS method failed, continue
            if route1 is None:
                continue
    
            if delta < 0:   
                routes.commit(route1, node1, route2, node2, method = ls_method)
    
        if routes.get_delta_from_best() < 0:
            # Keep the tour if it is the global best
            routes.update_best()
        else:
            # else go back to best
            routes.rollback()
    
    return routes 
