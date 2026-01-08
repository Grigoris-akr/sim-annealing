import numpy as np
import random
from utils import temperature


def sa_vns(routes, ls, temp_upd_method, init_T, final_T, alpha, ls_iter = 1000):
    """ Hybrid Simulated Annealing and Variable Neighborhood Search algorithm """ 
    print("SA-VNS")

    T = temperature(temp_upd_method, init_T, final_T, alpha)

    print(f"Final temperature: {final_T}")
    while T.now > final_T:
        print(f"Temperature: {T.now:.2f}", end = '\r')

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
    
        # apply local search algorithms and accept solutions based on SA concept 
        for _ in range(ls_iter):
            route1, node1, route2, node2, delta = ls.apply_local_search(routes.edges, routes.edges_inv, routes.load, node_route = routes.node_route, method = ls_method)
    
            # if the LS method failed, continue
            if route1 is None:
                continue
            
            # Basic SA function
            if delta < 0:
                # if the cost is better, do the change
                routes.commit(route1, node1, route2, node2, method = ls_method)

                # Keep the tour if it is the global best
                if routes.get_delta_from_best() < 0:
                    routes.update_best()

            # acceptance probability
            elif  np.exp(-delta/T.now) > random.random():
                routes.commit(route1, node1, route2, node2, method = ls_method)
    
        if routes.get_delta_from_best() < 0:
            # Keep the tour if it is the global best
            routes.update_best()
        else:
            # else go back to best
            routes.rollback()

        T.update()

    print(f"Iterations: {T.iter*ls_iter}")
    return routes 
