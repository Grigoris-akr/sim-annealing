import numpy as np
import random
from utils import temperature


def sim_anneal(routes, ls, temp_upd_method, init_T = 50, final_T = 1, alpha = 0.01, max_iter=1000):
    """ Simulated Annealing function """
    print("Simulated Annealing")

    T = temperature(temp_upd_method, init_T, final_T, alpha)

    # print(f"Final temperature: {final_T}")
    di = 0
    while T.now > final_T:
        # print(f"Temperature: {T.now:.2f}", end = '\r') # print temperature (affects performance)
        for _ in range(max_iter):
            # choose perturbation
            rand = random.random()
            if rand > 0.8: 
                ls_method = 'relocation'
            elif rand > 0.5:
                ls_method = '2opt'
            else:
                ls_method = 'exchange'

            # apply a local search method and get the elements
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
            
        # check if deviation threshold is violated
        if routes.get_delta_from_best() > 500:
            routes.rollback()
            di += 1

        T.update()

    print(f"Iterations: {T.iter*max_iter} -- deviation threshold violated: {di}")
    return routes
