#!/home/golis/.venvs/venv1/bin/python3
import numpy as np
import random


def cost_deviation_watchdog():
    pass

class temperature:
    def __init__(self, init_T, final_T, alpha):
        self.now = init_T
        self.init_T = init_T
        self.final_T = init_T
        self.alpha = alpha
        # maybe final_T == 0 -> easy check
    
    def update(self, iteration):
        self.now = max(final_T, (self.init_T * np.exp(-iteration * self.alpha)))
        
    

def acceptance(delta, T):
    return np.exp(-(delta/T)) > random.rand()



def sim_anneal(routes, node_dem_l, init_T = 1200, final_T = 1, alpha = 0.9, max_iter=1000):
    N = np.size(adj_cube, axis = 1)
    print(f"N: {N}")
    T = temperature(init_t, final_T, alpha)

    i = 0
    while T.now:
        
        for i in range(max_iter):
            # choose perturbation

            # 1-0 reloc
            
            rand_node = random.rand([1, N])
            
            # calculate cost difference
            delta = routes.get_delta()

            if delta < 0:
                routes.update_best()
                continue

            if acceptance(delta, T.now):
                #keep solution
                routes.apply_perturbation()
            
            if deviation_too_much:
                routes.reset_to_best()

        i += 1
        T.update(i, alpha)

    return routes
