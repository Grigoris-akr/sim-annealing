#!/home/golis/.venvs/venv1/bin/python3
import numpy as np
import random


def vns(routes, ls, max_iter = 100, ls_iter = 1000):
    """ Variable Neighborhood Search """ 
    print("Variable Neighborhood Search")

    for i in range(max_iter):
        # choose perturbation
        rand = random.random()
        if rand > 0.8:
            ls_method = 'relocation'
        elif rand > 0.5:
            ls_method = '2opt'
        else:
            ls_method = 'exchange'
    
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
