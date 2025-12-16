import numpy as np
import random


class temperature:
    def __init__(self, update_method, init_T, final_T, alpha):
        self.now = init_T
        self.init_T = init_T
        self.final_T = final_T
        self.alpha = alpha

        if update_method == 'linear':
            self.update = self.update_linear
        elif update_method == 'exponential':
            self.update = self.update_exp
        else:
            raise Exception()
    
    def update_exp(self, iteration):
        self.now = self.init_T * np.exp(-iteration * self.alpha)
        
    def update_linear(self, iteration):
        self.now = self.init_T - (iteration * self.alpha)
        

def sim_anneal(routes, ls, temp_upd_method, init_T = 50, final_T = 1, alpha = 0.01, max_iter=1000):
    T = temperature(temp_upd_method, init_T, final_T, alpha)

    i = 0
    di = 0
    while T.now > final_T:
        for _ in range(max_iter):
            # choose perturbation
            if random.random() > 0.80: 
                ls_method = 'relocation'
            else:
                ls_method = 'exchange'
            
            route1, node1, route2, node2, delta = ls.apply_local_search(routes.edges, routes.edges_inc, routes.load, node_route = routes.node_route, method = ls_method) 

            if route1 is None:
                continue

            if delta < 0:
                routes.commit(route1, node1, route2, node2, method = ls_method)

                if routes.get_delta_from_best() < 0:
                    routes.update_best()

            # acceptance probability
            elif  np.exp(-delta/T.now) > random.random():
                routes.commit(route1, node1, route2, node2, method = ls_method)
            
        # check if deviation threshold is violated
        if routes.get_delta_from_best() > 500:
            di += 1
            routes.reset_to_best()

        i += 1
        T.update(i)
    print(f"Iterations: {i*max_iter} -- deviation threshold violated: {di}")
    return routes
